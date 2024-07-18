import sys, json, Machine_operation
from json import load,dump ; from time import sleep
from Machine_operation import welcome_page, initial_page, mac_da_read, cli_da_read, admin_login, admin_dashboard

#_______________________________________________________________________ > Master control <
def master_control():

    flag = True
    while flag:
        sleep(0.5)

        try:
            n = int(input(f'''
                        Input your action   
                    
            1. Machine data             2. Client data 
            3. Admin login              4. Welcome page
            5. Exit
                            
                    000. Credentials Override
                
                    
            ==> '''))
            
        
            if n == 1:
                try:
                    print(f'\n{mac_da_read()}\n') if n == 1 else '\nInvalid entry\n'
                    sleep(2.0)

                except json.JSONDecodeError :
                    print('\n**  Requested dataset is empty  **\n')
                    sleep(2.0)

            elif n == 2:
                try : 
                    print(f'\n{cli_da_read()}\n') if n == 2 else '\nInvalid entry\n'
                    sleep(2.0)

                except json.JSONDecodeError :
                    print('\n**  Requested dataset is empty  **\n')
                    sleep(2.0)

            elif n in [3, 4, 5, 000]:

                if n == 3:
                    admin_login()  
                elif n == 4:
                    welcome_page()  
                elif n == 000: 
                    credentials_override() 
                elif n == 5:
                    flag = False  
                
            else:
                raise ValueError

        except ValueError:
            print('\n\t**  Invalid entry. Try input within the given index  **\n')
            sleep(2)
            continue
    print(f'\n\t**  Exiting  **\n')
    sleep(2.0)
    sys.exit()    
#_______________________________________________________________




#_______________________________________________________________ >>>  B.O  ( Back Office Credentials Override )  <<<
def credentials_override():
    
    with open('BO_credentials.json', 'r') as file:
        BO_cred = load(file)

    master_id = input('Master ID \n==> ')
    password = int(input('Password \n==> '))

    while True:
        if master_id == BO_cred['master_access_id'] and password == BO_cred['key'] :

            print(f'''\n
                _(Back Office Credential Access)_
                            
            ##  Be aware before taking any action's  ##
                ''')
            
            sleep(3)
            flag = True
            while flag:
                try:
                    get = int(input(f'''           
                  Input index no. and hit enter
                        
      1 . Machine data override       2. Client data override

                  3. Admin credential override
                            
      \nPress "0" to exit 
                        
                  ==> '''))
                    if get == 0:
                        master_control()
                    elif get == 1:
                        machine_data_override()
                    elif get == 2:
                        client_data_override(BO_cred)
                    elif get == 3:
                        admin_credentials_override() 
                    else:
                        print('\n\t**  Invalid entry. Try input within the given index  **\n')
                        sleep(1.5)
                        continue

                except ValueError:
                    print('\n\t**  Invalid entry. Try input within the given index  **\n')
                    sleep(2)
                    continue
        else:
            print('\n\t  **  Wrong Credentils  **  \n')
            sleep(2.5)
            continue


#_______________________________________________________________ Machine data override
def machine_data_override():
    admin_dashboard()
    sleep(2.5)



#_______________________________________________________________ Admin credentials override
def admin_credentials_override(): 
    try:
        with open('admin_data.json','r') as file:
            data = load(file)

        existing_id = [ele['admin_id'] for ele in data]

        print(f'\n\t\t     **  Current Data  **  \n')

        for ele in existing_id:
            print(f'{ele}')

    except json.JSONDecodeError:
        data = []
        existing_id = []
        print(f'\n\t\t     **  Current Data  **  \n')
        print(f'"The dataset is empty"\n')

    sleep(2.5)
    flag = True 
    
    while flag:
        get = int(input(f'''           
                  Input index no. and hit enter
                
         1. Add new entry        2. Remove existing entry
                        
                          3. Exit 

            ==> '''))
        
        if get == 1:

            new_id = input('\nEnter Admin ID:  ==> ')
            password = int(input(f'\nEnter password to set for "{new_id}":  ==> '))

            if not new_id in existing_id:
                data.append({'admin_id' : new_id, 'key' : password})

                with open ('admin_data.json', 'w') as file:
                    dump(data, file, indent=4)

                print(f"\n **  Admin ID \"{new_id}\" has been added sucessfully  **.\n")
                sleep(2.5)
                

            else:
                print(f"\n**  Admin ID '{new_id}' already exists. Skipping insertion.  **\n")
                sleep(2.5)
                

        elif get == 2:
            
            remove_id = input('\nEnter Admin ID:  ==> ')

            if not remove_id in existing_id:
                print(f"\n**  Admin ID '{remove_id}' does not exists.  **\n")
                sleep(2.5)
 
            else:
                new_data = [ele for ele in data if ele['admin_id'] != remove_id]

                with open ('admin_data.json', 'w') as file:
                    dump(new_data, file, indent=4)

                print(f"\n **  Admin ID \"{remove_id}\" has been removed sucessfully  **.\n")
                sleep(2.5)

        elif get == 3:
            flag = False

        else:
            print('\nInvalid input\n')


