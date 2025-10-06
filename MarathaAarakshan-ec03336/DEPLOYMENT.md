# 🚀 Maratha Aarakshan - Production Deployment Guide

This guide covers multiple deployment options for the Maratha Aarakshan application with **Gunicorn (50 workers)** and **Nginx** optimization.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Traditional Server Deployment](#traditional-server-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Vercel Deployment](#vercel-deployment)
5. [Performance Optimization](#performance-optimization)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **RAM**: Minimum 4GB (Recommended 8GB+ for 50 workers)
- **CPU**: Minimum 4 cores (Recommended 8+ cores)
- **Storage**: 20GB+ available space
- **Python**: 3.9+
- **Network**: Port 80, 443 open for web traffic

### Domain Setup
- Domain name pointed to your server IP
- SSL certificate (Let's Encrypt recommended)

## 🖥️ Traditional Server Deployment

### Option 1: Automated Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/MarathaAarakshan.git
cd MarathaAarakshan

# Run automated deployment
sudo chmod +x deploy.sh
sudo ./deploy.sh
```

### Option 2: Manual Deployment

#### Step 1: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git curl

# Install Node.js (for additional tools)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### Step 2: Setup Application
```bash
# Create application directory
sudo mkdir -p /var/www/maratha_aarakshan
sudo chown -R $USER:$USER /var/www/maratha_aarakshan

# Clone and setup application
git clone https://github.com/your-username/MarathaAarakshan.git /var/www/maratha_aarakshan
cd /var/www/maratha_aarakshan

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 3: Configure Gunicorn Service
```bash
# Create systemd service
sudo tee /etc/systemd/system/maratha_aarakshan.service > /dev/null <<EOF
[Unit]
Description=Maratha Aarakshan Gunicorn Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/maratha_aarakshan
Environment="PATH=/var/www/maratha_aarakshan/venv/bin"
ExecStart=/var/www/maratha_aarakshan/venv/bin/gunicorn --config gunicorn.conf.py wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
sudo chown -R www-data:www-data /var/www/maratha_aarakshan

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable maratha_aarakshan
sudo systemctl start maratha_aarakshan
```

#### Step 4: Configure Nginx
```bash
# Copy nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/maratha_aarakshan

# Enable site
sudo ln -s /etc/nginx/sites-available/maratha_aarakshan /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

#### Step 5: Setup SSL (Let's Encrypt)
```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

## 🐳 Docker Deployment

### Prerequisites
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Deployment Steps
```bash
# Clone repository
git clone https://github.com/your-username/MarathaAarakshan.git
cd MarathaAarakshan

# Create environment file
cat > .env <<EOF
REDIS_PASSWORD=your_redis_password
GRAFANA_PASSWORD=your_grafana_password
EOF

# Build and start containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f web
```

### Advanced Docker Commands
```bash
# Scale web workers
docker-compose up -d --scale web=3

# Update application
docker-compose build web
docker-compose up -d web

# Monitor resources
docker stats

# Backup data
docker-compose exec redis redis-cli BGSAVE
```

## 🌐 Vercel Deployment

### Prerequisites
```bash
# Install Vercel CLI
npm install -g vercel
```

### Deployment Steps
```bash
# Login to Vercel
vercel login

# Deploy
vercel --prod

# Configure environment variables in Vercel dashboard
# - FLASK_ENV=production
# - FLASK_APP=wsgi:application
```

### Vercel Configuration Features
- **Optimized Routes**: Static files cached for 1 year
- **Security Headers**: XSS protection, content type sniffing prevention
- **Regional Deployment**: Mumbai, Singapore, Tokyo regions
- **Function Optimization**: 1GB memory, 30s timeout

## ⚡ Performance Optimization

### Gunicorn Configuration Highlights
```python
# gunicorn.conf.py highlights
workers = 50                    # High concurrency
worker_class = "sync"          # Synchronous workers
max_requests = 1000            # Worker recycling
preload_app = True             # Faster startup
worker_tmp_dir = "/dev/shm"    # Memory filesystem
```

### Nginx Optimization Features
- **Load Balancing**: Least connections algorithm
- **Caching**: Static files cached for 1 year
- **Compression**: Gzip enabled for text files
- **Rate Limiting**: API protection (10 req/s)
- **Security**: Multiple security headers
- **HTTP/2**: Enabled for better performance

### System Optimizations
```bash
# Increase file limits
echo '* soft nofile 65536' | sudo tee -a /etc/security/limits.conf
echo '* hard nofile 65536' | sudo tee -a /etc/security/limits.conf

# Optimize kernel parameters
sudo tee -a /etc/sysctl.conf <<EOF
net.core.somaxconn = 65536
net.ipv4.tcp_max_syn_backlog = 65536
net.core.netdev_max_backlog = 5000
EOF

sudo sysctl -p
```

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Check application status
sudo systemctl status maratha_aarakshan

# Check nginx status
sudo systemctl status nginx

# Manual health check
curl http://localhost/health

# View application logs
sudo journalctl -u maratha_aarakshan -f

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Automated Monitoring Script
The deployment includes `/usr/local/bin/maratha_monitor.sh` that runs every 5 minutes and:
- Checks service status
- Monitors disk usage
- Monitors memory usage
- Tests application response
- Auto-restarts failed services

### Performance Monitoring
```bash
# Monitor system resources
htop

# Monitor network connections
netstat -tulpn | grep :80

# Monitor Gunicorn processes
ps aux | grep gunicorn

# Check memory usage
free -h

# Check disk usage
df -h
```

## 🛠️ Management Commands

### Using start_server.sh
```bash
# Start server
./start_server.sh start

# Start with custom workers
./start_server.sh start --workers 25 --port 8080

# Development mode
./start_server.sh dev

# Check status
./start_server.sh status

# Restart server
./start_server.sh restart

# View logs
./start_server.sh logs

# Stop server
./start_server.sh stop
```

### Database Management
```bash
# Activate virtual environment
source venv/bin/activate

# Database migrations
export FLASK_APP=wsgi:application
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Backup database
cp instance/maratha_arakshan.db backups/db_$(date +%Y%m%d_%H%M%S).db
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Service Won't Start
```bash
# Check service status
sudo systemctl status maratha_aarakshan

# Check logs
sudo journalctl -u maratha_aarakshan -n 50

# Check configuration
sudo -u www-data /var/www/maratha_aarakshan/venv/bin/gunicorn --config gunicorn.conf.py --check-config wsgi:application
```

#### 2. High Memory Usage
```bash
# Check memory usage per worker
ps aux | grep gunicorn | awk '{print $6, $11}' | sort -n

# Reduce workers temporarily
sudo systemctl edit maratha_aarakshan
# Add: Environment="WORKERS=25"

sudo systemctl restart maratha_aarakshan
```

#### 3. Nginx Errors
```bash
# Test nginx configuration
sudo nginx -t

# Check nginx logs
sudo tail -f /var/log/nginx/error.log

# Reload nginx configuration
sudo systemctl reload nginx
```

#### 4. SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Renew certificates
sudo certbot renew

# Test renewal
sudo certbot renew --dry-run
```

### Performance Tuning

#### Optimize Worker Count
```bash
# Formula: (2 x CPU cores) + 1
# For 8 cores: (2 x 8) + 1 = 17 workers
# For high I/O: Up to 50 workers

# Test with different worker counts
./start_server.sh start --workers 25
# Monitor memory and CPU usage
# Adjust based on performance
```

#### Database Optimization
```bash
# Enable WAL mode for SQLite (if using SQLite)
sqlite3 instance/maratha_arakshan.db "PRAGMA journal_mode=WAL;"

# Optimize database
sqlite3 instance/maratha_arakshan.db "VACUUM;"
sqlite3 instance/maratha_arakshan.db "ANALYZE;"
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use multiple servers behind a load balancer
- Shared database (PostgreSQL recommended)
- Redis for session storage
- CDN for static files

### Vertical Scaling
- Increase server resources
- Optimize worker count
- Use faster storage (SSD)
- Increase network bandwidth

## 🔐 Security Best Practices

1. **Firewall Configuration**
   ```bash
   sudo ufw enable
   sudo ufw allow OpenSSH
   sudo ufw allow 'Nginx Full'
   ```

2. **Regular Updates**
   ```bash
   sudo apt update && sudo apt upgrade -y
   pip install --upgrade -r requirements.txt
   ```

3. **Backup Strategy**
   ```bash
   # Daily database backup
   echo "0 2 * * * cp /var/www/maratha_aarakshan/instance/maratha_arakshan.db /backups/db_\$(date +\%Y\%m\%d).db" | crontab -
   ```

4. **SSL Security**
   - Use strong SSL ciphers
   - Enable HSTS headers
   - Regular certificate renewal

## 📞 Support

For deployment issues or questions:
1. Check the troubleshooting section
2. Review application logs
3. Check system resources
4. Verify configuration files

---

**🎉 Congratulations!** Your Maratha Aarakshan application is now running with **50 Gunicorn workers** and **optimized Nginx** configuration for maximum performance!
