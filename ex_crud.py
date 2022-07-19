from select import select
import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

### CREATE
def dodaj_pracownika(conn, pracownik):
    sql = '''INSERT INTO pracownicy(imię, nazwisko, zawód)
              VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, pracownik)
    conn.commit()
    return cur.lastrowid
def dodaj_zadanie(conn, zadanie):
    sql = '''INSERT INTO zadania(zadanie_id, opis_zadania, czas_wykonania_w_godz)
              VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, zadanie)
    conn.commit()
    return cur.lastrowid

### READ
def wybierz_wg_parametru(conn, zadanie_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM zadania WHERE zadanie_id=?", (zadanie_id,))
    rows = cur.fetchall()
    return rows

def select_all(conn, table):
    cur = conn.cursor()
    cur.execute(f"SELECT * From {table}")
    rows = cur.fetchall()
    return rows
    
def select_where(conn, table, **query):
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = cur.fetchall()
    return rows

### UPDATE

def update(conn, table, id, **kwargs):
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id, )
    sql = f""" UPDATE {table}
                SET {parameters}
                WHERE id = ?"""
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("OK")
    except sqlite3.OperationalError as e:
        print(e)

###DELETE
def delete_where(conn, table, **kwargs):
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k} = ?")
        values += (v,)
    q = " AND ".join(qs)
    sql = f"DELETE  FROM {table} WHERE {q}"
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")
def delete_all(conn, table):
    sql = f"DELETE FROM {table}"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Deleted")
        


if __name__ == "__main__":
    conn = create_connection("harmonogram_pracy.db")

###dodanie praconika i jego zadania
    pracownik = ("Jan", "Kowalski", "murarz")
    pracownik_id = dodaj_pracownika(conn, pracownik)
    zadanie = (
       pracownik_id,
       "wymurownie jednej kondygnacji",
       80
    )
    zadanie_id = dodaj_zadanie(conn, zadanie)

    print(pracownik_id, zadanie_id)
    conn.commit()

###wyświetl listę pracowników i zadania
    print(select_all(conn, "pracownicy"))
    print(select_all(conn, "zadania"))

###wyświetl zadanie wg id=1
    print(wybierz_wg_parametru(conn, 2))

###wyświetl wg wybranej tabeli i parametru
    print(select_where(conn, "pracownicy", imię="Jan"))
    print("---------")
#aktualizacja wybranego wiersza
    update(conn, "zadania", id=2, opis_zadania="wykonanie stropu monolitycznego" )
    print(wybierz_wg_parametru(conn, 2))


   