import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except Error as e:
       print(e)

   return conn

def execute_sql(conn, sql):
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)

if __name__ == "__main__":

   create_projects_sql = """
   -- pracownicy tabela
   CREATE TABLE IF NOT EXISTS pracownicy (
      id integer PRIMARY KEY,
      imię text NOT NULL,
      nazwisko text,
      zawód text
   );
   """

   create_tasks_sql = """
   -- zadanie tabela
   CREATE TABLE IF NOT EXISTS zadania (
      id integer PRIMARY KEY,
      zadanie_id integer NOT NULL,
      opis_zadania text,
      czas_wykonania_w_godz integer,
      FOREIGN KEY (zadanie_id) REFERENCES pracownicy (id)
   );
   """

   db_file = "harmonogram_pracy.db"

   conn = create_connection(db_file)
   if conn is not None:
       execute_sql(conn, create_projects_sql)
       execute_sql(conn, create_tasks_sql)
       conn.close()