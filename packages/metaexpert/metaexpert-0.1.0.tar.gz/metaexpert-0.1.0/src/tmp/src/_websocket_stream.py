import json
import os
import time

import psycopg
import websocket
from dotenv_vault import load_dotenv


def on_message(ws, message):
    data = json.loads(message)

    with psycopg.connect(
            f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASSWORD')}"
    ) as conn:
        with conn.cursor() as cur:
            for symbol in data:
                cur.execute(
                    "INSERT INTO prices (symbol, value) VALUES (%s, %s) ON CONFLICT (symbol) DO UPDATE SET value = %s",
                    (symbol["s"], symbol["c"], symbol["c"]),
                )
            conn.commit()
    time.sleep(3)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


if __name__ == "__main__":
    _ = load_dotenv()

    ws = websocket.WebSocketApp(
        "wss://stream.binance.com:9443/ws/!ticker@arr",
        on_message=on_message,
        on_close=on_close,
    )

    ws.run_forever()
