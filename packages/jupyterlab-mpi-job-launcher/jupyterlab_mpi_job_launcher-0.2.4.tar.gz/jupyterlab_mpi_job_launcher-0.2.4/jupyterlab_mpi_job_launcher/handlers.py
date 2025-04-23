import json

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

from jupyterlab_mpi_job_launcher.mpi_job_handler import MpiJobHandler


class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(
            json.dumps(
                {"data": "This is /jupyterlab-mpi-job-launcher/get-example endpoint!"}
            )
        )


def setup_handlers(web_app):
    host_pattern = ".*$"
    app_name = "jupyterlab-mpi-job-launcher"
    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, app_name, "get-example")
    submit_mpi_job = url_path_join(base_url, app_name, "submit")
    handlers = [
        (route_pattern, RouteHandler),
        (submit_mpi_job, MpiJobHandler),
    ]
    web_app.add_handlers(host_pattern, handlers)
