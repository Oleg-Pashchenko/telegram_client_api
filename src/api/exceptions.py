class AuthorizationError(Exception):
    def __init__(self, message="Authorization failed"):
        self.message = message
        super().__init__(self.message)
