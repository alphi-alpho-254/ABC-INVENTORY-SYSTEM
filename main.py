# importing the database (SQLITE3 for this case ->lightweight)
import sqlite3
# importing the time module 
import time


#----- initialize the database (general table)----
def setup_database():
    conn=sqlite3.connect("inventory.db")
    c =conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS records(
          id INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          quantity INTEGER NOT NULL,
          price INTEGER NOT NULL
          )
""")


# ----users table to store authentication----

    c.execute("""CREATE TABLE IF NOT EXISTS users(
         id INTEGER PRIMARY KEY,
         username TEXT UNIQUE NOT NULL,
         password TEXT NOT NULL,
         role TEXT NOT NULL CHECK(role IN ("Admin","Staff"))
               
         )
""")
    conn.commit()
    conn.close()
    # print("\nTable created succesfully!")

# add item to the database
def add_item():
    conn =sqlite3.connect("inventory.db")
    c = conn.cursor()
    try:

        name =input("Enter the product name: ").lower()
        quantity =int(input("Enter the quantity(KGS): "))
        price =int(input("Enter the price: "))
        c.execute("INSERT INTO records(name,quantity,price) VALUES (?,?,?)",(name,quantity,price))
        conn.commit()
        conn.close()
        print("\nItem addded succesfully!")
    except ValueError:
        print("You have entered a wrong input")



# Function to register a new user
def register_user():
    conn=sqlite3.connect("inventory.db")
    c =conn.cursor()
    print("\n----REGISTER AS NEW USER----")
    username=input("Enter username: ")
    password=input("Enter your password: ")
    role=input("Enter Your Role(ADMIN or STAFF): ").capitalize()
    try:

        c.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)",(username, password ,role))
        conn.commit()
        print("\nWait as the system validates you")
        print("VALIDATING",end="")
        for i in range(5):
            time.sleep(1)
            print(".",end="")

        print("\n----User registerd succesfully----")
    except sqlite3.IntegrityError:
        print("Username already taken.\n Try Again!")

    conn.close()


# Functions to loggin 
def login_user():
    conn=sqlite3.connect("inventory.db")
    c =conn.cursor()
    print("\n....LOG IN ...")
    username=input("Enter Your username: ").strip()
    password =input("Enter password: ").strip()
    c.execute("SELECT role FROM users WHERE username=? AND password=?",(username,password))
    result =c.fetchone()

    conn.close()
    if result:
        print("Loading.",end="")
        for i in range(5):
            time.sleep(1)
            print(".",end="")
        print("\nVALIDATING.",end="")
        for i in range(5):
            time.sleep(1)
            print(".",end="")
        
        print(f"\nLogin succesful! Welcome {username} ({result[0]})\n")
        return result[0]
    else:
        return ""









# view item to the database
def view_item():
    conn=sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM records")
    items=c.fetchall()
    if not items:
        print("No such item in records")

    else:
        print("\n...Inventory List...")
        for item in items:
            print(f"ID: {item[0]}\tName:{item[1]}\tQuantity:{item[2]}\tPrice:{item[3]}")

    conn.close()


# update item to the database
def update_item():
    conn=sqlite3.connect("inventory.db")
    c =conn.cursor()
    item_id =int(input("Enter the ID to update: "))
    new_quantity=int(input("Enter the new quantity: "))
    c.execute("UPDATE records SET quantity= ? WHERE id =?",(new_quantity,item_id))
    conn.commit()
    conn.close()
    print("Item updated succesfully!")


def delete_item():
    conn =sqlite3.connect("inventory.db")
    c=conn.cursor()
    try:

        item_id = int(input("Enter the item ID to Delete: "))
        c.execute("DELETE FROM records WHERE id =?",(item_id,))
        print ("Item deleted ")

        conn.commit()
        conn.close()

    except ValueError:
        print("ID should be a number!!")








def main_menu(role):
    while True:
        print("\n===MAIN MENU===")
        if role =="Admin":
            print("1. Add Item")
            print("2. View_items")
            print("3. Update")
            print("4. Delete ")
            print("5. Generate Report ")
            print("6. Logout ")

        else:
            print("1. View_items")
            print("2. Logout ")
        try:
            choice =int(input("\nEnter choice to proceed(1-6): "))

        except ValueError:
            print("Value error")
            continue

        if role=="Admin":

            if choice ==1:
                add_item()

            elif choice ==2:
                view_item()

            elif choice ==3:
                update_item()

            elif choice==4:
                delete_item()

            elif choice==6:
                print("Logging out.",end="")
                for i in range(5):
                    time.sleep(1)
                    print(".", end="")
                break
                

            else:
                print("Invalid Input!")


        else:
            if choice ==1:
                view_item()

            elif choice==2:
                print("Logging out.....")
                time.sleep(3)
                break
            else:
                print("Invalid input")



def main():
    setup_database()
    
    while True:
        print("\n==ABC COMPANY INVENTORY SYSTEM==")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        try:
            choice=int(input("Enter choice (1-3): "))
        except ValueError:
            print("Wrong input!!")
            continue
        if choice==1:
            register_user()

        elif choice==2:
            role=login_user()
            if role.lower()=="admin":
                main_menu(role)
            elif role.lower()=="staff":
                main_menu(role)
            else:
                print("Invalid username or password.")
            

        elif choice==3:
            
            print("Exiting",end="")
            for i in range(5):
                time.sleep(1)
                print(".",end="")
            print("\nExited")
            break
                

        else:
            print("Invalid Input.Try Again")
try:
    main()  

except KeyboardInterrupt:

    print("Program interupted.")         
