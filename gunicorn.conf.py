from app.config.settings import get_settings

settings = get_settings()

wsgi_app = "app.app:app"
loglevel = "info"
workers = settings.gunicorn_workers
worker_class = "uvicorn.workers.UvicornWorker"
bind = f"0.0.0.0:{settings.gunicorn_port}"
reload = False
accesslog = "./access/gunicorn-access.log"
errorlog = "./error/gunicorn-error.log"
capture_output = True