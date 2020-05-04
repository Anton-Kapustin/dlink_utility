import sys

from Controllers.ControllerMain import ControllerMain


class MainView:

    def __init__(self, argv):
        self.controller = ControllerMain(self)
        self.controller.set_sys_argv(argv)
        # print(argv)


if __name__ == '__main__':
    view = MainView(sys.argv)
