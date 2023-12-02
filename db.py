import mysql.connector

# remote = mysql.connector.connect(
#     host="192.168.56.101",  
#     user="goym",  
#     password="your_password",
#     database="TermDB", 
#     port=4567  
# )

# cur = remote.cursor()

# while True:
#     command = input("Enter Query")
    
#     try:
#         cur.execute(command)
#         result = cur.fetchall()
        
#         for row in result:
#             print(row)
            
#     except KeyboardInterrupt:
#         print("Exiting...")
#         break

# remote.close()

def check_login_credentials(id, pw):
    try:
        remote = mysql.connector.connect(
            host="192.168.56.101",
            user="goym",
            password="your_password",
            database="TermDB",
            port=4567
        )

        cur = remote.cursor()

        query = f"SELECT * FROM User WHERE uid = '{id}' AND pw = '{pw}'"
        cur.execute(query)
        result = cur.fetchall()

        remote.close()

        return len(result) > 0

    except Exception as e:
        print(f"Error: {e}")
        return False
    
def register_new_user(id, pw, email, name):
    try:
        remote = mysql.connector.connect(
            host="192.168.56.101",
            user="goym",
            password="your_password",
            database="TermDB",
            port=4567
        )

        cur = remote.cursor()

        check_query = f"SELECT uid FROM User WHERE uid = '{id}'"
        cur.execute(check_query)
        existing_user = cur.fetchone()

        if existing_user:
            return False
        else:
            insert_query = f"INSERT INTO User (uid, pw, email, user_name) VALUES ('{id}', '{pw}', '{email}', '{name}')"
            cur.execute(insert_query)
            remote.commit()
            return True

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        cur.close()
        remote.close()
