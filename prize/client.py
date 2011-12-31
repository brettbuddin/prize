import base64
import urllib
import signal
import time
import prize.log as log
from tornado import ioloop
from tornado import httpclient
import simplejson as json

class Client:
    def __init__(self, username, password, track=[], follow=[]):
        self.username           = username
        self.password           = password
        self.track              = track
        self.follow             = follow
        self.callbacks          = []

        self.http_client        = httpclient.AsyncHTTPClient()
        self.io_loop            = ioloop.IOLoop.instance()

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def start(self):
        self.io_loop.start()

    def stop(self, signal, frame):
        self.http_client.close()
        self.io_loop.stop()

    def disconnect(self):
        self.http_client.close()
    
    def connect(self):
        track       = ",".join([urllib.quote(s) for s in self.track])
        follow      = ",".join([urllib.quote(s) for s in self.follow])
        post_data   = "track=%s&follow=%s" % (track, follow)
        signal.signal(signal.SIGINT, self.stop)

        request = httpclient.HTTPRequest(
            'https://stream.twitter.com/1/statuses/filter.json', 
            'POST', 
            {'Authorization': "Basic %s" % self._auth()},
            body=post_data,
            streaming_callback=self._on_chunk,
            request_timeout=None
        )
        
        self.http_client.fetch(request, self._reconnect)

    def _reconnect(self, response):
        log.log("Reconnecting...")
        time.sleep(5)
        self.connect()

    def _auth(self):
        return base64.b64encode("%s:%s" % (self.username, self.password))

    def _on_chunk(self, data):
        try:
            entry = json.loads(data)
        except:
            log.error('Could not parse JSON object.')
            return

        for callback in self.callbacks:
            callback(entry, self.track, self.follow)
