# reference:-https://www.geeksforgeeks.org/python-program-to-create-bankaccount-class-with-deposit-withdraw-function/

class bankAccount:
  def __init__(self, owner, balance):
    self.owner = owner
    self.balance = balance
  def deposit(self):
    amount = float(input("Enter amount to be deposited: "))
    self.balance += amount
    print("\n Amount Deposited: ", amount, " and your balance: ", self.balance)
  def withdraw(self):
    amount = float(input("enter amount to be withdrawn: "))
    if self.balance >= amount:
      self.balance -= amount
      print("\n You Withdraw: ", amount)
    else:
      print("Insufficient funds ")
  def dispaly(self):
    print("\n Net Available Balance", self.balance)
a = "a"
b = 10000
s = bankAccount(a, b)
s.deposit()
s.withdraw()
s.dispaly()