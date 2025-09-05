# Defining Custom Exceptions:

class AuthError(Exception):
    pass

class ValidationError(Exception):
    pass

class DatabaseError(Exception):
    pass