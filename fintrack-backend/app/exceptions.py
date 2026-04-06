class NotExistsError(Exception):
    pass


class CannotDeleteUserWithAccounts(Exception):
    pass


class CannotDeleteAccountWithBalance(Exception):
    pass


class IncorrectPassword(Exception):
    pass


class ForbiddenError(Exception):
    pass


class OnlyTransferCanHaveToAccountId(Exception):
    pass


class TransferNeedsDestinationAccount(Exception):
    pass
