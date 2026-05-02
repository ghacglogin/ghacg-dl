class IllegalDownloadRequestException(Exception):
    def __init__(self, message: str = "Illegal download request"):
        super().__init__(message)

class IllegalRefererException(IllegalDownloadRequestException):
    def __init__(self):
        super().__init__("Illegal referer")

class IllegalUserAgentException(IllegalDownloadRequestException):
    def __init__(self):
        super().__init__("Illegal user agent")

class CookieCheckFailedException(IllegalDownloadRequestException):
    def __init__(self):
        super().__init__("Cookie check failed")
