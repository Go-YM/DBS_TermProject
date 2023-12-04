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
        
def get_car_data():
    try:
        remote = mysql.connector.connect(
            host="192.168.56.101",
            user="goym",
            password="your_password",
            database="TermDB",
            port=4567
        )

        cur = remote.cursor(dictionary=True)  # Use dictionary cursor

        # Car 테이블의 모든 데이터를 가져옴
        cur.execute("SELECT * FROM Car")
        car_data = cur.fetchall()

        return car_data

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        cur.close()
        remote.close()

        
def get_staff_name(sid):
    try:
        remote = mysql.connector.connect(
            host="192.168.56.101",
            user="goym",
            password="your_password",
            database="TermDB",
            port=4567
        )

        cur = remote.cursor()

        # Staff 테이블에서 sid에 해당하는 staff의 user_name을 가져옴
        cur.execute("SELECT user_name FROM Staff WHERE sid = %s", (sid,))
        staff_name = cur.fetchone()

        return staff_name[0] if staff_name else None

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        cur.close()
        remote.close()

def check_accident(cid):
    try:
        remote = mysql.connector.connect(
            host="192.168.56.101",
            user="goym",
            password="your_password",
            database="TermDB",
            port=4567
        )

        cur = remote.cursor(dictionary=True)

        # 해당 cid의 사고 여부를 확인
        cur.execute("SELECT * FROM Accident WHERE car_id = %s", (cid,))
        accident_data = cur.fetchall()

        if not accident_data:
            return False
        else:
            return True, accident_data

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        cur.close()
        remote.close()
        
def reserve_car(cid, uid):
    try:
        remote = mysql.connector.connect(
            host="192.168.56.101",
            user="goym",
            password="your_password",
            database="TermDB",
            port=4567
        )

        cur = remote.cursor(dictionary=True)

        cur.execute("UPDATE Car SET buyer = %s WHERE cid = %s", (uid, cid))
        remote.commit()

        return True  
    
    except Exception as e:
        print(f"Error: {e}")
        return False 

    finally:
        cur.close()
        remote.close()

import mysql.connector

def show_reserver(sid):
    try:
        remote = mysql.connector.connect(
            host="192.168.56.101",
            user="goym",
            password="your_password",
            database="TermDB",
            port=4567
        )

        cur = remote.cursor(dictionary=True)

        # Staff의 sid와 일치하는 판매자가 Car 테이블에 있는 경우, 해당 판매자가 판매한 차량 중 buyer가 비어있지 않은 경우를 확인하여 해당 buyer의 정보와 Car 정보를 반환
        cur.execute("""
            SELECT U.uid, U.user_name, U.email, C.cid, C.model
            FROM Car C
            JOIN User U ON C.buyer = U.uid
            WHERE C.seller = %s AND C.buyer IS NOT NULL
        """, (sid,))
        
        reservations = cur.fetchall()

        return reservations

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        cur.close()
        remote.close()

