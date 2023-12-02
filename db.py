import mysql.connector

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
