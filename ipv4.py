def patch():
    import socket

    def getaddrinfo_wrapper(
            host, port, family=0, socktype=0, proto=0, flags=0
    ):
        return orig_getaddrinfo(
            host, port, socket.AF_INET, socktype, proto, flags
        )

    orig_getaddrinfo = socket.getaddrinfo
    socket.getaddrinfo = getaddrinfo_wrapper
