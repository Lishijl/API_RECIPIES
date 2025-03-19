import mysql.connector
from mysql.connector import pooling

# Configuración de la BD
db_config = {
    'host': 'mariadb',
    'user': 'root',
    'password': 'P@ssw0rd',
    'database': 'recipies',
    'collation': 'utf8mb4_general_ci'
}

# Crear un pool de conexiones
db_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **db_config)

def get_db_connection():
    conn = db_pool.get_connection()
