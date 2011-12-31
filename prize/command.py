from prize.client import Client
from prize.worker import Worker
from ConfigParser import ConfigParser
import daemon
import lockfile

class Command:
    def __init__(self, options):
        self.options = options

        self.config = ConfigParser()
        self.config.readfp(open(self.options.config_path))

    def execute(self):
        track  = self.config.get('twitter', 'track').split(',')
        follow = self.config.get('twitter', 'follow').split(',')

        worker = Worker(self.config.get('redis', 'host'), int(self.config.get('redis', 'port')))
        client = Client(self.config.get('twitter', 'username'), self.config.get('twitter', 'password'), track, follow)
        client.add_callback(worker.perform)

        client.connect()
        client.start()

    def run(self):
        if self.options.daemonize:
            context = daemon.DaemonContext(
                pidfile=lockfile.FileLock(self.config.get('prize', 'pid_path'))
            )
            with context:
                self.execute()
        else:
            self.execute()
