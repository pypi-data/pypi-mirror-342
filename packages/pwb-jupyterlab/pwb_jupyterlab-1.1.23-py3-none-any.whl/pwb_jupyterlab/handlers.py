
from pwb_jupyterlab.constants import SERVER_URL, URI_SCHEME, SESSION_URL, URL_ENDPOINT, SERVER_ENDPOINT, HEARTBEAT_ENDPOINT
from pwb_jupyterlab.proxiedServersProvider import ProxiedServersProvider

import json

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

from typing import Awaitable, Optional
class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        if SERVER_URL and len(SERVER_URL) != 0:
            base_url = SERVER_URL
        elif URI_SCHEME:
            base_url = URI_SCHEME + ':'
        else: # this case should only be reached in local testing
            base_url = 'http:'
            print("""Warning: Environment variables SERVER_URL and URI_SCHEME are not set 
                  - proxied server links will not work as expected""")
            
        if SESSION_URL:
            base_session_url = base_url + SESSION_URL
        else: # this case should only be reached in local testing
            base_session_url = base_url
            print("""Warning: Environment variable SESSION_URL is not set -
                  proxied server links will not work as expected""")

        self.finish(json.dumps({
            "baseSessionUrl": base_session_url
        }))


class ProxiedServersHandler(APIHandler):
    def __init__(self, application, request, **kwargs):
        self.provider = kwargs.pop('provider')
        super().__init__(application, request, **kwargs)

    async def prepare(self) -> Optional[Awaitable[None]]:
        await super().prepare()
        await self.provider.load_running_servers()

    @tornado.web.authenticated
    def get(self):
        json_data = self.provider.get_servers_json()
        self.finish(json_data)

class HeartbeatHandler(APIHandler):
    @tornado.web.authenticated
    def get(self):
        self.finish({ "result": True})

def setup_handlers(web_app, url_path):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]

    url_route_pattern = url_path_join(base_url, url_path, URL_ENDPOINT)
    servers_route_pattern = url_path_join(base_url, url_path, SERVER_ENDPOINT)
    heartbeat_route_pattern = url_path_join(base_url, url_path, HEARTBEAT_ENDPOINT)
    provider = ProxiedServersProvider()
    handlers = [(heartbeat_route_pattern, HeartbeatHandler),
                (servers_route_pattern, ProxiedServersHandler, {'provider': provider}),
                (url_route_pattern, RouteHandler)]
    web_app.add_handlers(host_pattern, handlers)
