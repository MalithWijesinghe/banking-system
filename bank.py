from cryptography.fernet import Fernet

class Bank:
    def __init__(self):
        self.accounts = {}  # Store account details of all users
        self.accounts_credentials = {}
        self.balance = 0
        self.first_name = None
        self.last_name = None
        self.nic = None
        self.email = None
        self.password = None
        self.account_number = None
        self.receiver_account = None
        self.transfer_amount = None
        self.personal_account = {}  # This is for temporary dictionary
        self.encryption_key = Fernet.generate_key()
        self.key = Fernet(self.encryption_key)

    def generate_account_number(self, account_number=None):  # Generate account number from given argument value
        self.account_number = account_number
        # Try to use try-exception block for below block of codes.
        if len(self.accounts) == 0:  # Find the dictionary empty or not
            self.accounts.update(
                {account_number: None})  # If empty, add e predefined value that enter as starting account number.
            account_number = max(self.accounts.keys())  # Now increment the value
            account_number += 1
            del self.accounts[self.account_number]  # Finally remove the starting account number
        else:
            account_number = max(self.accounts.keys())
            account_number += 1
        return account_number

    def encrypt_password(self, password):
        self.password = password
        encrypted_password = self.key.encrypt(password)
        return encrypted_password

    def decrypt_password(self, password):
        self.password = password
        decrypted_password = self.key.decrypt(password)
        return decrypted_password

    def create_account(self, first_name, last_name, nic, email, balance=0):  # create and return details as dictionary.
        self.first_name = first_name
        self.last_name = last_name
        self.nic = nic
        self.email = email
        self.balance = balance
        return dict(first_name=first_name, last_name=last_name, nic=nic, email=email,
                    balance=balance)

    def login_account(self, account_number, password):
        self.account_number = account_number
        self.password = password
        if account_number in self.accounts_credentials.keys():
            if password == self.decrypt_password(self.accounts_credentials[account_number]):
                return self.accounts[account_number]

    def view_account_details(self, personal_account):
        self.personal_account = personal_account
        return personal_account.values()

    def update_account(self, account_number, personal_account):
        self.account_number = account_number
        self.personal_account = personal_account
        return self.accounts[account_number].update(personal_account)

    def logout_account(self, personal_account):  # Clear temporary dictionary values
        self.personal_account = personal_account
        personal_account.clear()

    def delete_account(self, account_number, password):
        self.account_number = account_number
        self.password = password
        if account_number in self.accounts:
            if password == self.accounts[account_number]['password']:
                del self.accounts[account_number]

    def transfer_funds(self, account_number, receiver_account, transfer_amount):
        self.account_number = account_number
        self.receiver_account = receiver_account
        self.transfer_amount = transfer_amount
        if receiver_account in self.accounts:
            self.accounts[receiver_account]['balance'] += transfer_amount  # This will add transfer amount to receiver's account.
            return self.accounts[receiver_account]['balance']
