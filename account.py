from bank import Bank


class Account(Bank):
    def __init__(self):
        super().__init__()

    def deposit(self, balance, amount):
        balance += amount
        return balance

    def withdraw(self, balance, amount):
        if balance >= amount:
            balance -= amount
            return balance

    def check_balance(self, personal_account):
        self.personal_account = personal_account
        return personal_account['balance']

    def send_funds(self, balance, sent_amount):
        if balance >= sent_amount:
            balance -= sent_amount
            return balance

    def receive_funds(self, account_number, balance, received_amount, ):
        self.received_amount = received_amount
        self.account_number = account_number
        balance += received_amount
        return balance




