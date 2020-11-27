def raise_(e):
    """A helper to raise an exception when you can't call raise directly.

    E.g. raising an exception in a lambda function. get(some_key, lambda: _raise(Exception("Some message")))
    """
    raise e
