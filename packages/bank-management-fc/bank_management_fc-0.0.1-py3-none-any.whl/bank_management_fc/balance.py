from abc import ABC, abstractmethod
from datetime import datetime

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .account import Account

class Transaction(ABC):
  @abstractmethod
  def record(self, account: "Account"):
    pass
    
class Deposit(Transaction):
  def __init__(self, value: float):
    """Creates a Deposit

    Args:
        value (float): The value to be deposited
    """
    self.value = value

  def record(self, account: "Account") -> tuple:
    """Calculates the new balance value and returns it

    Args:
        account (Account): The account to be calculated

    Returns:
        tuple: Returns the new balance and the object
    """
    new_balance = account.balance + self.value
    return new_balance, self

class Withdraw(Transaction):
  def __init__(self, value: float):
    """Creates a new withdraw

    Args:
        value (float): The value to be withdraw
    """
    self.value = value

  def record(self, account: "Account"):
    """Calculates the new balance value and returns it

    Args:
        account (Account): The account to be calculated

    Returns:
        tuple: Returns the new balance and the object if the withdraws is valid; otherwise returns None and the object
    """
    if account.balance >= self.value:
      new_balance = account.balance - self.value
      return new_balance, self
    print(f"@ Insufficient account balance: $ {account.balance:.2f} :: $ {self.value:.2f}")
    return None, self

class Statement:
  def __init__(self):
    """Creates the new Statement
    """
    self.str_transactions : list[str] = []
    self.transactions : list[Transaction] = []

  def add_to_statement(self, transaction: Transaction):
    """Add the transaction to the statement

    Args:
        transaction (Transaction): The transaction to be added

    Returns:
        bool: Returns True is the transaction is valid; otherwise returns False
    """
    date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


    if isinstance(transaction, Deposit):
      symbol = "+"
      value = transaction.value
    elif isinstance(transaction, Withdraw):
      symbol = "-"
      value = transaction.value
    else:
      return False
    
    if value >= 1000000000:
      self.str_transactions.append(f"{symbol}   $ +999,999,999.99   -   {date_time}")
    else:
      self.str_transactions.append(f"{symbol}   $  {value:14,.2f}   -   {date_time}")
    
    self.transactions.append(transaction)

    return True