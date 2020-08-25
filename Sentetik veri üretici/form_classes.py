from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QFileDialog, QTableView
from PyQt5.QtCore import Qt, QAbstractTableModel

import pandas as pd
import pickle
import sys

from veri_uretici import sentetik_veri_uretici

from main_window import Ui_MainWindow as mw
from oznitelik_bilgi import Ui_Dialog as ob
from veriseti_tablo import Ui_VerisetiTabloDialog as vt

class ana_ekran(QMainWindow, mw):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.oznitelik_bilgileri=[]
        
        self.ilerle_btn.clicked.connect(self.oznitelik_bilgi_ekran)
        self.veriseti_goruntule_action.triggered.connect(self.veriseti_goruntule)

    def oznitelik_bilgi_ekran(self):
        if self.oznitelik_sayisi.text() == '' or int(self.oznitelik_sayisi.text()) <=0:
            popup=QMessageBox()
            popup.setWindowTitle('Hatalı girdi')
            popup.setText('Öznitelik sayısı 0\'dan büyük olmalıdır.')
            popup.exec_()
            return
        
        oznitelik_bilgi_dialog=oznitelik_bilgi(int(self.oznitelik_sayisi.text()))
        oznitelik_bilgi_dialog.durum=oznitelik_bilgi_dialog.exec()
        while oznitelik_bilgi_dialog.durum!=QDialog.Accepted:
            continue
        
        self.oznitelik_bilgileri=oznitelik_bilgi_dialog.oznitelik_bilgileri
        veriseti=self.veriseti_olustur()

        veriseti_tablo_dialog=veriseti_tablo(veriseti)
        veriseti_tablo_dialog.durum=veriseti_tablo_dialog.exec()
        while veriseti_tablo_dialog.durum!=QDialog.Accepted:
            continue
        
        self.close()
        
    def veriseti_goruntule(self):
        dosya_adi,_=QFileDialog.getOpenFileName(self,'Dosya seçiniz...','','CSV Dosyası(*.csv)')
        if dosya_adi=='':
            return
        veriseti=pd.read_csv(dosya_adi)
        
        veriseti_tablo_dialog=veriseti_tablo(veriseti)
        veriseti_tablo_dialog.durum=veriseti_tablo_dialog.exec()
        while veriseti_tablo_dialog.durum!=QDialog.Accepted:
            continue
        
        
    def veriseti_olustur(self):
        svi = sentetik_veri_uretici(self.oznitelik_bilgileri, int(self.veri_sayisi.text()), float(self.korelasyon_katsayisi.text()))
        
        svi.veri_uret()
        
        svi.korelasyon_kontrol()
                
        if self.normalizasyon_minmax.isChecked():
            svi.normalizasyon_minmax()
        elif self.normalizasyon_z_score.isChecked():
            svi.normalizasyon_z_score()

        return svi.veriseti
        

class oznitelik_bilgi(QDialog, ob):
    def __init__(self,oznitelik_sayisi, parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        
        self.oznitelik_sayisi=oznitelik_sayisi
        self.oznitelik_bilgileri=[[],[]]
        self.durum=None
        
        self.oznitelik_no_input.setText('1')
        self.oznitelik_ad_input.setText('F1')
        self.aralik_kucuk_input.setText('0')
        self.aralik_buyuk_input.setText('100')
        
        self.ilerle_btn.clicked.connect(self.sonraki_oznitelik)
        
        
    def sonraki_oznitelik(self):
        self.oznitelik_bilgileri[0].append(str(self.oznitelik_ad_input.text()))
        self.oznitelik_bilgileri[1].append([int(self.aralik_kucuk_input.text()),int(self.aralik_buyuk_input.text())])
        
        self.oznitelik_ad_input.setText('F'+str(int(self.oznitelik_no_input.text())+1))
        self.aralik_kucuk_input.setText('0')
        self.aralik_buyuk_input.setText('100')
        
        self.oznitelik_no_input.setText(str(int(self.oznitelik_no_input.text())+1))
        if int(self.oznitelik_no_input.text())>self.oznitelik_sayisi:
            self.oznitelik_bilgileri[0].append('Sınıf')
            self.oznitelik_bilgileri[1].append([0,1])
            self.accept()
            

class veriseti_tablo(QDialog,vt):
    def __init__(self,df,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.durum=None
        
        self.df=df
        
        model=tablo_model(df)
        self.veriseti_table.setModel(model)

        header=self.veriseti_table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        
        self.kaydet_btn.clicked.connect(self.veriseti_kaydet)
        self.cikis_btn.clicked.connect(self.accept)
        
    def veriseti_kaydet(self):
        dosya_adi,_=QFileDialog.getSaveFileName(self,'Dosya kaydet...','','CSV Dosyası(*.csv)')
        self.df.to_csv(dosya_adi,index=False)
        
        
class tablo_model(QAbstractTableModel):
    def __init__(self,df):
        QAbstractTableModel.__init__(self)
        self.df=df

    def rowCount(self,parent=None):
        return self.df.shape[0]

    def columnCount(self,parent=None):
        return self.df.shape[1]

    def data(self,index,role):
        if index.isValid():
            if role==Qt.DisplayRole:
                return str(self.df.iloc[index.row(),index.column()])

        return None
            
