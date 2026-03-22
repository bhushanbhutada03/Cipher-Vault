import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cipher_vault"
    )
    
def insert_password(website, username, password):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO credentials (website, username, password) VALUES (%s, %s, %s)"
    values = (website, username, password)

    cursor.execute(query, values)
    conn.commit()
    conn.close()


def fetch_by_website(website):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM credentials WHERE website = %s"
    cursor.execute(query, (website,))

    rows = cursor.fetchall()

    conn.close()
    return rows


def fetch_all_passwords():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM credentials")
    rows = cursor.fetchall()

    conn.close()
    return rows


def update_password_db(id, new_password):
    conn = get_connection()
    cursor = conn.cursor()

    query = "UPDATE credentials SET password=%s WHERE id=%s"
    cursor.execute(query, (new_password, id))

    conn.commit()
    conn.close()


def delete_password_db(id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "DELETE FROM credentials WHERE id=%s"
    cursor.execute(query, (id,))

    conn.commit()
    conn.close()