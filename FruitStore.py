


from Users import User, Manager, Employee, Customer
from FruitStore_Custom_Error import CommaError, DivisibleBy4Error, TooLargeError
import logging
import mysql.connector
import mysql_config as c
import re

def main():

    try:
        cnx = mysql.connector.connect(user=c.user, password=c.password, host=c.host, database="220711_p0")
        cursor = cnx.cursor()
    except mysql.connector.Error as mce:
        print(mce.msg)
        return
    except Exception as e:
        print("ERROR: Exiting program")
        return

    logging.basicConfig(filename="fruit_store.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')


    fruits_table = load_table(cursor, "fruits")
    users_table = load_table(cursor, "users")

    print("*** Welcome to the Little Jamies Fruit Store ***")

    while True:
        while True:
            try:
                name = input("\nEnter your user name:\n>>>")
                check = re.search(r'\D', name)

                if check == None:
                    raise CommaError
            except CommaError:
                print("Must have a non-digit in user name!\n")
            else:
                break
    
        user = None
        returner = 0
        for row in users_table:
            if name == row[2]:
                if row[1] == "Customer":
                    user = Customer(row[2])
                elif row[1] == "Employee":
                    while True:
                        try:
                            password = input("\nEnter Employee logon passcode (or 'exit' to quit):\n>>>")
                            
                            if password == "e_pimilbeono":
                                user = Manager(name)
                            elif password.lower() == "exit":
                                print("User logon failed")
                            else:
                                raise CommaError

                        except CommaError:
                            print("Invalid passcode!\n")
                        else:
                            break


                    user = Employee(row[2])
                elif row[1] == "Manager":

                    while True:
                        try:
                            password = input("\nEnter Manager logon passcode (or 'exit' to quit):\n>>>")
                            
                            if password == "m_pimilbeono":
                                user = Manager(row[2])
                            elif password.lower() == "exit":
                                print("User logon failed")
                            else:
                                raise CommaError

                        except CommaError:
                            print("Invalid passcode!\n")
                        else:
                            break



                else:
                    raise Exception("INVALID USER TYPE!")
                returner = 1
        
        if returner == 1:
            if user == None:
                pass
            else: 
                print("Returning User")
                break
        else:
            user = create_user(cursor, name)
            if user == None:
                pass
            else :
                print("New User")
                break

    cnx.commit()
    print(user)

    while(True):
        print("\nPlease select which operation you want to perform:")
        print("\t1) Order Fruit")
        print("\t2) View Past Orders")
        print("\t3) Replenish Stock")
        print("\t4) Edit Orders")
        print("\t5) Edit Users")
        print("\t6) Exit Productivity Log")
        action_type = input(">>> ")

        if action_type == "1":
            print("\n\nOperation not implemented")
        elif action_type == "2":
            print("\n\nOperation not implemented")
        elif action_type == "3":
            print("\n\nOperation not implemented")
        elif action_type == "4":
            print("\n\nOperation not implemented")
        elif action_type == "5":
            print("\n\nOperation not implemented")
        elif action_type == "6":
            print("\n\nThank you for using the Productivity Log!")
            break
        else:
            print("\n\n***** INVALID INPUT: Please enter 1-6 *****")
        print("\n\nDirecting back to operation menu....")
    

    cnx.commit()
    cursor.close()
    cnx.close()


def load_table(cursor, table) -> list:
    '''
    This function grabs all data from the specified table in our mySQL server
    Returns a list
    '''
    query = "SELECT * FROM " + table

    cursor.execute(query)
    lst_data = []

    for record in cursor:
        row = (record[0], record[1], record[2])
        
        lst_data.append(row)
    
    return lst_data

def create_user(cursor, name) -> User:

  
    while True:
        try:
            type = input("\nEnter your user type (Customer, Employee, Manager):\n>>>")
            check = re.search(r'^Customer$|^Employee$|^Manager$', type)

            if check == None:
                raise CommaError
        except CommaError:
            print("Must be one of the specified types!\n")
        else:
            break
        
    if type == "Customer":
        add_user_db = f"INSERT INTO Users (u_type, u_name) VALUES ('{type}', '{name}')"
        user = Customer(name)
    elif type == "Employee":
        while True:
            try:
                password = input("\nEnter Employee creation passcode (or 'exit' to quit):\n>>>")
                
                if password == "e_pimilbeono":
                    add_user_db = f"INSERT INTO Users (u_type, u_name) VALUES ('{type}', '{name}')"
                    user = Employee(name)
                elif password.lower() == "exit":
                    print("User creation aborted")
                    return None
                else:
                    raise CommaError
            except CommaError:
                print("Invalid passcode!\n")
            else:
                break
    else:
        while True:
            try:
                password = input("\nEnter Manager creation passcode (or 'exit' to quit):\n>>>")
                
                if password == "m_pimilbeono":
                    add_user_db = f"INSERT INTO Users (u_type, u_name) VALUES ('{type}', '{name}')"
                    user = Manager(name)
                elif password.lower() == "exit":
                    print("User creation aborted")
                    return None
                else:
                    raise CommaError

            except CommaError:
                print("Invalid passcode!\n")
            else:
                break

    print(add_user_db)
    cursor.execute(add_user_db)
    return user






if __name__ == "__main__":
    main()