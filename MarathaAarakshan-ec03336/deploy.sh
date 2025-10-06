#!/bin/bash

# Maratha Aarakshan Deployment Script
# Automated deployment with Gunicorn and Nginx

set -e  # Exit on any error

echo "🚀 Starting Maratha Aarakshan Deployment..."

# Configuration
APP_NAME="maratha_aarakshan"
APP_DIR="/var/www/maratha_aarakshan"
NGINX_CONF="/etc/nginx/sites-available/maratha_aarakshan"
NGINX_ENABLED="/etc/nginx/sites-enabled/maratha_aarakshan"
SYSTEMD_SERVICE="/etc/systemd/system/maratha_aarakshan.service"
USER="www-data"
GROUP="www-data"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        log_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    log_info "Installing system dependencies..."
    
    # Update package list
    apt-get update
    
    # Install required packages
    apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        nginx \
        supervisor \
        git \
        curl \
        htop \
        ufw
    
    log_info "Dependencies installed successfully"
}

# Create application directory
setup_app_directory() {
    log_info "Setting up application directory..."
    
    # Create app directory
    mkdir -p $APP_DIR
    
    # Copy application files
    cp -r . $APP_DIR/
    
    # Set ownership
    chown -R $USER:$GROUP $APP_DIR
    
    # Set permissions
    chmod -R 755 $APP_DIR
    
    log_info "Application directory setup complete"
}

# Setup Python virtual environment
setup_python_env() {
    log_info "Setting up Python virtual environment..."
    
    cd $APP_DIR
    
    # Create virtual environment
    sudo -u $USER python3 -m venv venv
    
    # Activate and install dependencies
    sudo -u $USER bash -c "
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
    "
    
    log_info "Python environment setup complete"
}

# Create systemd service for Gunicorn
create_systemd_service() {
    log_info "Creating systemd service..."
    
    cat > $SYSTEMD_SERVICE << EOF
[Unit]
Description=Maratha Aarakshan Gunicorn Application
After=network.target

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --config gunicorn.conf.py wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable maratha_aarakshan
    
    log_info "Systemd service created and enabled"
}

# Configure Nginx
configure_nginx() {
    log_info "Configuring Nginx..."
    
    # Copy nginx configuration
    cp nginx.conf $NGINX_CONF
    
    # Create symbolic link to enable site
    ln -sf $NGINX_CONF $NGINX_ENABLED
    
    # Remove default nginx site
    rm -f /etc/nginx/sites-enabled/default
    
    # Test nginx configuration
    if nginx -t; then
        log_info "Nginx configuration is valid"
    else
        log_error "Nginx configuration test failed"
        exit 1
    fi
    
    log_info "Nginx configuration complete"
}

# Setup firewall
setup_firewall() {
    log_info "Configuring firewall..."
    
    # Enable UFW
    ufw --force enable
    
    # Allow SSH
    ufw allow OpenSSH
    
    # Allow HTTP and HTTPS
    ufw allow 80
    ufw allow 443
    
    # Allow Nginx
    ufw allow 'Nginx Full'
    
    log_info "Firewall configuration complete"
}

# Initialize database
init_database() {
    log_info "Initializing database..."
    
    cd $APP_DIR
    sudo -u $USER bash -c "
        source venv/bin/activate
        export FLASK_APP=wsgi:application
        flask db upgrade || echo 'No migrations to run'
    "
    
    log_info "Database initialization complete"
}

# Start services
start_services() {
    log_info "Starting services..."
    
    # Start and enable Maratha Aarakshan service
    systemctl start maratha_aarakshan
    systemctl status maratha_aarakshan --no-pager
    
    # Restart and enable Nginx
    systemctl restart nginx
    systemctl enable nginx
    systemctl status nginx --no-pager
    
    log_info "Services started successfully"
}

# Create monitoring script
create_monitoring() {
    log_info "Setting up monitoring..."
    
    cat > /usr/local/bin/maratha_monitor.sh << 'EOF'
#!/bin/bash

# Monitoring script for Maratha Aarakshan

check_service() {
    if systemctl is-active --quiet $1; then
        echo "✅ $1 is running"
    else
        echo "❌ $1 is not running"
        systemctl restart $1
        echo "🔄 Restarted $1"
    fi
}

echo "🔍 Maratha Aarakshan Health Check - $(date)"
echo "============================================"

check_service maratha_aarakshan
check_service nginx

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2{printf "%.1f", $5}' | sed 's/%//')
if (( $(echo "$DISK_USAGE > 80" | bc -l) )); then
    echo "⚠️  Disk usage is high: ${DISK_USAGE}%"
else
    echo "💾 Disk usage: ${DISK_USAGE}%"
fi

# Check memory usage
MEM_USAGE=$(free | awk 'NR==2{printf "%.1f", $3*100/$2}')
echo "🧠 Memory usage: ${MEM_USAGE}%"

# Check application response
if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200"; then
    echo "🌐 Application is responding"
else
    echo "🚨 Application is not responding"
    systemctl restart maratha_aarakshan
fi

echo "============================================"
EOF

    chmod +x /usr/local/bin/maratha_monitor.sh
    
    # Add to crontab for automatic monitoring
    (crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/maratha_monitor.sh >> /var/log/maratha_monitor.log") | crontab -
    
    log_info "Monitoring setup complete"
}

# Main deployment function
main() {
    log_info "Starting deployment process..."
    
    check_root
    install_dependencies
    setup_app_directory
    setup_python_env
    create_systemd_service
    configure_nginx
    setup_firewall
    init_database
    start_services
    create_monitoring
    
    log_info "🎉 Deployment completed successfully!"
    log_info "Your application should now be running at:"
    log_info "  - HTTP: http://your-domain.com"
    log_info "  - HTTPS: https://your-domain.com"
    log_info ""
    log_info "To check status:"
    log_info "  sudo systemctl status maratha_aarakshan"
    log_info "  sudo systemctl status nginx"
    log_info ""
    log_info "To view logs:"
    log_info "  sudo journalctl -u maratha_aarakshan -f"
    log_info "  sudo tail -f /var/log/nginx/access.log"
    log_info ""
    log_info "To restart services:"
    log_info "  sudo systemctl restart maratha_aarakshan"
    log_info "  sudo systemctl restart nginx"
}

# Run main function
main "$@"
