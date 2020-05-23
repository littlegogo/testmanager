import sys
# from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QApplication
from mainwnd import CraneTestDocWnd

if __name__ == "__main__":
    # appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    app = QApplication([])
    wnd = CraneTestDocWnd()
    wnd.show()
    app.exec_()
    # exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    # sys.exit(exit_code)




