import subprocess
import sys
from pathlib import Path

import threading


def exec_real_time(command):
    """
    Executes a command and prints its stdout and stderr in real time.

    Args:
        command (list or str): The command to execute as a list of arguments
                               or a single string.
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,  # Ensure output is treated as text
    )

    def print_stdout():
        for line in process.stdout:
            print(line, end="")  # Print without extra newline

    def print_stderr():
        for line in process.stderr:
            print(f"stderr: {line}", end="")

    stdout_thread = threading.Thread(target=print_stdout)
    stderr_thread = threading.Thread(target=print_stderr)

    stdout_thread.start()
    stderr_thread.start()

    process.wait()

    stdout_thread.join()
    stderr_thread.join()

    if process.returncode != 0:
        print(f"Command exited with code: {process.returncode}", file=sys.stderr)


def has_help(argv):
    if "-h" in argv or "--help" in argv:
        return True
    if "/?" in argv:
        return True
    if "-?" in argv:
        return True
    if len(argv) == 0:
        return True
    return False


def main():
    argv = sys.argv[1:]
    if has_help(argv):
        from fastqc_py.help_str import help_str

        print(help_str)
        exit(0)
    fastqc_path = Path(__file__).resolve().parent.parent.joinpath("fastqc_lib")
    fastqc_path_str = str(fastqc_path).replace("\\", "/")
    classpath = "!;!/sam-1.103.jar;!/jbzip2-0.9.jar".replace("!", fastqc_path_str)
    # print(classpath)
    exec_real_time(
        f"java -Xmx250m -classpath {classpath} uk.ac.babraham.FastQC.FastQCApplication "
        + " ".join(argv)
    )


if __name__ == "__main__":
    main()
