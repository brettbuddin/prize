import syslog

def log(message):
    syslog.syslog(message)

def error(message):
    syslog.syslog(syslog.LOG_ERR, message)
