FROM python:3.11-slim

WORKDIR /srv/jupyterhub

RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir jupyterhub jupyterlab notebook
RUN npm install -g configurable-http-proxy

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

EXPOSE 8000
CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
