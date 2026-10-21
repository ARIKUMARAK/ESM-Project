from flask import Flask, render_template
import sqlite3
import socket
import platform
import psutil
import time
import os

from process_monitor import get_processes
from scheduling import (
    processes,
    fcfs,
    sjf,
    priority_scheduling,
    round_robin
)

app = Flask(__name__)

# ============================================================
# DATABASE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "server_monitor.db")


# ============================================================
# GET MONITORING DATA
# ============================================================

def get_monitoring_data():

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM monitoring_data
        ORDER BY id DESC
        LIMIT 1
    """)

    latest = cursor.fetchone()

    cursor.execute("""
        SELECT timestamp, cpu, ram, disk
        FROM monitoring_data
        ORDER BY id DESC
        LIMIT 20
    """)

    history = cursor.fetchall()

    cursor.execute("""
        SELECT timestamp, resource, usage, message
        FROM alerts
        ORDER BY id DESC
        LIMIT 20
    """)

    alerts = cursor.fetchall()

    connection.close()

    history = history[::-1]

    return latest, history, alerts


# ============================================================
# SERVER UPTIME
# ============================================================

def get_uptime():

    boot_time = psutil.boot_time()

    uptime_seconds = time.time() - boot_time

    days = int(uptime_seconds // 86400)

    hours = int(
        (uptime_seconds % 86400) // 3600
    )

    minutes = int(
        (uptime_seconds % 3600) // 60
    )

    return f"{days} Days {hours} Hours {minutes} Minutes"


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    # Monitoring data
    latest, history, alerts = get_monitoring_data()

    # Server information
    server_name = socket.gethostname()

    operating_system = platform.system()

    try:
        ip_address = socket.gethostbyname(server_name)
    except socket.gaierror:
        ip_address = "Unable to find IP"

    uptime = get_uptime()

    # Network information
    network = psutil.net_io_counters()

    data_sent = round(
        network.bytes_sent / (1024 * 1024),
        2
    )

    data_received = round(
        network.bytes_recv / (1024 * 1024),
        2
    )

    # ========================================================
    # PROCESS MONITORING
    # ========================================================

    running_processes = get_processes()

    running_processes = sorted(
        running_processes,
        key=lambda x: x["cpu"],
        reverse=True
    )

    running_processes = running_processes[:20]


    # ========================================================
    # CPU SCHEDULING
    # ========================================================

    fcfs_results, fcfs_wait, fcfs_turn = fcfs(processes)

    sjf_results, sjf_wait, sjf_turn = sjf(processes)

    priority_results, priority_wait, priority_turn = (
        priority_scheduling(processes)
    )

    rr_results, rr_wait, rr_turn, rr_execution = (
        round_robin(
            processes,
            quantum=2
        )
    )


    # ========================================================
    # SEND EVERYTHING TO DASHBOARD
    # ========================================================

    return render_template(
        "dashboard.html",

        # Monitoring
        data=latest,
        history=history,
        alerts=alerts,

        # Server
        server_name=server_name,
        operating_system=operating_system,
        ip_address=ip_address,
        uptime=uptime,

        # Network
        data_sent=data_sent,
        data_received=data_received,

        # Processes
        processes=running_processes,

        # CPU Scheduling
        fcfs_results=fcfs_results,
        fcfs_wait=fcfs_wait,
        fcfs_turn=fcfs_turn,

        sjf_results=sjf_results,
        sjf_wait=sjf_wait,
        sjf_turn=sjf_turn,

        priority_results=priority_results,
        priority_wait=priority_wait,
        priority_turn=priority_turn,

        rr_results=rr_results,
        rr_wait=rr_wait,
        rr_turn=rr_turn,

        rr_execution=rr_execution
    )


# ============================================================
# START FLASK
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)