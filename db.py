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

def check_login_User(id, pw):
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

def check_login_Staff(id, pw):
    try:
        remote = mysql.connector.connect(
            host="192.168.56.101",
            user="goym",
            password="your_password",
            database="TermDB",
            port=4567
        )

        cur = remote.cursor()

        query = f"SELECT * FROM Staff WHERE sid = '{id}' AND pw = '{pw}'"
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
        
def register_new_car(id, age, model, seller, distance, price, image):
    try:
        remote = mysql.connector.connect(
            host="192.168.56.101",
            user="goym",
            password="your_password",
            database="TermDB",
            port=4567
        )

        cur = remote.cursor()

        check_query = f"SELECT cid FROM Car WHERE cid = '{id}'"
        cur.execute(check_query)
        existing_user = cur.fetchone()

        if existing_user:
            return False
        else:
            insert_query = f"INSERT INTO Car (cid, age, model, seller, distance, price, image) VALUES ('{id}', '{age}', '{model}', '{seller}', '{distance}', '{price}', '{image}')"
            cur.execute(insert_query)
            remote.commit()
            return True

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        cur.close()
        remote.close()

def delete_car(id):
    try:
        remote = mysql.connector.connect(
            host="192.168.56.101",
            user="goym",
            password="your_password",
            database="TermDB",
            port=4567
        )
        
        cur = remote.cursor()

        check_query = f"SELECT * FROM Car WHERE cid = '{id}'"
        cur.execute(check_query)
        result = cur.fetchone()

        if result:
            delete_query = f"DELETE FROM Car WHERE cid = '{id}'"
            cur.execute(delete_query)
            remote.commit()
            print(f"차량 (CID: {id}) 삭제 성공!")
            return True
        else:
            print(f"차량 (CID: {id})가 존재하지 않습니다.")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        cur.close()
        remote.close()
