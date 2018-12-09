# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/src/plugin_build_tool/tests/sample2/designer/about_widget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 240)
        self.lbl_text = QtWidgets.QLabel(Form)
        self.lbl_text.setGeometry(QtCore.QRect(60, 40, 231, 101))
        self.lbl_text.setAutoFillBackground(False)
        self.lbl_text.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_text.setWordWrap(True)
        self.lbl_text.setIndent(-1)
        self.lbl_text.setObjectName("lbl_text")
        self.btn_ok = QtWidgets.QPushButton(Form)
        self.btn_ok.setGeometry(QtCore.QRect(200, 180, 96, 35))
        self.btn_ok.setObjectName("btn_ok")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lbl_text.setText(_translate("Form",
                                         "This is an demonstration about box, which is rendered by a compiled .ui file found in the designer folder."))
        self.btn_ok.setText(_translate("Form", "ok"))

