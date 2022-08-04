

from Users import User, Manager, Employee, Customer
from FruitStore_Custom_Error import CommaError, DivisibleBy4Error, TooLargeError
import logging
import mysql.connector
import mysql_config as c
import re

def main():
    logging.basicConfig(filename="fruit_store.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')

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


    # fruits_table = load_table(cursor, "fruits")
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
                    user = Customer(row[2], row[3])
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


                    user = Employee(row[2], row[3])
                elif row[1] == "Manager":

                    while True:
                        try:
                            password = input("\nEnter Manager logon passcode (or 'exit' to quit):\n>>>")
                            
                            if password == "m_pimilbeono":
                                user = Manager(row[2], row[3])
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

    cursor.execute(f"SELECT u_id FROM Users WHERE u_name='{user._name}'")
    for record in cursor:
        userid = record[0]
    print(userid)

    while(True):
        print("\nPlease select which operation you want to perform:")
        print("\t1) Order Fruit")
        print("\t2) View Past Orders")
        print("\t3) Replenish Stock")
        print("\t4) Edit Order")
        print("\t5) Edit User")
        print("\t6) Remove Order")
        print("\t7) Remove User")
        print("\t8) Exit Productivity Log")
        action_type = input(">>> ")

        if action_type == "1":
            order_fruit(cursor, userid)
            cnx.commit()
        elif action_type == "2":
            orders_table = check_orders(cursor, user, userid)
            print(('o_id', 'u_name', 'fruit', 'cost'))
            for record in orders_table:
                print(record)
        elif action_type == "3":
            if type(user) != Manager:
                print("\n\nOperation not authorized, please contact a Manager for assistence")
            else:
                restock(cursor, userid)
                cnx.commit()
        elif action_type == "4":
            if type(user) == Customer:
                print("\n\nOperation not authorized, please contact an Employee for assistence")
            else:
                edit_orders(cursor)
                cnx.commit()
        elif action_type == "5":
            if type(user) != Manager:
                print("\n\nOperation not authorized, please contact a Manager for assistence")
            else:
                edit_user(cursor)
                cnx.commit()
        elif action_type == "6":
            if type(user) != Manager:
                print("\n\nOperation not authorized, please contact a Manager for assistence")
            else:
                remove_order(cursor)
                cnx.commit()
        elif action_type == "7":
            if type(user) != Manager:
                print("\n\nOperation not authorized, please contact a Manager for assistence")
            else:
                remove_user(cursor)
                cnx.commit()
        elif action_type == "8":
            print("\n\nThank you for using the Productivity Log!")
            break
        else:
            print("\n\n***** INVALID INPUT: Please enter 1-8 *****")
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
        row = (record[0], record[1], record[2], record[3])
        
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
        add_user_db = f"INSERT INTO Users (u_type, u_name, discount) VALUES ('{type}', '{name}', .1)"
        user = Customer(name, .1)
    elif type == "Employee":
        while True:
            try:
                password = input("\nEnter Employee creation passcode (or 'exit' to quit):\n>>>")
                
                if password == "e_pimilbeono":
                    add_user_db = f"INSERT INTO Users (u_type, u_name, discount) VALUES ('{type}', '{name}', .15)"
                    user = Employee(name, .15)
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
                    add_user_db = f"INSERT INTO Users (u_type, u_name, discount) VALUES ('{type}', '{name}', .2)"
                    user = Manager(name, .2)
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
    logging.info(f"Added a new user {name}")
    return user

def order_fruit(cursor, user_id) -> None:

    print("\nWhich fruit would you like to order:")
    print("\t1) orange")
    print("\t2) apple")
    print("\t3) grapes")
    print("\t4) pineappple")

    while True:
        try:
            fruit_type = int(input("\nSelect fruit type:\n>>>"))

            if fruit_type > 4:
                raise TooLargeError

        except TooLargeError:
            print("\nPlease input a number between 1 and 4!\n")
        except ValueError as ve:
            print("\nPlease input a number between 1 and 4!\n")
        else:
            break
    
    while True:
        try:
            quantity = int(input("\nHow much would you like:\n>>>"))

            if quantity < 0:
                raise TooLargeError
        except TooLargeError:
            print("\nPlease input a positive number!\n")
        except ValueError as ve:
            print("\nPlease input a number!\n")
        else:
            break

    new_order = f"INSERT INTO orders (u_id, f_id, amount) VALUES ({user_id}, {fruit_type}, {quantity})" 
    cursor.execute(new_order)
    logging.info(f"Added a new order for {user_id}")
    return None

def check_orders(cursor, user, userid) -> list:
    if type(user) == Manager:
        string = ""
    else:
        string = f" WHERE orders.u_id={userid}"

    query = f"WITH t1 AS (SELECT o_id, f_id, amount, discount, u_name FROM orders LEFT JOIN users ON orders.u_id=users.u_id{string}) SELECT o_id, u_name, f_type, ROUND(amount*f_price*(1-discount), 2) as cost FROM t1 LEFT JOIN fruits ON t1.f_id=fruits.f_id"


    cursor.execute(query)
    lst_data = []

    for record in cursor:
        row = (record[0], record[1], record[2], record[3])
        
        lst_data.append(row)
    
    return lst_data
    
def edit_orders(cursor) -> None:
    orders_table = load_table(cursor, "orders")
    i = 0
    print("\n(o_id, u_id, f_id, amount)")
    for record in orders_table:
        print(record)
        i += 1
    
    while True:
        try:
            order_id = int(input("\nSelect order to edit:\n>>>"))

        except ValueError as ve:
            print("\nPlease select a listed index!\n")
        else:
            break
    
    print("\nWhat property needs edited:")
    print("\t1) user")
    print("\t2) fruit")
    print("\t3) amount")

    while True:
        try:
            property = int(input("\nSelect property:\n>>>"))

            if property > 3:
                raise TooLargeError

        except TooLargeError:
            print("\nPlease input a number between 1 and 3!\n")
        except ValueError as ve:
            print("\nPlease input a number between 1 and 3!\n")
        else:
            break
    
    if property == 1:
        column = "u_id"
    elif property == 2:
        column = "f_id"
    else:
        column = "amount"
    
    while True:
        try:
            edit = int(input("\nIndicate new value:\n>>>"))
        except ValueError as ve:
            print("\nPlease input a number between 1 and 3!\n")
        else:
            break

    
    try:
        query = f"UPDATE orders SET {column} = {edit} WHERE o_id={order_id}"
        cursor.execute(query)
        logging.info(f"Updated order {order_id}")
    except mysql.connector.Error as mce:
        print(mce.msg)
        print("UPDATE FAILED")
        return
    except Exception as e:
        print("UPDATE FAILED")
        return


    return None
    

def edit_user(cursor) -> None:
    users_table = load_table(cursor, "users")
    i = 0
    print("\n(u_id, u_type, u_name, discount)")
    for record in users_table:
        print(record)
        i += 1
    
    while True:
        try:
            user_id = int(input("\nSelect user to edit:\n>>>"))

        except ValueError as ve:
            print("\nPlease select a listed index!\n")
        else:
            break
    
    print("\nWhat property needs edited:")
    print("\t1) type")
    print("\t2) name")
    print("\t3) discount")

    while True:
        try:
            property = int(input("\nSelect property:\n>>>"))

            if property > 3:
                raise TooLargeError

        except TooLargeError:
            print("\nPlease input a number between 1 and 3!\n")
        except ValueError as ve:
            print("\nPlease input a number between 1 and 3!\n")
        else:
            break
    
    if property == 1:
        column = "u_type"
        while True:
            try:
                edit = input("\nEnter the new user type (Customer, Employee, Manager):\n>>>")
                check = re.search(r'^Customer$|^Employee$|^Manager$', edit)

                if check == None:
                    raise CommaError
            except CommaError:
                print("Must be one of the specified types!\n")
            else:
                break
        query = f"UPDATE users SET {column} = '{edit}' WHERE u_id={user_id}"
    elif property == 2:
        column = "u_name"

        while True:
            try:
                edit = input("\nEnter the new user name:\n>>>")
                check = re.search(r'\D', edit)

                if check == None:
                    raise CommaError
            except CommaError:
                print("Must have a non-digit in user name!\n")
            else:
                break
        query = f"UPDATE users SET {column} = '{edit}' WHERE u_id={user_id}"

    else:
        column = "discount"

        while True:
            try:
                edit = float(input("\nSet new discount:\n>>>"))

                if edit > 1:
                    raise TooLargeError

            except TooLargeError:
                print("\nPlease input a number between 0 and 1!\n")
            except ValueError as ve:
                print("\nPlease input a number between 0 and 1!\n")
            else:
                break
        query = f"UPDATE users SET {column} = {edit} WHERE u_id={user_id}"
    

        

 
    try:
        
        cursor.execute(query)
        logging.info(f"Updated user {user_id}")
    except mysql.connector.Error as mce:
        print(mce.msg)
        print("UPDATE FAILED")
        return
    except Exception as e:
        print("UPDATE FAILED")
        return

    return None

def restock(cursor, userid) -> None:
    
    for i in range(4):
        fruit_type = i + 1
        cursor.execute(f"SELECT sum(amount) FROM orders WHERE f_id = {fruit_type}")
        for record in cursor:
            amount = record[0]
        print(amount)

        if amount >= 0:
            new_order = f"INSERT INTO orders (u_id, f_id, amount) VALUES ({userid}, {fruit_type}, -100)"
            cursor.execute(new_order)
            print("\nOrdered more of fruit " + str(fruit_type))
            logging.info(f"Restocked for {fruit_type}")
        else: 
            print("\nEnough stock of fruit " + str(fruit_type))

    return None

def remove_order(cursor) -> None:
    orders_table = load_table(cursor, "orders")
    i = 0
    print("\n(o_id, u_id, f_id, amount)")
    for record in orders_table:
        print(record)
        i += 1
    
    while True:
        try:
            order_id = int(input("\nSelect order to remove:\n>>>"))

        except ValueError as ve:
            print("\nPlease select a listed index!\n")
        else:
            break
    
    try:
        query = f"DELETE FROM orders WHERE o_id={order_id}"
        cursor.execute(query)
        logging.info(f"Removed order {order_id}")
    except mysql.connector.Error as mce:
        print(mce.msg)
        print("DELETION FAILED")
        return
    except Exception as e:
        print("DELETION FAILED")
        return

    
def remove_user(cursor) -> None:
    users_table = load_table(cursor, "users")
    i = 0
    print("\n(u_id, u_type, u_name, discount)")
    for record in users_table:
        print(record)
        i += 1
    
    while True:
        try:
            user_id = int(input("\nSelect user to remove:\n>>>"))

        except ValueError as ve:
            print("\nPlease select a listed index!\n")
        else:
            break
    
    try:
        query = f"DELETE FROM users WHERE u_id={user_id}"
        cursor.execute(query)
        logging.info(f"Removed user {user_id}")
    except mysql.connector.Error as mce:
        print(mce.msg)
        print("DELETION FAILED")
        return
    except Exception as e:
        print("DELETION FAILED")
        return



    return None
    
       






if __name__ == "__main__":
    main()