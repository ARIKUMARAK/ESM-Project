import psutil
import socket
import platform
import sqlite3
import time
from datetime import datetime


DATABASE = "server_monitor.db"


# Save monitoring data
def save_monitoring_data(timestamp, cpu, ram, disk, data_sent, data_received):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO monitoring_data
        (timestamp, cpu, ram, disk, data_sent, data_received)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        cpu,
        ram,
        disk,
        data_sent,
        data_received
    ))

    connection.commit()

    connection.close()


# Save alert
def save_alert(timestamp, resource, usage, message):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO alerts
        (timestamp, resource, usage, message)
        VALUES (?, ?, ?, ?)
    """, (
        timestamp,
        resource,
        usage,
        message
    ))

    connection.commit()

    connection.close()


print("========================================")
print("      ENTERPRISE SERVER MONITOR")
print("========================================")


while True:

    # Server information

    server_name = socket.gethostname()

    operating_system = platform.system()

    try:
        ip_address = socket.gethostbyname(server_name)
    except:
        ip_address = "Unable to find IP"


    # Resource usage

    cpu = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory().percent

    disk = psutil.disk_usage('/').percent


    # Network usage

    network = psutil.net_io_counters()

    data_sent = round(
        network.bytes_sent / (1024 * 1024),
        2
    )

    data_received = round(
        network.bytes_recv / (1024 * 1024),
        2
    )


    # Timestamp

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # Display information

    print()
    print("========================================")

    print("Server Name :", server_name)

    print("OS          :", operating_system)

    print("IP Address  :", ip_address)

    print("----------------------------------------")

    print("CPU Usage   :", cpu, "%")

    print("RAM Usage   :", ram, "%")

    print("Disk Usage  :", disk, "%")

    print("----------------------------------------")

    print("Data Sent     :", data_sent, "MB")

    print("Data Received :", data_received, "MB")


    print()
    print("========== RESOURCE STATUS ==========")


    # CPU status

    if cpu > 80:

        print("⚠️ WARNING: High CPU Usage")

        save_alert(
            timestamp,
            "CPU",
            cpu,
            "High CPU Usage"
        )

    else:

        print("✅ CPU Status: Normal")


    # RAM status

    if ram > 80:

        print("⚠️ WARNING: High RAM Usage")

        save_alert(
            timestamp,
            "RAM",
            ram,
            "High RAM Usage"
        )

    else:

        print("✅ RAM Status: Normal")


    # Disk status

    if disk > 85:

        print("⚠️ WARNING: High Disk Usage")

        save_alert(
            timestamp,
            "Disk",
            disk,
            "High Disk Usage"
        )

    else:

        print("✅ Disk Status: Normal")


    # Save monitoring information

    save_monitoring_data(
        timestamp,
        cpu,
        ram,
        disk,
        data_sent,
        data_received
    )


    print()
    print("✅ Data saved to database.")

    print("Next check in 5 seconds...")

    time.sleep(5)