class KwargsOnly:

    def __new__(cls, *args, **kwargs):
        if args:
            raise TypeError("%s only accepts kwargs" % cls)
        inst = super().__new__(cls)
        inst.__kwargs = kwargs
        return inst
