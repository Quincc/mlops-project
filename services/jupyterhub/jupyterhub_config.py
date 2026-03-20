import os
from jupyter_server.auth import passwd

c = get_config()

c.JupyterHub.bind_url = 'http://0.0.0.0:8000'
c.Authenticator.admin_users = {os.getenv('JUPYTER_ADMIN_USER', 'admin')}
c.JupyterHub.spawner_class = 'simple'
c.JupyterHub.authenticator_class = 'dummy'
c.DummyAuthenticator.password = os.getenv('JUPYTER_ADMIN_PASSWORD', 'admin')
c.Spawner.default_url = '/lab'
c.Spawner.args = ["--allow-root"]
c.Spawner.default_url = "/lab"
c.Spawner.http_timeout = 120
c.Spawner.start_timeout = 120