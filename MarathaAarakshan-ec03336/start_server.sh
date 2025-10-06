#!/bin/bash

# Quick start script for Maratha Aarakshan Application
# Supports both development and production modes

set -e

# Configuration
APP_NAME="maratha_aarakshan"
VENV_PATH="./venv"
WORKERS=50
HOST="0.0.0.0"
PORT=8000

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

show_help() {
    echo -e "${BLUE}Maratha Aarakshan Server Control${NC}"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  start       Start the application server"
    echo "  stop        Stop the application server"
    echo "  restart     Restart the application server"
    echo "  status      Check server status"
    echo "  dev         Start in development mode"
    echo "  logs        Show application logs"
    echo "  help        Show this help message"
    echo ""
    echo "Options:"
    echo "  --workers N     Number of workers (default: 50)"
    echo "  --port N        Port number (default: 8000)"
    echo "  --host HOST     Host address (default: 0.0.0.0)"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 start --workers 25 --port 8080"
    echo "  $0 dev"
    echo "  $0 restart"
}

# Check if virtual environment exists
check_venv() {
    if [ ! -d "$VENV_PATH" ]; then
        log_warn "Virtual environment not found. Creating..."
        python3 -m venv $VENV_PATH
        source $VENV_PATH/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        log_info "Virtual environment created and dependencies installed"
    fi
}

# Start production server
start_production() {
    log_info "Starting Maratha Aarakshan in production mode..."
    log_info "Workers: $WORKERS, Host: $HOST, Port: $PORT"
    
    check_venv
    source $VENV_PATH/bin/activate
    
    # Create PID directory if it doesn't exist
    mkdir -p /tmp
    
    # Start Gunicorn with custom configuration
    exec gunicorn \
        --config gunicorn.conf.py \
        --workers $WORKERS \
        --bind $HOST:$PORT \
        --daemon \
        --pid /tmp/maratha_aarakshan.pid \
        --access-logfile - \
        --error-logfile - \
        wsgi:application
    
    log_info "Server started successfully!"
    log_info "Application running at http://$HOST:$PORT"
}

# Start development server
start_development() {
    log_info "Starting Maratha Aarakshan in development mode..."
    
    check_venv
    source $VENV_PATH/bin/activate
    
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    export FLASK_APP=wsgi:application
    
    python wsgi.py
}

# Stop server
stop_server() {
    log_info "Stopping Maratha Aarakshan server..."
    
    if [ -f /tmp/maratha_aarakshan.pid ]; then
        PID=$(cat /tmp/maratha_aarakshan.pid)
        if kill -0 "$PID" 2>/dev/null; then
            kill -TERM "$PID"
            log_info "Server stopped (PID: $PID)"
            rm -f /tmp/maratha_aarakshan.pid
        else
            log_warn "PID file exists but process not running"
            rm -f /tmp/maratha_aarakshan.pid
        fi
    else
        log_warn "No PID file found. Attempting to kill any running Gunicorn processes..."
        pkill -f "gunicorn.*wsgi:application" || log_info "No Gunicorn processes found"
    fi
}

# Check server status
check_status() {
    log_info "Checking Maratha Aarakshan server status..."
    
    if [ -f /tmp/maratha_aarakshan.pid ]; then
        PID=$(cat /tmp/maratha_aarakshan.pid)
        if kill -0 "$PID" 2>/dev/null; then
            log_info "✅ Server is running (PID: $PID)"
            
            # Check if server is responding
            if command -v curl >/dev/null 2>&1; then
                if curl -s "http://localhost:$PORT/health" >/dev/null; then
                    log_info "✅ Server is responding to requests"
                else
                    log_warn "⚠️  Server is running but not responding"
                fi
            fi
            
            # Show process details
            ps -p "$PID" -o pid,ppid,cmd,etime,%cpu,%mem
        else
            log_error "❌ PID file exists but process not running"
        fi
    else
        log_warn "❌ Server is not running (no PID file)"
    fi
}

# Show logs
show_logs() {
    log_info "Showing application logs..."
    
    # Show systemd logs if running as service
    if systemctl is-active --quiet maratha_aarakshan 2>/dev/null; then
        journalctl -u maratha_aarakshan -f
    else
        # Show local logs
        if [ -f /var/log/maratha_aarakshan.log ]; then
            tail -f /var/log/maratha_aarakshan.log
        else
            log_warn "No log file found. Server might not be running."
        fi
    fi
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --workers)
                WORKERS="$2"
                shift 2
                ;;
            --port)
                PORT="$2"
                shift 2
                ;;
            --host)
                HOST="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done
}

# Main function
main() {
    case "${1:-help}" in
        start)
            parse_args "$@"
            start_production
            ;;
        stop)
            stop_server
            ;;
        restart)
            stop_server
            sleep 2
            parse_args "$@"
            start_production
            ;;
        status)
            check_status
            ;;
        dev|development)
            start_development
            ;;
        logs)
            show_logs
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
