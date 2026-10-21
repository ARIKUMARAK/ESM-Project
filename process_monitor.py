import psutil


def get_processes():

    processes = []

    for process in psutil.process_iter(
        ['pid', 'name', 'status', 'cpu_percent', 'memory_percent']
    ):

        try:

            processes.append({
                'pid': process.info['pid'],
                'name': process.info['name'],
                'status': process.info['status'],
                'cpu': process.info['cpu_percent'],
                'memory': process.info['memory_percent']
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            pass

    return processes