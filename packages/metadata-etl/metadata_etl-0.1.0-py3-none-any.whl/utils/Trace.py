class Trace(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Trace, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def setup(self, verb=None):
        # Initialize and set up the trace instance
        self.verbose = verb if verb is not None else self.verbose if hasattr(self, "verbose") else True
        self.trace = print if self.verbose else lambda *a, **k: None
        return self.trace


def enable_trace(f):
    def wrapper(*args, **kwargs):
        f.__globals__['trace'] = Trace().setup()
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Handle exceptions here, e.g., log or raise the exception
            raise e
    return wrapper
