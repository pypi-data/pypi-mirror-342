from .user import User
from .balance import Statement, Deposit, Withdraw

class Account:
  def __init__(self, *, number: int, user: User):
    """Creates a Account

    Args:
        number (int): The account number
        user (User): The user to whom the account belongs
    """
    self._balance = 0.0
    self._number = number
    self._AGENCY = "0001"
    self._user = user
    self._statement = Statement()

  @property
  def balance(self) -> float:
    """Get balance of the account

    Returns:
        float: The balance of account
    """
    return self._balance
  
  @property
  def statement(self) -> list[float]:
    """Get Statement of the account

    Returns:
        list[float]: A list with the values of transactions
    """
    return [transaction.value if isinstance(transaction, Deposit) else -transaction.value for transaction in self._statement.transactions]
  
  @classmethod
  def new_account(cls, number: int, user: User) -> "Account":
    """Creates the account and appends the account to the user

    Args:
        number (int): The account number
        user (User): The user to whom the account belongs

    Returns:
        Account: The account created
    """
    return user.add_account(cls(number=number, user=user))

  def deposit(self, value: float) -> bool:
    """Makes a deposit in the account

    Args:
        value (float): The value to be deposited

    Returns:
        bool: Returns True if the deposit worked; otherwise, it returns False
    """
    new_balance, deposit = Deposit(value).record(self)
    
    if new_balance is not None:
      self._balance = new_balance
      self._statement.add_to_statement(deposit)
      return True

    return False

  def withdraw(self, value: float) -> bool:
    """Makes a withdraw in the account

    Args:
        value (float): The value to be withdrew

    Returns:
        bool: Returns True if the withdraw worked; otherwise, it returns False
    """
    new_balance, withdraw = Withdraw(value).record(self)
    if new_balance is not None:
      self._balance = new_balance
      self._statement.add_to_statement(withdraw)
      return True
    
    return False
  
  def string_statement(self) -> str:
    """Returns a string formatted statement to print

    Returns:
        str: The string version of statement
    """
    string = f"Statement for account {self._number} - Agency {self._AGENCY}\n{"".center(48, "-")}\n"
    for line in self._statement.str_transactions:
      string += line + "\n"
    string += f"{"".center(48, "-")}\nCurrent balance: $ {self._balance:29,.2f}\n"

    return string

class CheckingAccount(Account):
  def __init__(self, number: int, user: User, limit=500.0, withdraws_limit=3):
    """Creates a Checking Account

    Args:
      number (int): The account number
      user (User): The user to whom the account belongs
      limit (float, optional): The withdrawal cash amount limit. Defaults to 500.0.
      withdraws_limit (int, optional): The maximum number of withdrawals allowed per account. Defaults to 3.
    """
    super().__init__(number=number, user=user)
    self.limit = limit
    self.withdraws_limit = withdraws_limit
    self.count = 0

  def withdraw(self, value):
    """Makes a withdraw in the account

    Args:
        value (float): The value to be withdrew

    Returns:
        bool: Returns True if the withdraw worked; otherwise, it returns False
    """
    if self.count >= self.withdraws_limit:
      print("@ Transaction limit reached, try again tomorrow!")
    elif value > self.limit:
      print(f"@ Value exceeds the maximum limit of $ {self.limit:.2f} :: $ {value:.2f}")
    else:
      if super().withdraw(value):
        self.count += 1
        return True
      
    return False
