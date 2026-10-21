# ============================================================
# CPU SCHEDULING MODULE
# Enterprise Server Monitoring System
# ============================================================


# ============================================================
# SAMPLE PROCESS DATA
# ============================================================

processes = [
    {
        "pid": 101,
        "name": "Process-1",
        "burst": 5,
        "priority": 2
    },
    {
        "pid": 102,
        "name": "Process-2",
        "burst": 3,
        "priority": 1
    },
    {
        "pid": 103,
        "name": "Process-3",
        "burst": 8,
        "priority": 3
    },
    {
        "pid": 104,
        "name": "Process-4",
        "burst": 4,
        "priority": 2
    }
]


# ============================================================
# FCFS - FIRST COME FIRST SERVE
# ============================================================

def fcfs(processes):

    waiting_time = 0

    results = []

    total_waiting = 0
    total_turnaround = 0

    for process in processes:

        turnaround_time = waiting_time + process["burst"]

        results.append({
            "pid": process["pid"],
            "name": process["name"],
            "burst": process["burst"],
            "priority": process["priority"],
            "waiting": waiting_time,
            "turnaround": turnaround_time
        })

        total_waiting += waiting_time
        total_turnaround += turnaround_time

        waiting_time += process["burst"]

    average_waiting = total_waiting / len(processes)

    average_turnaround = total_turnaround / len(processes)

    return results, average_waiting, average_turnaround


# ============================================================
# SJF - SHORTEST JOB FIRST
# ============================================================

def sjf(processes):

    sorted_processes = sorted(
        processes,
        key=lambda x: x["burst"]
    )

    return fcfs(sorted_processes)


# ============================================================
# PRIORITY SCHEDULING
# Smaller number = Higher priority
# ============================================================

def priority_scheduling(processes):

    sorted_processes = sorted(
        processes,
        key=lambda x: x["priority"]
    )

    return fcfs(sorted_processes)


# ============================================================
# ROUND ROBIN
# ============================================================

def round_robin(processes, quantum=2):

    remaining = {}

    completion = {}

    for process in processes:

        remaining[process["pid"]] = process["burst"]


    current_time = 0

    queue = []

    for process in processes:

        queue.append(process["pid"])


    execution_order = []


    while queue:

        pid = queue.pop(0)

        execution_order.append(pid)


        # Process still needs more CPU time
        if remaining[pid] > quantum:

            current_time += quantum

            remaining[pid] -= quantum

            queue.append(pid)


        # Process finishes
        else:

            current_time += remaining[pid]

            remaining[pid] = 0

            completion[pid] = current_time


    results = []

    total_waiting = 0
    total_turnaround = 0


    for process in processes:

        pid = process["pid"]

        turnaround_time = completion[pid]

        waiting_time = (
            turnaround_time - process["burst"]
        )


        results.append({
            "pid": process["pid"],
            "name": process["name"],
            "burst": process["burst"],
            "priority": process["priority"],
            "waiting": waiting_time,
            "turnaround": turnaround_time
        })


        total_waiting += waiting_time

        total_turnaround += turnaround_time


    average_waiting = (
        total_waiting / len(processes)
    )

    average_turnaround = (
        total_turnaround / len(processes)
    )


    return (
        results,
        average_waiting,
        average_turnaround,
        execution_order
    )


# ============================================================
# DISPLAY FUNCTION
# ============================================================

def display_results(
    algorithm,
    results,
    average_waiting,
    average_turnaround
):

    print()
    print("------------------------------------------")
    print(algorithm)
    print("------------------------------------------")

    print(
        f"{'PID':<8}"
        f"{'PROCESS':<15}"
        f"{'BURST':<8}"
        f"{'PRIORITY':<10}"
        f"{'WAITING':<10}"
        f"{'TURNAROUND':<12}"
    )

    print("-" * 63)


    for process in results:

        print(
            f"{process['pid']:<8}"
            f"{process['name']:<15}"
            f"{process['burst']:<8}"
            f"{process['priority']:<10}"
            f"{process['waiting']:<10}"
            f"{process['turnaround']:<12}"
        )


    print()

    print(
        "Average Waiting Time    :",
        round(average_waiting, 2)
    )

    print(
        "Average Turnaround Time :",
        round(average_turnaround, 2)
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("          CPU SCHEDULING MODULE")
    print("==========================================")


    # ========================================================
    # DISPLAY INPUT PROCESSES
    # ========================================================

    print()
    print("Input Processes")
    print("------------------------------------------")

    for process in processes:

        print(
            f"PID: {process['pid']} | "
            f"Name: {process['name']} | "
            f"Burst Time: {process['burst']} | "
            f"Priority: {process['priority']}"
        )


    # ========================================================
    # FCFS
    # ========================================================

    results, avg_wait, avg_turn = fcfs(processes)

    display_results(
        "FCFS - First Come First Serve",
        results,
        avg_wait,
        avg_turn
    )


    # ========================================================
    # SJF
    # ========================================================

    results, avg_wait, avg_turn = sjf(processes)

    display_results(
        "SJF - Shortest Job First",
        results,
        avg_wait,
        avg_turn
    )


    # ========================================================
    # PRIORITY
    # ========================================================

    results, avg_wait, avg_turn = priority_scheduling(processes)

    display_results(
        "Priority Scheduling",
        results,
        avg_wait,
        avg_turn
    )


    # ========================================================
    # ROUND ROBIN
    # ========================================================

    results, avg_wait, avg_turn, execution_order = (
        round_robin(processes, quantum=2)
    )


    print()
    print("------------------------------------------")
    print("ROUND ROBIN")
    print("------------------------------------------")

    print("Time Quantum:", 2)

    print()

    print(
        "Execution Order:"
    )

    print(
        " -> ".join(
            str(pid)
            for pid in execution_order
        )
    )


    print()

    print(
        f"{'PID':<8}"
        f"{'PROCESS':<15}"
        f"{'BURST':<8}"
        f"{'WAITING':<10}"
        f"{'TURNAROUND':<12}"
    )

    print("-" * 53)


    for process in results:

        print(
            f"{process['pid']:<8}"
            f"{process['name']:<15}"
            f"{process['burst']:<8}"
            f"{process['waiting']:<10}"
            f"{process['turnaround']:<12}"
        )


    print()

    print(
        "Average Waiting Time    :",
        round(avg_wait, 2)
    )

    print(
        "Average Turnaround Time :",
        round(avg_turn, 2)
    )


    # ========================================================
    # COMPLETION MESSAGE
    # ========================================================

    print()
    print("==========================================")
    print("       CPU SCHEDULING COMPLETED")
    print("==========================================")