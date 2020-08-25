import sys
from PyQt5 import QtWidgets
import form_classes as fc

app=QtWidgets.QApplication(sys.argv)
ana_ekran=fc.ana_ekran()
ana_ekran.show()

sys.exit(app.exec_())