#_______________________________________________________________ Client data override
def client_data_override(BO_cred):   

    with open('client_data.json', 'r') as file:
        client_data = load(file)

    print(f'\n\t\t      **  Current Data  **  \n')

    existing_id = [ele  for ele in client_data]
    
    existing_id_name = [(ele , client_data[ele].get("client_name")) for ele in client_data]

    for ele in existing_id_name:
        print(ele) 

    sleep(3)

    flag = True
    
    while flag:
        try:
            get = int(input(f'''\n          
                      Input index no. and hit enter
                    
            1. Add new entry             2. Remove existing entry
                            
                        3. Modify existing
                            
            0. To exit 

                ==> '''))
            if get not in [0,1,2,3]:
                print('\n  ** Invalid entry. Try again or press "0" to exit.\n')
                sleep(2.5)
                continue

            elif get == 0:
                print(f'\n\t**  Exiting  **\n')
                sleep(0.5)
                flag = False

            elif get == 1:
                client_data_add(client_data, existing_id)
                        
            elif get == 2:
                client_data_remove(client_data, existing_id)

            elif get == 3:
                client_data_modify(BO_cred, client_data)

        except ValueError :
            print(f'\n\t**  Invalid entry  **\n')
            sleep(1.5)
            continue

    sleep(2.5)
    master_control()


#_______________________________________________________________ Add new client data
def client_data_add(client_data, existing_id):
    while True:
        new_id = input('\nEnter new Client ID:  ==> ')
        try:
            if new_id in existing_id:
                print(f'\n\t **  Provided "{new_id}" already exist.')
                continue

            else:
                required = ['name', 'pin', 'balance', 'max. limit']
                new_client_details = []
                for ele in required:
                    get = input(f'Enter "{ele}" to set:> ')
                    new_client_details.append(get)

                client_data[new_id] = {
                                        "client_name": new_client_details[0],
                                        "wrong_PIN_limit": 5,
                                        "client_PIN": int(new_client_details[1]),
                                        "client_available_balance": int(new_client_details[2]),
                                        "min_limit": 100,
                                        "max_limit": int(new_client_details[3])
                                    }
                
                with open('client_data.json','w') as file:
                    dump(client_data, file, indent=4)

                print(f'\n ** New client "{new_id}" with the name "{client_data[new_id]["client_name"]}" and PIN "{client_data[new_id]["client_PIN"]}" has balance of "{client_data[new_id]["client_available_balance"]}" with a max. limit "{client_data[new_id]["max_limit"]}" ** \nhas been sucessfully added to database.\n')
                sleep(3.5)
                client_data_override()
        except ValueError :
            print('\n  **  Inputed data not valid. Please check and try again.  **\n')
            client_data_override()


#_______________________________________________________________ Remove existing client data
def client_data_remove(client_data, existing_id):
        while True:
            remove_id = input('\nEnter Client ID to remove:  ==> ')

            if remove_id not in existing_id :
                if remove_id == '0':
                    break  
                print(f'\n\t **  Provided "{remove_id}" does not exist. Press 0 to exit')
                continue

            else: 
                client_data.pop(remove_id, 'value not found')
                with open('client_data.json', 'w') as file:
                    dump(client_data, file, indent=4)
                print(f'\n ** Client data of "{remove_id}" has sucessfully removed.')
                sleep(3)
                break


