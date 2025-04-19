from datetime import date

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .account import Account

from .balance import Transaction

class User:
  def __init__(self, address: str):
    """Creates a User

    Args:
        address (str): The address of the user being created
    """
    self._address = address
    self._accounts = []

  def new_transaction(self, account: "Account", transaction: Transaction) -> tuple | None:
    """Record a new transaction in the account received

    Args:
        account (Account): The account where the transaction occured
        transaction (Transaction): The transaction to be recorded

    Returns:
        tuple|None: If the account exists, it returns a tuple containing the new list of transactions for the account; otherwise, it returns None
    """
    if account in self._accounts:
      return transaction.record(account)
    print(f"@ The account does not belong to the user")

  def add_account(self, account: "Account") -> "Account":
    """Adds a account to the User

    Args:
        account (Account): The account that will be added

    Returns:
        Account: The account added
    """
    self._accounts.append(account)
    return account

class NaturalPerson(User):
  def __init__(self, address: str, identifier: str, name: str, birth_date: date):
    """Creates a natural person User

    Args:
        address (str): The address of the natural person
        identifier (str): The identifier of the user (use personal documents to prevent duplicate users)
        name (str): The name of the natural person
        birth_date (date): The birth date of the user
    """
    super().__init__(address)
    self._identifier = identifier
    self._birth_date = birth_date
    self.name = name