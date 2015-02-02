WAMP_ROUTER = "ws://localhost:8080/ws"
WAMP_REALM = "whistiti"
DEBUG = False

try:
    from local_settings import *
except ImportError:
    pass
