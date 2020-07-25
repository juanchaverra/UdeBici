import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem
from PyQt5 import uic
from datetime import datetime, date
from PyQt5.QtGui import QFont as QF, QPixmap
import pandas as pd
from openpyxl import load_workbook
import cv2
import PySimpleGUI as sg
import Datalake
import azureSQL

porteria_pc = "Ferrocarril"
posicion = 0
lista = []
s = []



def get_image(camara):
    retval, img = camara.read()
    return img
# funcion para enviar la cedula ingresada a la ventana de registro, y para identificar el boton presionado
def leer_cedula(cc=0, d='0'):
    lista.append(cc)
    lista.append(d)
    return lista[0], lista[1]


# Funcion para identicar si se presiono el boton de confirmar o el boton de cancelar
def conexion(b="0"):
    s.append(b)
    size = len(s)
    if size == 2:
        return s[0]
    else:
        return s[len(s) - 2]


class Principal(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("Ui/mainwindow.ui", self)
        self.setWindowTitle("Universidad de Antioquia")
        self.bt_entrada.clicked.connect(self.bt_Entrada)
        self.bt_salida.clicked.connect(self.bt_Salida)
        self.bt_pendientes.clicked.connect(self.bt_Pendiente)
        self.bt_finalizar.clicked.connect(self.bt_Finalizar)
        self.ventana = Ventana()
        self.lista = Lista()
        self.consultar_datos_entrada()
        self.consultar_datos_salida()

    def showEvent(self, event):
        fecha = datetime.now().strftime("%d-%m-%Y")
        self.l_fecha.setText(fecha)
        self.l_fecha.setFont(QF("Sanserif ", 16))
        self.l_fecha.setStyleSheet('color:green')

        ingresos = azureSQL.select_ingreso(1)
        con_ingreso = len(ingresos)
        self.l_num_ingreso.setText(str(con_ingreso))
        self.l_num_ingreso.setFont(QF("Sanserif ", 11))
        self.l_num_ingreso.setStyleSheet('color:green')

        # self.l_fecha.setColor("green")

    def bt_Entrada(self):
        cedula = self.le_tip.text()
        ingresos, val, disponible = self.validaciones(cedula)
        if ingresos and disponible == "true":  # Verifica que el estudiante no este en la tabla de ingreso
            self.msg_ya_exite()
        elif val == 3:
            leer_cedula(cedula, "entrada")
            self.ventana.exec_()
            self.le_tip.clear()
            boton = conexion()
            s.clear()
            if boton == "confirmar":
                ultimo = azureSQL.select_ingreso()  # Consulta la tabla de ingresos
                self.actualizar_tabla_ingreso(ultimo[len(ultimo) - 1])  # Escribir el ultimo ingresado a la
                cont_ingresos = len(azureSQL.select_ingreso(1))  # Escribir numero de ingresos
                self.l_num_ingreso.setText(str(cont_ingresos))
                self.l_num_ingreso.setFont(QF("Sanserif ", 12))
                self.l_num_ingreso.setStyleSheet('color:green')

        elif cedula == "lista":
            leer_cedula(cedula, "entrada")
            self.lista.exec_()
            self.le_tip.clear()

    def bt_Salida(self):
        cedula = self.le_tip.text()

        ingresos, val, disponible = self.validaciones(cedula)
        if ingresos:
            consulta = azureSQL.where_salida(cedula)
            if not consulta:
                self.actualizar(cedula)
            else:
                dis = consulta[len(consulta) - 1][5]
                if dis == "true":
                    self.msg_ya_salio()
                else:
                    self.actualizar(cedula)
        elif val == 3:
            self.msg_no_ingreso()

    def bt_Pendiente(self):
        cedula = self.le_tip.text()
        pendientes, val, disponible = self.validaciones(cedula)
        if pendientes:
            self.msg_ingreso_pendiente()
        elif val == 3:
            pendiente = azureSQL.where_pendientes(cedula)
            if pendiente:
                leer_cedula(cedula, "pendiente")
                self.ventana.exec_()
                self.le_tip.clear()
                boton = conexion()
                s.clear()
                if boton == "confirmar":
                    azureSQL.select_pendientes(1)
            else:
                self.msg_no_pendientes()

        elif cedula == "lista":
            leer_cedula(cedula, "pendiente")
            self.lista.exec_()
            self.le_tip.clear()

    def bt_Finalizar(self):
        pregunta = QMessageBox.question(self, "Finalizar", "Guardar informe y eliminar ingresos",
                                        QMessageBox.Yes | QMessageBox.No)
        if pregunta == QMessageBox.Yes:
            pendientes = azureSQL.select_pendientes()
            no_pendiente = []
            for pendiente in pendientes:
                if pendiente[7]:
                    no_pendiente.append(pendiente)
                    azureSQL.delete_pendiente(pendiente[1])
            ingresos = azureSQL.select_ingreso()
            fecha = datetime.now().strftime("%d-%m-%Y")
            informe = []
            lista_pendientes = []

            for estudiante in ingresos:
                cedula = estudiante[1]
                nombre = estudiante[2]
                hora = estudiante[3]
                porteria = estudiante[4]
                hps = azureSQL.hora_porteria_salida(estudiante[1])
                try:
                    dato = (cedula, nombre, hora, porteria, hps[0][1], hps[0][0])
                    informe.append(dato)
                except:
                    dato = (cedula, nombre, hora, porteria, fecha)
                    azureSQL.insert_pendientes_entrada(dato)
                    lista_pendientes.append(dato)





            file = str(fecha) + ".xlsx"
            azureSQL.select_pendientes(1)
            df = pd.DataFrame(informe)
            df.columns = ['Cedula', 'Nombre', 'Hora Ingreso', 'Porteria Ingreso', 'Hora Salida', 'Porteria Salida']
            df.to_excel(file, sheet_name='Informe')

            book = load_workbook(file)
            writer = pd.ExcelWriter(file, engine='openpyxl')
            writer.book = book
            writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

            df1 = pd.DataFrame(lista_pendientes)
            df1.columns = ['Cedula', 'Nombre', 'Hora', 'Porteria', 'Fecha']
            df1.to_excel(writer, 'Pendiente')

            df2 = pd.DataFrame(no_pendiente)
            df2.columns = ['Cedula', 'Nombre', 'Hora Ingreso', 'Porteria ingreso', 'Fecha ingreso', 'Porteria Salida', 'Hora salida', 'Fecha salida']
            df2.to_excel(writer, 'No_pendientes')
            azureSQL.limpiar_ingreso()
            azureSQL.limpiar_salida()
            self.tb_ingreso.setRowCount(0)
            self.l_num_ingreso.setText("0")
            self.l_num_ingreso.setFont(QF("Sanserif ", 11))
            self.l_num_ingreso.setStyleSheet('color:green')

            self.tb_salida.setRowCount(0)
            self.l_num_salida.setText("0")
            self.l_num_salida.setFont(QF("Sanserif ", 11))
            self.l_num_salida.setStyleSheet('color:red')

            self.close()

    def msg_no_pendientes(self):
        QMessageBox.warning(None, "Pendientes", u'El estudiante no se encuentra en la lista de pendientes',
                            QMessageBox.Ok,
                            QMessageBox.Ok)

    def msg_ingreso_pendiente(self):
        QMessageBox.warning(None, "Pendiente", u'El estudiante se encuentra registrado el día de hoy',
                            QMessageBox.Ok,
                            QMessageBox.Ok)

    def msg_ya_salio(self):
        QMessageBox.warning(None, "Dato", u'El estudiante ya salió',
                            QMessageBox.Ok,
                            QMessageBox.Ok)

    def msg_sin_dato(self):
        QMessageBox.warning(None, "Sin dato", u'Ingresa la cedula',
                            QMessageBox.Ok,
                            QMessageBox.Ok)

    def msg_error_datos(self):
        QMessageBox.warning(None, "Datos", u'Error con datos ingresados',
                            QMessageBox.Ok,
                            QMessageBox.Ok)

    def msg_error_size(self):
        QMessageBox.warning(None, "Longitud", u'El número no es válido',
                            QMessageBox.Ok,
                            QMessageBox.Ok)

    def msg_ya_exite(self):
        QMessageBox.warning(None, "Ingreso", u'El estudiante ya ingresó',
                            QMessageBox.Ok,
                            QMessageBox.Ok)

    def msg_no_ingreso(self):
        QMessageBox.warning(None, "Salida", u'El usuario no ingresó',
                            QMessageBox.Ok,
                            QMessageBox.Ok)

    def validaciones(self, cc):  # Realiza 3 validaciones
        ingresos = ''
        disponible = "falso"
        val = 0
        if cc:  # Verifica que no este vacio
            val += 1
            try:  # El dato ingresado es un numero
                int(cc)
                val += 1
                if len(cc) > 6 and len(cc) < 12:  # la longitud de la cc debe estar en el rango (6,12)
                    val += 1
                    ingresos = azureSQL.where_ingreso(cc)
                    if ingresos:
                        disponible = ingresos[len(ingresos) - 1][5]
                    return ingresos, val, disponible
                else:
                    self.msg_error_size()

            except:
                if cc != 'lista':
                    self.msg_error_datos()


        else:
            self.msg_sin_dato()
        return ingresos, val, disponible

    def actualizar_tabla_ingreso(self, ingresos):
        nombre = ingresos[2]
        cc = ingresos[1]
        if nombre:
            self.tb_ingreso.insertRow(self.fila)
            col = 0
            for j in range(1, 5):
                celda = QTableWidgetItem(str(ingresos[j]))
                self.tb_ingreso.setItem(self.fila, col, celda)
                col += 1
            self.fila += 1

        else:
            azureSQL.delete_ingreso(cc)

    def actualizar_tabla_salida(self, ingresos):
        nombre = ingresos[0][2]
        cc = ingresos[0][1]
        if nombre:
            self.tb_salida.insertRow(self.fila_salida)
            col = 0
            for j in range(1, 5):
                celda = QTableWidgetItem(str(ingresos[0][j]))
                self.tb_salida.setItem(self.fila_salida, col, celda)
                col += 1

            self.fila_salida += 1
            self.l_num_salida.setText(str(self.fila_salida))
            self.l_num_salida.setFont(QF("Sanserif ", 11))
            self.l_num_salida.setStyleSheet('color:red')


        else:
            azureSQL.delete_ingreso(cc)

    def consultar_datos_entrada(self):
        self.datos = azureSQL.select_ingreso(1)
        self.fila = 0
        for elementos in self.datos:
            self.tb_ingreso.insertRow(self.fila)
            col = 0
            for j in range(1, 5):
                celda = QTableWidgetItem(str(elementos[j]))
                self.tb_ingreso.setItem(self.fila, col, celda)
                col += 1
            self.fila += 1

    def consultar_datos_salida(self):
        self.fila_salida = 0
        salida = azureSQL.select_salida()
        size = len(salida)
        for registro in salida:
            self.tb_salida.insertRow(self.fila_salida)
            col = 0
            for j in range(1, 5):
                celda = QTableWidgetItem(str(registro[j]))
                self.tb_salida.setItem(self.fila_salida, col, celda)
                col += 1
            self.fila_salida += 1
        self.l_num_salida.setText(str(size))
        self.l_num_salida.setFont(QF("Sanserif ", 11))
        self.l_num_salida.setStyleSheet('color:red')

    def actualizar(self, cedula):
        leer_cedula(cedula, "salida")
        self.ventana.exec_()
        self.le_tip.clear()
        boton = conexion()
        s.clear()
        if boton == "confirmar":
            salida = azureSQL.where_salida(cedula)
            self.actualizar_tabla_salida(salida)
        else:
            pass

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
        self.bt_confirmar.clicked.connect(self.bt_Confirmar)
        self.bt_cancelar.clicked.connect(self.bt_Cancelar)
        self.bt_eli_img.clicked.connect(self.bt_Eliminar_img)
        self.bt_foto.clicked.connect(self.bt_Tomar_foto)
        self.camara = Camara()

    def showEvent(self, event):
        self.lb_img.setPixmap(QPixmap("escudo2.png"))
        global datos_registro
        hora = datetime.now().strftime("%H:%M:%S")
        cedula, f = leer_cedula()
        self.le_cc.setText(cedula)
        self.nuevo = 0
        self.le_cc.setEnabled(False)
        self.le_cc.setFont(QF("Sanserif", 10, weight=QF.Bold))

        if f == "pendiente":
            self.label.setText("Registro de pendientes")
            self.label.setFont(QF("Sanserif", 14, weight=QF.Bold))
            self.label.setStyleSheet('color:blue')
            self.label_9.setText("Fecha de ingreso")
            self.label_9.setFont(QF("Sanserif", 10))
            self.label_8.setText("Porteria de ingreso")
            self.label_8.setFont(QF("Sanserif", 10))
            pendientes = azureSQL.where_pendientes(cedula)  # Consultar fecha de ingreso y porteria
            self.le_hora.setText(pendientes[0][5])
            self.le_porteria.setText(pendientes[0][4])
            self.le_enabled()

        elif f == "entrada":
            self.label.setText("Registro de ingreso")
            self.label.setFont(QF("Sanserif", 14, weight=QF.Bold))
            self.label.setStyleSheet('color:green')
            self.label_9.setText("Hora de entrada")
            self.label_9.setFont(QF("Sanserif", 10))
            self.label_8.setText("Porteria de entrada")
            self.label_8.setFont(QF("Sanserif", 10))
            self.le_hora.setText(hora)
            self.le_porteria.setText(porteria_pc)
            self.habilitar()

        elif f == "salida":
            self.label.setText("Registro de salida")
            self.label.setFont(QF("Sanserif", 14, weight=QF.Bold))
            self.label.setStyleSheet('color:red')
            self.label_9.setText("Hora de salida")
            self.label_9.setFont(QF("Sanserif", 10))
            self.label_8.setText("Porteria de salida")
            self.label_8.setFont(QF("Sanserif", 10))
            self.le_hora.setText(hora)
            self.le_porteria.setText(porteria_pc)
            self.le_enabled()

        datos_registro = azureSQL.where_registro(cedula)
        if datos_registro:
            self.nombre_registro = datos_registro[0][2]
            self.le_nombre.setText(self.nombre_registro)  # Nombre
            self.le_serie.setText(datos_registro[0][3])  # Serie
            self.le_marca.setText(datos_registro[0][4])  # Marca
            self.le_color.setText(datos_registro[0][5])  # Color
            self.le_nombre.setEnabled(False)
            self.le_nombre.setFont(QF("Sanserif", 10, weight=QF.Bold))
            self.nuevo = 1
            img = Datalake.download_file_from_directory(cedula)
            if img:
                self.lb_img.setPixmap(QPixmap("Des/" + str(cedula) + ".jpeg"))

    def bt_Confirmar(self):
        cc = self.le_cc.text()
        nombre = self.le_nombre.text()
        serie = self.le_serie.text()
        marca = self.le_marca.text()
        color = self.le_color.text()
        if cc and nombre and serie and marca and color:

            try:
                datos_registro = azureSQL.where_registro(cc)
                nombre_registro = datos_registro[0][2]
                serie_registro = datos_registro[0][3]
                marca_registro = datos_registro[0][4]
                color_registro = datos_registro[0][5]
                if nombre_registro != nombre or serie != serie_registro or marca_registro != marca or color_registro != color:
                    azureSQL.actualizar_registro(cc, serie, marca, color)
            except:
                pass

            porteria = self.le_porteria.text()
            hora = self.le_hora.text()
            conexion("confirmar")
            cedula, decision = leer_cedula()
            lista.clear()
            if decision == "entrada":
                azureSQL.disponible_salida(cedula)
                disponible = "true"
                value_registro = (cc, nombre, serie, marca, color)
                dato = (cc, nombre, hora, porteria, disponible)
                azureSQL.insertar_ingreso(dato)

                if self.nuevo == 0:  # Verifica si el usuario estaba previamente registrado
                    azureSQL.insertar_registro(value_registro)

            elif decision == "salida":
                hora = datetime.now().strftime("%H:%M:%S")
                datos_salida = (cc, nombre, porteria, hora, "true")
                azureSQL.insert_salida(datos_salida)
                azureSQL.disponible_ingreso(cc)

            elif decision == "pendiente":
                fecha = datetime.now().strftime("%d-%m-%Y")
                hora = datetime.now().strftime("%H:%M:%S")
                datos_salida = (cc, nombre, porteria_pc, hora, fecha)
                azureSQL.insert_pendientes_salida(datos_salida)

            self.le_nombre.clear()  # Nombre
            self.le_serie.clear()  # Serie
            self.le_marca.clear()  # Marca
            self.le_color.clear()
            QDialog.close(self)
        else:
            self.msg_campos_vacios()

    def bt_Cancelar(self):
        QMessageBox.information(None, "Cancelar", u'Registro Cancelado',
                                QMessageBox.Ok,
                                QMessageBox.Ok)
        self.le_nombre.clear()  # Nombre
        self.le_serie.clear()  # Serie
        self.le_marca.clear()  # Marca
        self.le_color.clear()
        conexion("cancelar")
        leer_cedula()
        lista.clear()
        QDialog.close(self)

    def bt_Eliminar_img(self):
        cc = self.le_cc.text()
        Datalake.delete_file_from_directory(cc)
        self.lb_img.setPixmap(QPixmap("escudo2.png"))

    def bt_Tomar_foto(self):
        self.camara.exec_()

        """cedula = self.le_cc.text()
        camara = cv2.VideoCapture(0)
        sg.theme('DarkGreen5')
        layout = [[sg.Image(filename='', key='-image-')],
                  [sg.Button('Tomar Fotografia'), sg.Button('Salir')]]

        window = sg.Window('CAMARA FACIALIX',
                           layout,
                           no_titlebar=False,
                           location=(0, 0))

        image_elem = window['-image-']

        while camara.isOpened():
            event, values = window.read(timeout=0)
            ret, frame = camara.read()
            cv2.imshow("Foto", frame)
            cv2.waitKey()
            if event in ('Exit', None):
                break

            elif event == 'Tomar Fotografia':
                ruta = sg.popup_get_folder(title=str(cedula), message="Camara")
                cv2.imwrite(ruta + "/" + str(date.today()) + ".png", frame)
            if not ret:
                break

        cv2.destroyAllWindows()"""

    def le_enabled(self):

        self.le_serie.setEnabled(False)
        self.le_serie.setFont(QF("Sanserif", 10, weight=QF.Bold))
        self.le_marca.setEnabled(False)
        self.le_marca.setFont(QF("Sanserif", 10, weight=QF.Bold))
        self.le_color.setEnabled(False)
        self.le_color.setFont(QF("Sanserif", 10, weight=QF.Bold))
        self.le_porteria.setEnabled(False)
        self.le_porteria.setFont(QF("Sanserif", 10, weight=QF.Bold))
        self.le_hora.setEnabled(False)
        self.le_hora.setFont(QF("Sanserif", 10, weight=QF.Bold))
        self.bt_eli_img.setEnabled(False)
        self.bt_foto.setEnabled(False)

    def habilitar(self):
        self.le_nombre.setEnabled(True)
        self.le_nombre.setFont(QF("Sanserif", 10))
        self.le_serie.setEnabled(True)
        self.le_serie.setFont(QF("Sanserif", 10))
        self.le_marca.setEnabled(True)
        self.le_marca.setFont(QF("Sanserif", 10))
        self.le_color.setEnabled(True)
        self.le_color.setFont(QF("Sanserif", 10))
        self.le_porteria.setEnabled(False)
        self.le_porteria.setFont(QF("Sanserif", 10))
        self.le_hora.setEnabled(False)
        self.le_hora.setFont(QF("Sanserif", 10))
        self.bt_eli_img.setEnabled(True)

    def msg_campos_vacios(self):
        QMessageBox.warning(None, "Vacio", u'Debes ingresar todos los campos',
                            QMessageBox.Ok,
                            QMessageBox.Ok)


class Lista(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Ui/lista.ui", self)
        self.bt_lista.clicked.connect(self.bt_Ok)

    def showEvent(self, event):
        fila_lista = 0
        cedula, desicion = leer_cedula()
        lista.clear()
        self.tb_lista.setRowCount(0)

        if desicion == "pendiente":
            self.lb_lista.setText("Lista de pendientes")
            self.lb_lista.setFont(QF("Sanserif ", 16))
            self.lb_lista.setStyleSheet('color:blue')
            self.tb_lista.setHorizontalHeaderLabels(['Cédula', 'Nombre', 'Hora', 'Portería', 'Fecha'])
            pendientes = azureSQL.select_pendientes()
            for item in pendientes:
                self.tb_lista.insertRow(fila_lista)
                col_lista = 0
                for j in range(1, 6):
                    celda = QTableWidgetItem(str(item[j]))
                    self.tb_lista.setItem(fila_lista, col_lista, celda)
                    col_lista += 1
                fila_lista += 1

        elif desicion == "entrada":
            self.lb_lista.setText("Registrados")
            self.lb_lista.setFont(QF("Sanserif", 16))
            self.lb_lista.setStyleSheet('color:green')
            self.tb_lista.setHorizontalHeaderLabels(['Cédula', 'Nombre', 'Serie', 'Marca', 'Color'])
            registros = azureSQL.select_registro()
            for item in registros:
                self.tb_lista.insertRow(fila_lista)
                col = 0
                for j in range(1, 6):
                    celda = QTableWidgetItem(str(item[j]))
                    self.tb_lista.setItem(fila_lista, col, celda)
                    col += 1
                fila_lista += 1

    def bt_Ok(self):
        QDialog.close(self)

class Camara(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Ui/camara1.ui", self)
        #self.dialog = uic.loadUi('Ui/camara.ui')
        self.webcam = cv2.VideoCapture(0)
        self.bt_foto.clicked.connect(self.bt_Foto)

     #   self.show_frame()
      #  self.timer = QtCore.QTimer(self.dialog)
     #   self.timer.timeout.connect(self.show_frame)
     #   self.timer.start(1)

       # self.mostrar_imagen()
       # self.bt_foto.clicked.connect(self.bt_Foto)



    def showEvent(self, event):
        self.lb_img.setPixmap(QPixmap("prueba.png"))

    def bt_Foto(self):
        ok, img = self.webcam.read()

        while ok:
            if not ok:
                break

            cv2.imwrite("22069221.jpeg", img)

            self.lb_img.setPixmap(QPixmap("22069221.jpeg"))
            cv2.waitKey(100)

        self.webcam.release()

"""
    def showEvent(self, event):
        camara = cv2.VideoCapture(0)
        while True:
            retval, img = camara.read()
            if img is None:
                break
            cv2.imwrite("prueba.png", img)
            self.lb_img.setPixmap(QPixmap("prueba.png"))
            cv2.waitKey(100)

        camara.release()
        cv2.destroyAllWindows()
"""
  #  def bt_Foto(self):





if __name__ == "__main__":
    app = QApplication(sys.argv)
    principal = Principal()
    principal.show()
    app.exec_()
