import numpy as np
import psycopg2
from psycopg2.extras import DictCursor


DB_CONFIG = {
    "host": "77.239.102.166",
    "port": 5432,
    "dbname": "app_db",
    "user": "admin",
    "password": "your_strong_password"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

connection = get_db_connection()

with connection.cursor(cursor_factory=DictCursor) as cur:
    cur.execute("""
        SELECT id, description_vector
        FROM items
        WHERE description_vector IS NOT NULL
    """)

    rows = cur.fetchall()

connection = get_db_connection()


with connection.cursor() as update_cur:
    for row in rows:
        id_val, vector = row

        if vector is None:
            continue

        clean_string = vector.strip('[]{}()').replace(' ', '')
        vector_values = [float(x) for x in clean_string.split(',')]

        vector_np = np.array(vector_values)
        norm = np.linalg.norm(vector_np)

        if norm > 0:
            normalized_vector = vector_np / norm

            update_cur.execute("""
                UPDATE items
                SET description_vector = %s
                WHERE id = %s
            """, (normalized_vector.tolist(), id_val))

    connection.commit()