#_______________________________________________________________ Modify existing client data
def client_data_modify(BO_cred, client_data):
    while True:
        modify_id = input('\n"0" to exit \nEnter Client ID to modify:  ==> ')
        existing_id = client_data.keys()

        if modify_id not in existing_id:
            if modify_id == '0':
                    break  
            print(f'\n\t **  Provided client ID "{modify_id}" does not exist. Press "0" to exit')
            continue

        else:
            client_data = client_data[modify_id]
            flag = True
            while flag:
                print('\n')   
                for key,data in client_data.items():
                    print(f'{key}_> {data}')
                    sleep(1)
                sleep(2.5)
                
                try:
                    get = int(input(f'''\n
                        Input index no. and hit enter
                        
                1. Modify Name        2. Reset PIN limit
                                
                3. Modify PIN         4. Modify Balance
                                
                5. Modify max. limit    
                                    

        >> Input "0" to exit   |   Input "9" to save changes and exit.  << 
                                
                ==> '''))                 
                 
                    if get not in (1,2,3,4,5,9,0):
                        print('\n  ** Please select a valid input. Press "0" to exit.\n ')
                        sleep(1.5) 
                    elif get in (1,2,3,4,5,0):
                        
                        if get == 0:
                            print('\n\t  **  Exiting  ** ')
                            sleep(1.5)
                            flag = False

                        elif get == 2:
                            client_data['wrong_PIN_limit'] = 5

                        elif get == 3:
                            new_PIN = input('\nSet new PIN  ==> ').strip()                            

                            if len(new_PIN) != 4:
                                client_data['client_PIN'] = client_data['client_PIN'] 
                                print('\n ** Should be minimum "4" charecter \n  **  Should be numerical  **\n')
                                sleep(1.5)
                                continue

                            else :
                                client_data['client_PIN'] = int(new_PIN)
                        
                        elif get == 5:
                            new_limit = input('\nSet new limit  ==> ').strip()                            

                            if len(new_limit) < 5 or int(new_limit) % 10000 != 0:
                                client_data["max_limit"] = client_data["max_limit"] 
                                print('\n ** Should be minimum "₹ 20,000", and multiple of ₹ 10,000. **\n')
                                sleep(2.5)
                            else :
                                client_data["max_limit"] = int(new_limit)

                        elif get == 4:
                            new_balance = input('\nSet new balance  ==> ').strip() 
                            client_data['client_available_balance'] = int(new_balance)

                        elif get == 1:
                            new_name = input('\nSet new name  ==> ').strip() 
                            client_data['client_name'] = new_name

                    elif get == 9:
                            client_data_modify_execution(BO_cred, client_data, modify_id)
                    
                    else:
                        raise ValueError

                except ValueError :
                    print('\n  ** Invalid entry. Press "0" to exit.\n')      
                    sleep(1.5)  
                    

#_______________________________________________________________ Executing modified client data
def client_data_modify_execution(BO_cred, client_data, modify_id):

    print(f'\n\t\t   ** modified data ** \n') 
    print([data for data in client_data.items()])

    flag = True
    while flag:

        confirm = input('\n\t ** Press "11" to confirm (or) "00" to discard and exit to menu  **\n\n ==> ')

        if confirm not in ["11", "00"]:
            print('\n  ** Invalid entry. Press "00" to exit.\n')      
            sleep(1.5)
            continue

        elif confirm == "11":

                get_key = int(input(f'\nEnter override key  ==> '))
                
                m_key = BO_cred["override_key"]
                
                if get_key != m_key:
                    print('\n\t\t  **  Wrong key. Try again  **  \n')
                    
                    continue

                else:
                    modified_data = client_data
                    with open ('client_data.json', 'r') as file :
                        client_data = load(file)
                        client_data[modify_id] = modified_data

                    with open ('client_data.json', 'w') as file :
                        dump(client_data, file, indent=4)
                    print('\n  **  Changes saved sucessfully and exiting  **')
                    sleep(3.5)
                    flag = False
        
        elif confirm == "00":
            print('\n  **  Discarded and exiting  **')
            sleep(1.5)
            flag = False



master_control()