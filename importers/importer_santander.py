import json
import sqlite3
from datetime import datetime

# DATABASE = "/mnt/c/Users/DS/OneDrive/Documents/projects/db/my-finance-db.db"
DATABASE = "db/my-finance-db.db"
JSON_FILE = "parsed-jsons/2026-06.json"

class SantanderImporter:
    
    def get_connection():
        return sqlite3.connect(DATABASE)

    def test_connection():
        conn = get_connection()

        cursor = conn.cursor()
        cursor.execute('SELECT SQLITE_VERSION();')
        versao = cursor.fetchone()
        
        print("Conexão bem-sucedida! Versão do SQLite:", versao[0])
        
        conn.close()


    def get_account(conn):

        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM account
            WHERE institution = ?
                AND card = ?
            LIMIT 1
        """, (
            "Santander",
            "5201.2167"
        ))

        account = cursor.fetchone()

        if account:
            return account[0]

        now = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO account
            (
                institution,
                name,
                account_type,
                card,
                created_at,
                updated_at
            )
            VALUES
            (?, ?, ?, ?, ?, ?)
        """, (
            "Santander",
            "Conta Principal",
            "Conta Corrente",
            "5201.2167",
            now,
            now
        ))

        conn.commit()

        return cursor.lastrowid


    def importar():

        conn = get_connection()

        account_id = get_account(conn)

        with open(JSON_FILE, encoding="utf-8") as f:
            dados = json.load(f)

        cursor = conn.cursor()

        for item in dados:

            data = datetime.strptime(
                item["data"] + "/2026",
                "%d/%m/%Y"
            ).date()

            now = datetime.now().isoformat()

            cursor.execute("""
                INSERT INTO "transaction"
                (
                    account_id,
                    transaction_category_id,
                    transaction_type,
                    date,
                    name,
                    alias,
                    value,
                    status,
                    created_at,
                    updated_at
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                account_id,
                None,
                "Despesa",
                data.isoformat(),
                item["descricao"],
                None,
                str(item["valor"]),
                "Consolidado",
                now,
                now
            ))

        conn.commit()

        conn.close()


    def teste():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM "transaction"
    """)

    teste = cursor.fetchall()
    print(teste)


