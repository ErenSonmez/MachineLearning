# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oznitelik_bilgi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(592, 139)
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.oznitelik_no_label = QtWidgets.QLabel(Dialog)
        self.oznitelik_no_label.setObjectName("oznitelik_no_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.oznitelik_no_label)
        self.oznitelik_no_input = QtWidgets.QLineEdit(Dialog)
        self.oznitelik_no_input.setReadOnly(True)
        self.oznitelik_no_input.setObjectName("oznitelik_no_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.oznitelik_no_input)
        self.oznitelik_ad_label = QtWidgets.QLabel(Dialog)
        self.oznitelik_ad_label.setObjectName("oznitelik_ad_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.oznitelik_ad_label)
        self.oznitelik_ad_input = QtWidgets.QLineEdit(Dialog)
        self.oznitelik_ad_input.setObjectName("oznitelik_ad_input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.oznitelik_ad_input)
        self.aralik_label = QtWidgets.QLabel(Dialog)
        self.aralik_label.setObjectName("aralik_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.aralik_label)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.aralik_kucuk_input = QtWidgets.QLineEdit(Dialog)
        self.aralik_kucuk_input.setObjectName("aralik_kucuk_input")
        self.horizontalLayout_4.addWidget(self.aralik_kucuk_input)
        self.aralik_input_label = QtWidgets.QLabel(Dialog)
        self.aralik_input_label.setObjectName("aralik_input_label")
        self.horizontalLayout_4.addWidget(self.aralik_input_label)
        self.aralik_buyuk_input = QtWidgets.QLineEdit(Dialog)
        self.aralik_buyuk_input.setObjectName("aralik_buyuk_input")
        self.horizontalLayout_4.addWidget(self.aralik_buyuk_input)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.ilerle_btn = QtWidgets.QPushButton(Dialog)
        self.ilerle_btn.setObjectName("ilerle_btn")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.ilerle_btn)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Öznitelik Bilgileri"))
        self.oznitelik_no_label.setText(_translate("Dialog", "Oluşturulan öznitelik numarası : "))
        self.oznitelik_ad_label.setText(_translate("Dialog", "Öznitelik adı : "))
        self.aralik_label.setText(_translate("Dialog", "Öznitelik veri aralığı : "))
        self.aralik_input_label.setText(_translate("Dialog", "ile"))
        self.ilerle_btn.setText(_translate("Dialog", "İlerle"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

