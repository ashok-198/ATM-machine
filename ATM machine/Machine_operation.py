import sys, datetime
from json import dump, load ; from time import sleep
from memory_profiler import profile

#@profile
#____________________________________________________________________________       Write machine data 
def mac_da_op(super_pass_1, denomintion, status = 'Running', call_from = 'client_withdraw'):    # if call_from = 'client_withdraw'(or) 'admin' => super_pass_1 = machine_available_balance 
                                                                                                # else call_from == 'client_deposit' => super_pass_1 = deposit amount
    with open('machine_data.json', 'r') as file:
        machine_data = load(file)
    
    if super_pass_1 == 0:
        machine_data[0]['machine_status'] = 'Out of cash'
    else:
        machine_data[0]['machine_status'] = status

    machine_data_denominatin = machine_data[1]['cash_denomination']

    if call_from =='client_withdraw':
        machine_data[0]['machine_available_balance'] = super_pass_1
        machine_data_denominatin['500'], machine_data_denominatin['200'], machine_data_denominatin['100'] = denomintion[0], denomintion[1], denomintion[2]
    
    elif call_from == 'client_deposit':
        machine_data[0]['machine_available_balance'] += super_pass_1

        for_500, for_200, for_100 = int((super_pass_1 * (3/6) ) // 500), int((super_pass_1 * (2/6) ) // 200), int((super_pass_1 * (1/6) ) // 100)

        machine_data_denominatin['500'] += for_500
        machine_data_denominatin['200'] += for_200
        machine_data_denominatin['100'] += for_100

        gathered_sum = (for_500 * 500) + (for_200 * 200) + (for_100 * 100)

    elif call_from == 'admin':
        machine_data[0]['machine_available_balance'] = super_pass_1

        machine_data_denominatin['500'] = int((super_pass_1 * (3/6)) // 500)
        machine_data_denominatin['200'] = int((super_pass_1 * (2/6)) // 200)
        machine_data_denominatin['100'] = int((super_pass_1 * (1/6)) // 100)

        gathered_sum = (machine_data_denominatin['500'] * 500) + (machine_data_denominatin['200'] * 200) + (machine_data_denominatin['100'] * 100)
        
    if call_from in ('admin','client_deposit'):
        difference = super_pass_1 - gathered_sum

        if difference > super_pass_1:
            if difference % 100 == 0:
                machine_data_denominatin['100'] -= int(difference // 100)   
            elif difference % 200 == 0:
                machine_data_denominatin['200'] -= int(difference // 200 )

        if difference < super_pass_1:
            if difference % 100 == 0:
                machine_data_denominatin['100'] += int(difference // 100)    
            elif difference % 200 == 0:
                machine_data_denominatin['200'] += int(difference // 200)

    with open('machine_data.json', 'w') as file:
        dump(machine_data, file, indent=4)
#____________________________________________________________________________


#____________________________________________________________________________       Read machine data
def mac_da_read():
    with open('machine_data.json','r') as file:
        machine_data = load(file)
    return machine_data
#____________________________________________________________________________


#____________________________________________________________________________       Write client data
def cli_da_op(id, super_pass_1, super_pass_2, request = 'client_withdraw' ): # if request = 'client_withdraw' ( super_pass_1 = client_available_balance, super_pass_2 = wrong_PIN_limit ) ; 
                                                                             # elif ( super_pass_1 = new client_PIN , super_pass_2 = wrong_PIN_limit )
                                                                             # elif ( super_pass_1 = deposit_amount , super_pass_2 = None )
    
    with open('client_data.json', 'r') as file:
        client_data = load(file)

    if request == 'client_withdarw':
        client_data[id]["client_available_balance"] = super_pass_1
        client_data[id]["wrong_PIN_limit"] = super_pass_2

    elif request == 'client_PIN_change': 
        client_data[id]["client_PIN"] = super_pass_1
        client_data[id]["wrong_PIN_limit"] = super_pass_2

    elif request == 'client_deposit':
        client_data[id]["client_available_balance"] += super_pass_1


    with open('client_data.json', 'w') as file:
        dump(client_data, file, indent=4)
#____________________________________________________________________________


#____________________________________________________________________________       Read client data
def cli_da_read():
    with open('client_data.json','r') as file:
        client_data = load(file)
    return client_data
#____________________________________________________________________________


#____________________________________________________________________________       Read admin credential data
def admin_da_read():
    with open('admin_data.json','r') as file:
        admin_data = load(file)
    return admin_data
#____________________________________________________________________________


#____________________________________________________________________________       Admin login (_need Admin credential_)
def admin_login():
    try:
        admin_id_given= input('\nEnter Admin ID: ')
        admin_password = int(input('Enter Admin password: '))

        admin_data = admin_da_read()

        for admin in admin_data:

            if admin['admin_id'] == admin_id_given:
                
                if admin['key'] == admin_password:
                    admin_dashboard()

                else:
                    print('\n\t  **  Invalid password  **  ')
                    sleep(2.2)
                    initial_page()

        else:
            print('\n\t  **  Invalid Admin ID  **  \n')
            sleep(2.2)
            initial_page()
    except ValueError :
        print('\n\t  **  Invalid Credentials  **  \n')
#____________________________________________________________________________


#____________________________________________________________________________       Admin dashboard (__after passing through [ def admin_login() ]__)
def admin_dashboard():
    sleep(1.2)
    flag = True

    while flag:
        machine_data = mac_da_read()

        print(f'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

        Machine Id    : {machine_data[0]['machine_id']} 
      Machine status  : {machine_data[0]['machine_status']} 
    Balance available : {machine_data[0]['machine_available_balance']}
    -----------------------------  
               Denomination\n
               "500"  : {machine_data[1]['cash_denomination']['500']} 
               "200"  : {machine_data[1]['cash_denomination']['200']} 
               "100"  : {machine_data[1]['cash_denomination']['100']} 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~''')
        
        sleep(2)
        action = input(f'\nAction to take (press the index no. then hit enter)  \
            \n\n\t1. Update balance \
            \n\t2. Update status \
            \n\t3. Update both \
            \n\t4. Initial page\n\n==> ')
        
        if action == "1":
            while True:
                update_balance = int(input('Enter the amount to update: '))
                if update_balance % 10000 != 0:
                    print('\n\t  **  Amount should be multiple of "10,000"  **\n')
                    continue
                else:
                    break
            sleep(1.5)
            mac_da_op(update_balance, None, status = machine_data[0]['machine_status'], call_from = 'admin')
        
        elif action == "2":

            update_status = int(input('\nEnter status update \n1. Running \n2. Out of service \n==> '))

            if update_status not in [1,2]:
                print('\n>>  Invalid input exiting  <<')
                sleep(2.2)
                continue

            else:
                update_status = 'Running' if update_status == 1 else 'Out of service' if update_status == 2 else print('\n\t>>  Invalid input  <<')
                print('\n\t>>  Changes made sucessfully.  <<')
                sleep(2.5)
                mac_da_op(machine_data[0]['machine_available_balance'], None, status=update_status, call_from = 'admin')
        
        elif action == "3":

            while True:
                update_balance = int(input('Enter the amount to update: '))
                if update_balance % 10000 != 0:
                    print('\n\t  **  Amount should be multiple of "10,000"  **\n')
                    continue
                else:
                    break

            update_status = int(input('\nEnter status update \n1. Running \n2. Out of service \n==> '))

            if update_status not in [1,2]:
                print('\n>>  Invalid input exiting  <<')
                sleep(2.2)
                continue

            else:
                update_status = 'Running' if update_status == 1 else 'Out of service' if update_status == 2 else print('\n\t>>  Invalid input  <<')
                print('\n\t>>  Changes made sucessfully.  <<')
                sleep(2.5)
                mac_da_op(update_balance, None, status=update_status, call_from = 'admin')

        elif action == "4":
            sleep(1.5)
            initial_page()   
                
        else:
            print('\n>> Invalid input. Please try again')
            sleep(2.2)
            continue   
#____________________________________________________________________________


#____________________________________________________________________________       Withdraw condition check
def withdraw_condition(id):
    
    client_data = cli_da_read()
    machine_data = mac_da_read()
    client_data = client_data[id]

    pin_limit = client_data['wrong_PIN_limit'] > 0

    if not pin_limit:
        print('\nWrong PIN limit reached, please try after 24 hours \n(or) \nVisit Branch office.')
        sleep(2.5)
        initial_page()
    print('\nInput  "00"  to exit')
    while True:
        try:
            amount = int(input('\nPlease enter amount  ==> ₹ '))
            if amount == 0:
                welcome_page()
            pin = int(input('\nPlease enter PIN  ==> '))
            break

        except ValueError:
            print('\n\t    **  Invalid input. Please try again  **  ')
            continue

    pin_check = True if pin == client_data['client_PIN'] else False
    multiple_of_100 = True if amount % 100 == 0 else False
    balance_check = True if amount <= client_data['client_available_balance'] else False
    min_limit_check = True if amount >= client_data['min_limit'] else False
    max_limit_check = True if amount <= client_data['max_limit'] else False
    machine_balance_check = True if amount <= machine_data[0]['machine_available_balance'] else False

    condition_check = all([pin_check, multiple_of_100, balance_check, min_limit_check, max_limit_check, machine_balance_check])



    withdraw(id, amount, client_data, machine_data, condition_check, pin_check, multiple_of_100, balance_check, min_limit_check, max_limit_check, machine_balance_check)
#____________________________________________________________________________


#____________________________________________________________________________       Cash denomination check
def denomination_func(amount):
    machine_data = mac_da_read()

    machine_data = machine_data[1]["cash_denomination"]

    cash_500, cash_200, cash_100 = machine_data["500"], machine_data["200"], machine_data["100"]

    if amount >= 500:

        count_for_500 = int(amount* (3/6)) // 500
        balance = abs(amount - 500 * count_for_500)
        
        count_for_200 = int(balance * (2/3)) // 200
        balance = abs(balance - 200 * count_for_200)

        count_for_100 = int (balance  // 100)

    elif 200 <= amount < 500:
        count_for_500 = 0

        count_for_200 = int(amount * (2/3)) // 200
        balance = abs(amount - 200 * count_for_200)

        count_for_100 = balance // 100

    elif amount < 200:
        count_for_500 = 0
        count_for_200 = 0  
        count_for_100 = amount // 100

    if cash_500 >= count_for_500 and cash_200 >= count_for_200 and cash_100 >= count_for_100:
        machine_cash = (cash_500 - count_for_500), (cash_200 - count_for_200), (cash_100 - count_for_100)
        denomination_count = count_for_500, count_for_200, count_for_100
        print(denomination_count)
        return [ True,  machine_cash, denomination_count ]

    else:
        return [ False ]
#____________________________________________________________________________


#____________________________________________________________________________       Withdraw Dashboard
def withdraw (id, amount, client_data, machine_data, condition_check, pin_check, multiple_of_100, balance_check, min_limit_check, max_limit_check, machine_balance_check):
    
    returning_from = denomination_func(amount)
    denomination_check = returning_from[0]

    if returning_from[0]:
        curr_cash_500, curr_cash_200, curr_cash_100 = returning_from[1][0], returning_from[1][1], returning_from[1][2]
        count_500, count_200, count_100 = returning_from[2][0], returning_from[2][1], returning_from[2][2]

        denomination_update = curr_cash_500, curr_cash_200, curr_cash_100 

    condition_check = condition_check and returning_from [0]

    flag = True
    while flag:

        if condition_check  :

            print('\n\n\t__________💲💲💲💲💲💲💲__________')
            print('\n\t\tPlease collect your amount\n')
            print(f'500 notes_> {count_500} \n200 notes_> {count_200} \n100 notes_> {count_100}\n')
            print('\t__________💲💲💲💲💲💲💲__________\n\n')
            sleep(2.5)
            
            cli_avail_balan = client_data['client_available_balance'] - amount
            mac_avail_balan = machine_data[0]['machine_available_balance'] - amount

            cli_da_op(id, cli_avail_balan, client_data['wrong_PIN_limit'])              # Function call after sucessful withdraw made
            mac_da_op(mac_avail_balan, denomination_update)  
            mini_statement(id, amount, call_from= 'client_withdraw')
            flag = False 

            sleep(1.5)
            balance_query = input('Press "1" to display balance \nPress "2" to cancel \n\n==> ')

            if balance_query == '1':
                print(f'\nCurrent available balance is \n\n>>>  ₹ {cli_avail_balan}/.  <<<\n')
                sleep(2.5)
                sys.exit('\n________  Thank you for banking with us.  ________\n')

            else:
                print('\n________  Thank you for banking with us.  ________\n')
                sleep(2)
                sys.exit()

        else:

            if not pin_check:
                print('\nWrong PIN, please try again\n')
                client_data['wrong_PIN_limit'] -= 1
                cli_da_op(id, client_data['client_available_balance'], client_data['wrong_PIN_limit'])
            
            elif not multiple_of_100:
                print('\nAmount should be multiple of "100", try again\n')

            elif not balance_check:
                print('\nAmount not available in your account, try lower amount\n')

            elif not min_limit_check:
                print('\nMinimun limit is "100". Try higher amount\n')

            elif not max_limit_check:
                print('\nMaximum limit is "50,000". Try lower amount\n')

            elif not machine_balance_check:
                print(f'\nAvailable machine balance {machine_data[0]['machine_available_balance']}, try lower amount\n')

            elif not denomination_check:
                print('\nCan not dispense this amount, try other amount\n')

            withdraw_condition(id)
            sleep(2)     
#____________________________________________________________________________


#____________________________________________________________________________       Balance option
def balance(id):
    client_data = cli_da_read()[id]
    pin_limit = client_data['wrong_PIN_limit'] > 0

    if not pin_limit:
        print('\nWrong PIN limit reached, please try after 24 hours \n(or) \nVisit Branch office.\n')
        sleep(2.5)
        initial_page()
    
    else:
        while True:
            try:
                Pin = int(input('\nPlease enter PIN \n==> '))
                break
            except ValueError:
                print('\n\t    **  Invalid input. Please try again  **  ')
                continue

        if Pin == client_data['client_PIN'] :
            print(f'\nCurrent available balance is \n\n>>>  ₹ {client_data['client_available_balance']}.  <<<\n')
            sleep(3.1)
            

        else:
            print('\nWrong PIN, please try again\n')
            client_data['wrong_PIN_limit'] -= 1
            cli_da_op(id, client_data['client_available_balance'], client_data['wrong_PIN_limit'])
            balance(id)
#____________________________________________________________________________


#____________________________________________________________________________       Deposit option
def deposit(id):
    
    while True:
        print(f'\n\t **  Please insert your cash into the deposit box.  **\n\n press "00" to cancel.')
        try:
            deposit_amount = int(input('\n  ==> ₹ '))
            if deposit_amount == 00:
                print(f'\n\t  **  Process cancelled. Exiting  **')
                sleep(2.5)
                break
            elif deposit_amount < 100 or deposit_amount % 100 != 0:
                print(f'\n  **  Minimun amount allowed is > ₹ 100 < \nand multiple of ₹ 100 ')
                sleep(2.5)
                continue
            else:
                print(f'\n **  Your placed amount is >>>  ₹ {deposit_amount}  <<<')
                sleep(2) 
                get = int(input('\n\nPress "99" to deposit (or) \npress "00" to cancel\n\n  ==> '))

                if get == 99:

                    mac_da_op(deposit_amount, None, call_from = 'client_deposit')           # Function call after sucessful withdraw made
                    cli_da_op(id, deposit_amount, None, request = 'client_deposit' )
                    mini_statement(id, deposit_amount, call_from= 'client_deposit')

                    print(f'\n\t\t  **  Deposit sucessful.  **')
                    sleep(3.5)
                    break

                elif get == 00:
                    print(f'\n\t  **  Process cancelled. Exiting  **')
                    sleep(2.2)
                    continue

                else:
                    raise ValueError
                
        except ValueError:
            print(f'\n\t  **  This is not valid. Please try again')
            sleep(2.2)
            continue
#____________________________________________________________________________


#____________________________________________________________________________       Change PIN
def change_PIN(id):

    client_data = cli_da_read()
    flag = True
    while flag:
        try:
            pin_limit = client_data[id]['wrong_PIN_limit'] > 0

            if not pin_limit:
                print('\nWrong PIN limit reached, please try after 24 hours \n(or) \nVisit Branch office.')
                sleep(3)
                cli_da_op(id, client_data[id]['client_available_balance'], client_data[id]['wrong_PIN_limit'])
                initial_page()

        
            old_PIN = int(input('\nEnter old PIN  ==> ').strip())

            if old_PIN != client_data[id]['client_PIN']:
                print('\n\t  **  Wrong PIN, please try again  **  ')
                client_data[id]['wrong_PIN_limit'] -= 1
                sleep(1.5)
                continue

            new_PIN = (input('\nEnter new PIN  ==> ').strip())

            if len(new_PIN) != 4:
                print('\n ** Should be minimum "4" charecter \n  **  Should be numerical  **\n')
                sleep(1.5)
                continue

            else :
                client_data[id]['client_PIN'] = int(new_PIN )
                cli_da_op(id, client_data[id]['client_PIN'], client_data[id]['wrong_PIN_limit'], request = 'PIN_change')
                sleep(1)
                print('\n\t\t  ****   PIN changed sucesfully.   ****  ')
                sleep(3)
                flag = False
        except ValueError:
            print('\n\t  **  Not valid input, try again  **')

    initial_page ()
#____________________________________________________________________________


#____________________________________________________________________________       Mini statement
def mini_statement(id, amount, call_from = 'client_mini_statement'):

    with open ('transactions_book.json', 'r') as file:
        mini_statements = load(file)
    mini_statement = mini_statements[id]
    with open ('client_data.json', 'r') as file:
        data = load(file)
        client_balance = data[id]['client_available_balance']


    if call_from == 'client_mini_statement':
        if len(mini_statement) !=0:
            print(f'\n\t  **  Your last 5 transactions are below  **\n')
            sleep(1)
            for ele in mini_statement:
                print(f'{ele}')
                sleep(1.2)
            print(f'\nBalance :>___₹  {client_balance}') 
            sleep(3.5)
            return
        else:
            print(f'\n\t  **  Your last 5 transactions are below  **\n')
            print(f'\n\t           **  No data available  **\n')
            sleep(3)
            return


    elif call_from in ('client_deposit', 'client_withdraw'):
        current_DateTime = datetime.datetime.now().strftime("%d-%m-%Y__%H:%M:%S")

        if len(mini_statement) >= 5:
            mini_statement.pop()

        if call_from == 'client_withdraw':
            action = 'Withdraw'
            update = f'{current_DateTime}______{action}___₹ -{amount}'
            mini_statement.insert(0,update)
                
        elif call_from == 'client_deposit':
            action = 'Deposit'
            update = f'{current_DateTime}______{action}.___₹ +{amount}'
            mini_statement.insert(0,update)  

        mini_statements[id] = mini_statement       


        with open ('transactions_book.json', 'w') as file:
            dump(mini_statements, file, indent=4)
    sleep(2.5)
#____________________________________________________________________________


#____________________________________________________________________________       Transfer
def transfer():
    print('\n   **  This service is currently unavailable  **  ')
#____________________________________________________________________________

#____________________________________________________________________________       Language option
def language_opt(language = 'English'):
    print(f'  **  Currently supported language is {language} \nLanguage sucessfully changed to {language}  **')
    sleep(2.5)
#____________________________________________________________________________


#____________________________________________________________________________       >>>__Initial Page__<<<
def initial_page ():

    id = input('\n Plese insert your card (or) enter client ID and press enter \n\nInput "0" to exit \n\n==> ')
    
    
    client_data = cli_da_read()

    if id == '0':
        print('\n    ________  Thank you for banking with us.  ________\n')   
        sleep(2)
        sys.exit() 

    elif id == 'admin':
        admin_login()

    elif id in client_data:
        print(f'''\n\t\t          Welcome.     
                       {client_data[id]['client_name'].title()}  ''')
        sleep(1.5)
        flag = True
        while flag:

            try:
                request = int(input(f'''
                      ________________         
                      Service required
                                

                Press index no. and hit enter
                                                
          1. Withdrawal           2. Balance check 
                    
          3. Deposit              4. Change PIN 
            
          5. Mini statement       6. Change language

          7. Transfer             8. Exit
                                
            ==> '''))
                print()
            
                if request == 0:
                    print('\n\t     ____________  Exiting.  ____________        \n')
                    sleep(2.5)
                    sys.exit()

                elif request == 1:
                    sleep(1)
                    withdraw_condition(id)

                elif request == 2:
                    sleep(1)
                    balance(id)

                elif request == 3:
                    sleep(1)
                    deposit(id)

                elif request == 4:
                    sleep(1)
                    change_PIN(id)

                elif request == 5:
                    sleep(1)
                    mini_statement(id, None)
                
                elif request == 6:
                    sleep(1)
                    language_opt()

                elif request == 7:
                    sleep(1)
                    transfer(id)
                
                elif request == 8:
                    print('\n      ________  Thank you for banking with us.  ________\n')
                    sleep(2.2)
                    sys.exit()

            except ValueError :
                print('\n\t  **  Invalid input. Please select from given option  **  ')

    else:
        print('\n-------  Sorry, can not procces the card.  -------\n')
        sleep(2.5)
        print('\n________  Thank you for banking with us.  ________\n')   
        sleep(2)
        sys.exit()  
#____________________________________________________________________________


#____________________________________________________________________________       >>>__Welcome Page__<<<
def welcome_page():
    machine_data = mac_da_read()

    if machine_data[0]['machine_status'] == "Out of service":
        print('\n\t\t\033[1;32mWelcome to Dubakoor Bank\n\033[0m')
        sleep(2.5)
        sys.exit('\t      **  Sorry, out of service  **\n')

    elif machine_data[0]['machine_status'] == "Out of cash" or machine_data[0]['machine_available_balance'] == 0:
        print('\n\t\t\033[1;32mWelcome to Dubakoor Bank\n\033[0m')
        sleep(2.5)
        sys.exit('\t       **  Sorry, out of cash  **\n')

    else: 
        print('\n\t\t\033[1;32mWelcome to Dubakoor Bank\n\033[0m')
        
        initial_page()





