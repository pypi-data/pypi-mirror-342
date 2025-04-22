import os
import signal
import daemon
from daemon.pidfile import PIDLockFile
import select
import time

from .run import run

PID_LOCK_FILE = "/tmp/lavender-data.pid"
LOG_FILE = "/tmp/lavender-data.log"
WORKING_DIRECTORY = "./"


def start(*args, **kwargs):
    pid_lock_file = PIDLockFile(PID_LOCK_FILE)
    if pid_lock_file.is_locked():
        exit(1)

    f = open(LOG_FILE, "a")
    with daemon.DaemonContext(
        working_directory=WORKING_DIRECTORY,
        umask=0o002,
        pidfile=pid_lock_file,
        stdout=f,
        stderr=f,
    ):
        run(*args, **kwargs)


def stop():
    pid_lock_file = PIDLockFile(PID_LOCK_FILE)
    if not pid_lock_file.is_locked():
        return

    pid = pid_lock_file.read_pid()
    pid_lock_file.break_lock()
    os.kill(pid, signal.SIGTERM)


def restart(*args, **kwargs):
    stop()
    start(*args, **kwargs)


def logs(f_flag: bool = False, n_lines: int = 10):
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        print("".join(lines[-n_lines:]))

        if f_flag:
            while True:
                line = f.readline()
                if line:
                    print(line, end="")
                else:
                    time.sleep(0.1)
                    read_fds, _, _ = select.select([f], [], [], 1)
                    for fd in read_fds:
                        print(fd.read(), end="")
