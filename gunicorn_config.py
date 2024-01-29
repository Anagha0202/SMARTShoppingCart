import multiprocessing

workers = multiprocessing.cpu_count()*2+1
bind = 'unix:shoppingcart.sock'
umask = 0o007
reload = True

accesslog = "/var/www/html/shoppingcart/logs/gunicorn_access.log"
errorlog = "/var/www/html/shoppingcart/logs/gunicorn_access.log"
