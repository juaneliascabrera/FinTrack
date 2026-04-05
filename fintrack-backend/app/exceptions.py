class NotExistsError(Exception):
    pass

class CannotDeleteUserWithAccounts(Exception):
    pass

class CannotDeleteAccountWithBalance(Exception):
    pass