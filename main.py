from account import *
import re

bank = Bank()
account = Account()
personal_account = {}


def run():
    while True:
        print("""
« Welcome to MBank Digital »
*****************************
* 1. Create an account      *
* 2. Log in to your account *
* 3. View account details   *
* 4. Balance                *
* 5. Deposit money          *
* 6. Withdraw money         *
* 7. Transfer money         *
* 8. Log out                *
* 9. Quite                  *
*****************************
               """)

        while True:
            try:
                choice = int(input("Enter Your Choice: "))
                break
            except ValueError:
                print('Invalid Choice.Try again.')

        if choice == 1:
            while True:
                first_name = input("Enter your first name: ").lower()
                last_name = input("Enter your last name: ").lower()
                if first_name.isalpha() and last_name.isalpha():
                    break
                else:
                    print("Enter valid name")

            while True:
                nic = input("Enter your NIC number: ")
                temporary_nic_holder = []
                for i in bank.accounts.keys():  # First loop through keys
                    for j in [bank.accounts[i]['nic']]:  # Now loop through values in nested dictionary
                        temporary_nic_holder.append(j)
                if nic in temporary_nic_holder:
                    print('This NIC number is already used.')
                elif not len(nic) <= 12 and (not re.match('[0-9]+V', nic) or not re.match('[0-9]', nic)):
                    print('This NIC is invalid. Please try again.')
                else:
                    break

            while True:
                email = input("Enter your email address: ")
                temporary_email_holder = []
                for i in bank.accounts.keys():  # First loop through keys
                    for j in [bank.accounts[i]['email']]:  # Now loop through values in nested dictionary
                        temporary_email_holder.append(j)
                if email in temporary_email_holder:
                    print("Email already registered")
                elif not re.match(r'^[a-zA-Z0-9_.+-]+@+[a-zA-Z]+.com', email):  # Check the default email format
                    print("Invalid Email address")
                else:
                    break

            while True:
                password = input("Enter your password: ")
                if not len(password) >= 8 or not len(re.findall('[0-9]', password)) >= 1:  # password validation
                    print(
                        'Your password must contain 8 characters, at least two numbers and least one special character.')
                else:
                    password = bank.encrypt_password(password.encode())  # Encode the password
                    break

            account_details = (bank.create_account(first_name=first_name, last_name=last_name, nic=nic, email=email))
            account_number = bank.generate_account_number(1000)

            bank.accounts.update({account_number: account_details})  # Update the bank account dictionary

            bank.accounts_credentials.update(
                {account_number: password})  # Update user login credential --> Account number and encrypted password



            print(f"""Hello, {first_name.capitalize()} {last_name.capitalize()}. Your account successfully created ✅
⏩ Your account number: {account_number} 
Please log into your account using account number and password. Thank you.
                  """)

        if choice == 2:
            while True:
                personal_account_number = int(input("Enter your account number: "))
                personal_password = input("Enter your password: ").encode()
                if len(personal_account) == 0 and bank.decrypt_password(bank.accounts_credentials[personal_account_number]) == personal_password:
                    personal_account.update(bank.login_account(account_number=personal_account_number, password=personal_password))
                    personal_account.update(account_number=personal_account_number)
                    print('You logged successfully!')
                    break
                elif len(personal_account) >= 1:
                    print('Your are already logged in. Please log out to log in again.')
                    break
                else:
                    print('Invalid credentials. Please try again.')
                    break

        if choice == 3:
            if not len(personal_account) == 0:
                first_name, last_name, nic, email, balance, account_number = bank.view_account_details(personal_account)
                print(f'--------------------------'
                      f'\nName: {first_name.capitalize()} {last_name.capitalize()}'
                      f'\nAccount number: {account_number}'
                      f'\nNic: {nic}'
                      f'\nEmail: {email}'
                      f'\nBalance:Rs. {balance}'
                      f'\n--------------------------')
            else:
                print('Please login to your account first.')

        if choice == 4:
            if not len(personal_account) == 0:
                print(f'Account balance:Rs. {account.check_balance(personal_account)}')
            else:
                print('Please login to your account first.')

        if choice == 5:
            if not len(personal_account) == 0:
                deposit_amount = int(input('Deposit amount:Rs. '))
                personal_account.update(balance=account.deposit(personal_account['balance'], deposit_amount))
                print(personal_account)
            else:
                print('Please login to your account first.')

        if choice == 6:
            if not len(personal_account) == 0:
                withdraw_amount = int(input('Withdraw amount:Rs. '))
                personal_account.update(balance=account.withdraw(personal_account['balance'], withdraw_amount))
                print(personal_account)

        if choice == 7:
            while True:
                if not len(personal_account) == 0:
                    send_amount = int(input('Transfer amount:Rs. '))
                    receiver_account_number = int(input('Receiver account number: '))
                    personal_account.update(balance=(account.send_funds(personal_account['balance'], send_amount)))
                    bank.accounts[personal_account.get('account_number')].update(personal_account)
                    print(personal_account)
                    bank.accounts[receiver_account_number].update(balance=(account.receive_funds(receiver_account_number, bank.accounts[receiver_account_number].get('balance'), send_amount)))
                    print(bank.accounts)
                    break
                else:
                    print('Invalid account number. Try again.')

        if choice == 8:
            if len(personal_account) >= 1:
                bank.update_account(personal_account['account_number'], personal_account)  #update the main account before logout
                bank.logout_account(personal_account)
                print(bank.accounts)
                print('You have successfully logged out')
            else:
                print('You are not logged in. Please log in before log out.')

        if choice == 9:
            print('Thank you for using our services. See you soon.')
            break

run()
