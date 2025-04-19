"""
PostgreSQL

https://www.psycopg.org/psycopg3/docs/basic/usage.html
"""

import os

import psycopg
from dotenv_vault import load_dotenv

if __name__ == "__main__":
    _ = load_dotenv()

    # Подключиться к существующей базе данных
    with psycopg.connect(
            f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASSWORD')}"
    ) as conn:
        # Откройте курсор для выполнения операций с базой данных.
        with conn.cursor() as cur:
            # Передавайте данные для заполнения заполнителей запроса
            # и позвольте Psycopg выполнить правильное преобразование (без SQL-инъекций!)
            cur.execute(
                # "INSERT INTO prices (symbol, value) VALUES (%s, %s)", ("abc'def", 100),
                # "DELETE FROM prices WHERE symbol = %s", ("abc'def",),
            )

            # Запросите базу данных и получите данные в виде объектов Python.
            cur.execute("SELECT * FROM prices")
            cur.fetchone()
            # will return (1, 100, "abc'def")

            # Вы можете использовать cur.fetchmany(), cur.fetchall()
            # для возврата списка из нескольких записей или даже перебирать курсор.
            for record in cur:
                print(record)

            # Сделать изменения в базе данных постоянными
            conn.commit()
