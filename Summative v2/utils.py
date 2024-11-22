from datetime import datetime


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class LOGGER:
    def __init__(self, filepath=None):
        self.level = 0
        self.filepath = filepath

        if self.filepath is not None:
            with open(self.filepath, "a") as f:
                f.write(f"{datetime.now()}\n")

    def PRINT_LOG(self, title, color, detail):
        indent = " " * self.level * 5
        print(f"{indent}{color}{title:20}{bcolors.ENDC}{detail}")

        if self.filepath is not None:
            with open(self.filepath, "a") as f:
                f.write(f"{indent}{title:20}{detail}\n")

    def ADD_LEVEL(self):
        self.level = self.level + 1

    def SUB_LEVEL(self):
        self.level = self.level - 1

    def RESET_LEVEL(self):
        self.level = 0
