# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'veriseti_tablo.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VerisetiTabloDialog(object):
    def setupUi(self, VerisetiTabloDialog):
        VerisetiTabloDialog.setObjectName("VerisetiTabloDialog")
        VerisetiTabloDialog.resize(837, 509)
        self.verticalLayout = QtWidgets.QVBoxLayout(VerisetiTabloDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.veriseti_table = QtWidgets.QTableView(VerisetiTabloDialog)
        self.veriseti_table.setObjectName("veriseti_table")
        self.verticalLayout.addWidget(self.veriseti_table)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.kaydet_btn = QtWidgets.QPushButton(VerisetiTabloDialog)
        self.kaydet_btn.setEnabled(True)
        self.kaydet_btn.setObjectName("kaydet_btn")
        self.horizontalLayout.addWidget(self.kaydet_btn)
        self.cikis_btn = QtWidgets.QPushButton(VerisetiTabloDialog)
        self.cikis_btn.setObjectName("cikis_btn")
        self.horizontalLayout.addWidget(self.cikis_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(VerisetiTabloDialog)
        QtCore.QMetaObject.connectSlotsByName(VerisetiTabloDialog)

    def retranslateUi(self, VerisetiTabloDialog):
        _translate = QtCore.QCoreApplication.translate
        VerisetiTabloDialog.setWindowTitle(_translate("VerisetiTabloDialog", "Veriseti Tablosu"))
        self.kaydet_btn.setText(_translate("VerisetiTabloDialog", "Kaydet"))
        self.cikis_btn.setText(_translate("VerisetiTabloDialog", "Çıkış"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VerisetiTabloDialog = QtWidgets.QDialog()
    ui = Ui_VerisetiTabloDialog()
    ui.setupUi(VerisetiTabloDialog)
    VerisetiTabloDialog.show()
    sys.exit(app.exec_())

