####------------------WORKING VERSION--------------------####
import random
import time
import sys
import sqlite3



# creating a database:
##______________________DB Layer_________________________

db = sqlite3.connect('card.s3db')  # card.s3db
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS card 
(id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER);""")
db.commit()


def insert_record(account):
    with db:
        sql.execute("SELECT * from card WHERE ID = (SELECT MAX(ID) FROM card)")
        id_n = sql.fetchone()
        if id_n == None:
            id_n_n = 1
        else:
            id_n_n = int(id_n[1])
            id_n_n = id_n_n + 1

        sql.execute("INSERT INTO card (id, number, pin, balance) VALUES(?, ?, ?, ?)",
                    (int(id_n_n), str(account.card_no), str(account.pin_no), int(account.balance)))
        db.commit()


def check_if_in_db(account_no):
    with db:
        sql.execute("SELECT * FROM card WHERE number = ?", (account_no,))
        acc_data = sql.fetchone()
        if acc_data == None:
            return '' 
        else:
            return acc_data


def fetch_login(account):
    with db:
        sql.execute("SELECT * FROM card WHERE number = ?", (account.card_no,))
        return_data = sql.fetchone()
        if return_data is not None:
            card_n, pin_n = int(return_data[1]), int(return_data[2])
            if card_n == int(account.card_no) and pin_n == int(account.pin_no):
                return True
            else:
                return False
        else:
            return False
        


            
def add_income(account): 
    with db: 
        sql.execute("UPDATE card set balance = ? where number = ? ", (account.balance, account.card_no))
        db.commit()

def transfer_balance(account, account2, amount_to_transfer):
    
    with db:
       
        sql.execute("SELECT balance FROM card WHERE number = ?", (account2.card_no,))
        balance2 = int(sql.fetchone()[0])
        
        balance1 = account.balance
        balance1 = balance1 - amount_to_transfer 
        balance2 = balance2 + amount_to_transfer
        
        sql.execute("UPDATE card set balance = ? where number = ?", (balance1, account.card_no,  ))
        sql.execute("UPDATE card set balance = ? where number = ?", (balance2, account2.card_no, ))
        
        db.commit()
        
        
        
#def fetch_account_data(account):   


def delete_account(account): 
    with db:
        sql.execute("DELETE FROM card WHERE number = ?", (account.card_no,))
        db.commit()
        

def verify_luhn_value(temp_card_num):
    temp_card_no = [int(x) for x in temp_card_num[::-1]]
    sum1 = sum(temp_card_no[0::2])
    sum2 = sum([(z*2)%10 + (z*2)//10 if z>=5 else z*2 for z in temp_card_no[1::2]])
    sum_final = sum1 + sum2 
    sum_final = str(sum_final)
    if sum_final[-1] == '0':
        return True
    else:
        return False

def fetch_balance(account): 
    with db:
        sql.execute("SELECT * FROM card where number = ?", (account.card_no,))
        balance_n = sql.fetchone()
        return balance_n


##____________________End - DB Layer

##_____________________Record - class

class Account():
    

    def __init__(self, card_no, pin_no, balance):
        self.card_no = card_no
        self.pin_no = pin_no
        self.balance = balance

            
    def create_account(self):
        def generate_account_no():
            while True:
                account_no = ''
                temp_list = []
                random.seed(time.process_time())
                temp_list.append([random.randint(0, 9) for x in range(9)])
                temp_no = [4, 0, 0, 0, 0, 0] + (temp_list[0])
                temp_sum_sum = [(z * 2) % 10 + (z * 2) // 10 if z >= 5 else z * 2 for z in temp_no[0::2]]
                temp_sum_no = [int(x) for x in temp_no[1::2]]
                pre_final_no = sum(temp_sum_sum) + sum(temp_sum_no)
                control_num = (pre_final_no * 9) % 10
                account_no = ''.join(str(y) for y in temp_no)
                account_no = account_no + str(control_num)
                check_db = check_if_in_db(account_no)
                if account_no not in check_db:
                    return account_no
                    break
                else:
                    continue

        self.card_no = generate_account_no()

    def create_pin(self):
        random.seed(time.process_time())
        temp_pin_no = str(random.randint(0, 9999))
        self.pin_no = temp_pin_no.zfill(4)
        
    
    def account_getter(self): 
        return account.card_no
    
    def account_setter(self, acc_no): 
        self.card_no = acc_no[1]
        self.pin_no = acc_no[2]
        self.balance = int(acc_no[3])
        
#Validating the Luhn algorithm checksum when entering the card number    

    
#Main execution loop:

while True:
    break_loop = False
    print('1. Create an account' + '\n' + '2. Log into account' + '\n' + ''+'0. Exit')
    choice = int(input('Enter number'))
    #Create a card
    if choice == 1:
        account = Account(card_no=None, pin_no=None, balance=0)
        account.create_account()
        account.create_pin()
        print('Your card has been created')
        print('Your card number:')
        print(account.card_no)
        print('Your card PIN:')
        print(account.pin_no)
        
        insert_record(account)
    #Log into the account: 
    if choice == 2:
        account = Account(card_no=input('Enter your card number: '), pin_no=input('Enter your PIN: '), balance=0)
        account_data = fetch_login(account)
        print(account_data)
        if account_data == True:
            print('You have successfully logged in!')
            while True:
                print('1. Balance')
                print('2. Add income')
                print('3. Do transfer')
                print('4. Close account')
                print('5. Log out')
                print('0. Exit')
                login_options = int(input('Enter a number: '))
                if login_options==1:
                    account.balance = int(fetch_balance(account)[3])
                    print('Balance: ', account.balance)
                    print(account.card_no)
                    continue
                if login_options==2:
                    account.balance = int(input('Enter income: '))
                    add_income(account)
                    print('Income was added!')
                    continue
                if login_options==3:
                    temp_card_num = input('Enter your card number: ')
                    luhn_checksum = verify_luhn_value(temp_card_num) 
                    if luhn_checksum == False: 
                        print('Probably you made a mistake in the card number. Please try again!')
                        continue
                    else: 
                        check_card_exists = check_if_in_db(temp_card_num)
                        if check_card_exists[1] != temp_card_num: 
                            print('Such a card does not exist')
                            continue
                        else:
                            if account.card_no == temp_card_num: 
                                print("You can't transfer money to the same account!")
                                continue
                            else:
                                current_balance = int(fetch_balance(account)[3])
                                account2 = Account(card_no = temp_card_num, pin_no = None, balance = 0)
                                acc2_data = fetch_balance(account2)
                                account2.account_setter(acc2_data)
                                print(account2.__dict__)
                                print(account.__dict__)
                                amount_to_transfer = int(input('Enter the amount to be transferred:'))
                                if amount_to_transfer > current_balance: 
                                    print('Not enough money!')
                                    continue
                                else: 
                                    transfer_balance(account, account2, amount_to_transfer)
                                    print(account.balance, account2.balance)
                                    continue
                            
                        
                if login_options==4: 
                    delete_account(account)
                    print('The account has been closed!')
                    break
                if login_options==5:
                    print('You have successfully logged out!')
                    break
                if login_options==0:
                    print('Bye!')
                    break_loop = True
                    break
            else:
                print('Wrong card number or PIN!')
                continue
    if choice == 0 or break_loop == True:
        print('Bye!')
        break
        
        