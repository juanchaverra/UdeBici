import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5 import uic
from datetime import date, datetime
from PyQt5.QtGui import QFont as QF

import bdlocal

cedula = 0


class Principal(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("Ui/mainwindow.ui", self)
        self.bt_entrada.clicked.connect(self.conectar)
        self.ventana = Ventana()

    def conectar(self):
        cedula = self.te_buscar.toPlainText()
        if cedula != 0:
            hora = datetime.now().strftime("%H:%M:%S")
            dato = (cedula, hora)
            bdlocal.cedula_ingreso(dato)
            bdlocal.select_ingreso(0)
            bdlocal.select_registro()
            self.ventana.exec_()

    def showEvent(self, event):
        fecha = datetime.now().strftime("%d-%m-%Y")
        self.l_fecha.setText(fecha)
        self.l_fecha.setFont(QF("Sanserif ", 12))
        self.l_fecha.setStyleSheet('color:green')
        # self.l_fecha.setColor("green")

    def closeEvent(self, event):
        pregunta = QMessageBox.question(self, "Salir", "¿Seguro desea salir?", QMessageBox.Yes | QMessageBox.No)
        if pregunta == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Ventana(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.nuevo = 0
        uic.loadUi("Ui/ventana.ui", self)
        self.bt_confirmar.clicked.connect(self.verificar)
        self.verificar()

    def showEvent(self, event):
        hora = datetime.now().strftime("%H:%M:%S")
        porteria = "Ferrocarril"  # diferenciar pc
        self.nuevo = 0
        self.te_porteria.setText(porteria)
        self.te_hora.setText(hora)
        datos_ingreso = bdlocal.select_ingreso(1)
        size = len(datos_ingreso)-1
        entrada = datos_ingreso[size]
        self.te_cc.setText(str(entrada[1]))
        datos_registro = bdlocal.where_registro(entrada[1])
        if datos_registro:
            self.te_nombre.setText(datos_registro[0][2])    # Nombre
            self.te_serie.setText(datos_registro[0][3])     # Serie
            self.te_marca.setText(datos_registro[0][4])     # Marca
            self.te_color.setText(datos_registro[0][5])     # Color
            self.nuevo = 1
        self.registraractualizar()


    def registraractualizar(self):
        nombre = self.te_nombre.toPlainText()



    def verificar(self):
        cc = self.te_cc.toPlainText()
        nombre = self.te_nombre.toPlainText()
        serie = self.te_serie.toPlainText()
        marca = self.te_marca.toPlainText()
        color = self.te_color.toPlainText()
        porteria = self.te_porteria.toPlainText()
        hora = self.te_hora.toPlainText()

        value_registro = (cc, nombre, serie, marca, color)
        value_ingreso = (nombre, porteria)
        if cc != '' and nombre != '' and serie != '' and marca != '' and color != '':
            bdlocal.nombre_porteria(nombre, porteria, cc)   # Actualizar base de datos ingreso
            if self.nuevo == 0:
                bdlocal.insertar_registro(value_registro)

            self.te_nombre.clear()  # Nombre
            self.te_serie.clear()  # Serie
            self.te_marca.clear()  # Marca
            self.te_color.clear()

            print(" --------------------------------------------------------------- \nBotón confirmar")
            bdlocal.select_registro()
            bdlocal.select_ingreso(0)
            QDialog.close(self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    principal = Principal()
    principal.show()
    app.exec_()
