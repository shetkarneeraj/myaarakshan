"""
Gunicorn Configuration for Maratha Aarakshan Application
Optimized for high-performance production deployment
"""

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = 50  # As requested
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 50

# Restart workers after this many requests, with jitter to prevent all workers restarting at the same time
preload_app = True

# Worker process management
worker_tmp_dir = "/tmp"  # Use memory filesystem for worker tmp
user = None
group = None
tmp_upload_dir = None

# Security
limit_request_line = 0
limit_request_fields = 100
limit_request_field_size = 8190

# Application
wsgi_module = "maratha_aarakshan.wsgi:application"

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"  # Log to stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "maratha_aarakshan"

# Server mechanics
daemon = False
pidfile = "/tmp/maratha_aarakshan.pid"
umask = 0
tmp_upload_dir = None

# Performance tuning
worker_class = "sync"  # Can be changed to "gevent" or "eventlet" for async workloads

# SSL (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Development settings (override in production)
if os.getenv("DEBUG") == "True":
    workers = 1
    reload = True
    loglevel = "debug"

# Environment variables for Django app
raw_env = [
    "DJANGO_SETTINGS_MODULE=maratha_aarakshan.settings",
    "DEBUG=False"
]


def when_ready(server):
    """Called just after the server is started."""
    server.log.info(
        "Maratha Aarakshan server is ready. Listening on: %s", server.address
    )


def worker_int(worker):
    """Called just after a worker has been killed."""
    worker.log.info("Worker received INT or QUIT signal")


def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass


def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_exec(server):
    """Called just before a new master process is forked."""
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Server is ready. Spawning workers")


def worker_abort(worker):
    """Called when a worker receives the SIGABRT signal."""
    worker.log.info("Worker received SIGABRT signal")
