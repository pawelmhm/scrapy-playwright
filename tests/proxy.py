import sys

from twisted.web import proxy, http
from twisted.internet import reactor, endpoints
from twisted.python import log
log.startLogging(sys.stdout)


class ProxyClient(proxy.ProxyClient):
    """Basic Proxy protocol that adds header to request and response.

    """
    header_added = False

    def connectionMade(self):
        # add header to request
        self.headers[b'X-Proxy-Header'] = b'True'
        super().connectionMade()

    def handleHeader(self, key, value):
        # add header to response
        if not self.header_added:
            self.father.responseHeaders.addRawHeader('X-Proxy-Node', 'George')
            self.header_added = True
        super().handleHeader(key, value)


class ProxyClientFactory(proxy.ProxyClientFactory):
    protocol = ProxyClient


class ProxyRequest(proxy.ProxyRequest):
    protocols = {b'http': ProxyClientFactory}


class Proxy(proxy.Proxy):
    requestFactory = ProxyRequest


class ProxyFactory(http.HTTPFactory):
    protocol = Proxy


endpoint = endpoints.TCP4ServerEndpoint(reactor, int(sys.argv[1]))
endpoint.listen(ProxyFactory())
reactor.run()
