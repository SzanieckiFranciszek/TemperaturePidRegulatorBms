from python_pid import PythonPID


def main():
    controller = PythonPID()
    controller.run_pid_controller()


if __name__ == "__main__":
    main()
