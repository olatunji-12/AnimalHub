# Gunicorn configuration file for Azure deployment
import multiprocessing

# Binding
bind = "0.0.0.0:5000"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 600

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'pet_adoption_hub'

# SSL Configuration (if needed)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'
