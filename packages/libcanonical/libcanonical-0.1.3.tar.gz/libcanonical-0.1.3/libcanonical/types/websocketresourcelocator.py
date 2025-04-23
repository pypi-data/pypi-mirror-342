from .httpresourcelocator import HTTPResourceLocator


class WebSocketResourceLocator(HTTPResourceLocator):
    __module__: str = 'libcanonical.types'
    protocols: set[str] = {'wss', 'ws'}