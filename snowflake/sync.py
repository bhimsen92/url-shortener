import threading


def synchronized(func):
    def _synchronized_func(self, *args, **kwargs):
        lock_name = "lock_%s" % func.__name__
        if not hasattr(self, lock_name):
            self.__dict__[lock_name] = threading.Lock()  # one lock per object.
        with self.__dict__[lock_name]:
            return func(self, *args, **kwargs)

    return _synchronized_func
