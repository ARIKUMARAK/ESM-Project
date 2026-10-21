import sqlite3


DATABASE = "server_monitor.db"


def create_tables():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    # Monitoring data table

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_data (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            cpu REAL,

            ram REAL,

            disk REAL,

            data_sent REAL,

            data_received REAL

        )
    """)


    # Alert history table

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            resource TEXT,

            usage REAL,

            message TEXT

        )
    """)


    connection.commit()

    connection.close()


if __name__ == "__main__":

    create_tables()

    print("✅ Database tables created successfully.")