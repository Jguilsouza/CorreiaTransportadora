import sys
import cv2
import pyqtgraph as pg
import time
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QDateTime
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget,QHBoxLayout, QLineEdit, QCalendarWidget, QGridLayout, QListWidget
from Inicializacao import *

"""
Este arquivo eh responsavel por gerar as telas do supervisorio nao estatica

"""

paleta_azul_cinza = '#384759'
paleta_azul_escuro = '#111826'
fundo = '#F2F2F2'

import numpy as np

def Ler_Imagem():
    while True:
        try:
            with open('./1234.pkl', 'rb') as f:
                frame = pickle.load(f)
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                yield qt_image
            time.sleep(0.01)  # Aguarda um curto período para evitar sobrecarga
        except:
            pass

class ImageReader(QThread):
    new_image = pyqtSignal(QImage)

    def run(self):
        for qt_image in Ler_Imagem():
            self.new_image.emit(qt_image)
            
class Tela_Desalinhamento(QWidget):
    
    def __init__(self):
        super().__init__()

        self.camera = QLabel()
        self.camera_rasgo = QLabel()
        self.camera_rasgo.setStyleSheet('background-image: url("foto.jpeg")')

        self.image_reader = ImageReader()
        self.image_reader.new_image.connect(self.Update_Frame)
        self.image_reader.start()

        self.titulo = QLabel('DESALINHAMENTO')
        self.titulo.setStyleSheet('color: black; text-decoration: underline; font: 400;')

        self.titulo_ras = QLabel('FUROS E RASGOS')
        self.titulo_ras.setStyleSheet('color: black; text-decoration: underline; font: 400;')

        self.camera.setFixedSize(540, 304)  # Defina a largura e altura fixa
        self.camera_rasgo.setFixedSize(540, 304)  # Defina a largura e altura fixa
        
        # Criar um layout horizontal e um vertical 
        tela = QVBoxLayout()
        cameras = QVBoxLayout()
        cameras_ras = QVBoxLayout()
        analise_camera = QHBoxLayout()

        cameras_ras.addWidget(self.titulo_ras)
        cameras_ras.addWidget(self.camera_rasgo)
        analise_camera.addLayout(cameras_ras)
        
        cameras.addWidget(self.titulo)
        cameras.addWidget(self.camera)
        # cameras.addWidget(self.camera_rasgo)
        analise_camera.addLayout(cameras)

        tela.addLayout(analise_camera)

        # Definir o layout para o widget
        self.setLayout(tela)
        
    def Update_Frame(self, qt_image):
        pixmap = QPixmap.fromImage(qt_image)
        self.camera.setPixmap(pixmap)

    def Close_Event(self, event):
        self.video_thread.quit()
        self.video_thread.wait()
        event.accept()


'''-----------------------------------------------------------tela dados historicos-----------------------------------------------------------------------------'''

class tela_dados_historicos(QWidget):
    def __init__(self):
        super().__init__()

        self.graph_widget = GraphWidget()

        lista = QListWidget()

        # Botão para abrir o calendário
        calendario_botao_inicio = QPushButton('Calendário')
        calendario_botao_inicio.clicked.connect(self.abrir_calendario_inicio)

        # Botão para adicionar a data ao gráfico
        enviar_botao = QPushButton('Enviar')
        enviar_botao.clicked.connect(self.adicionar_data_grafico)

        inicio = QLabel('INICIO')

        self.edit_inicio = QLineEdit()

        fim = QLabel('FIM')

        calendario_botao_fim = QPushButton('Calendário')
        calendario_botao_fim.clicked.connect(self.abrir_calendario_final)

        self.edit_fim = QLineEdit()

        # Layout
        orientacao_grafico_botao = QHBoxLayout(self)
        orientacao_botao = QGridLayout()
        vertical_grafico_edit = QHBoxLayout()

        vertical_grafico_edit.addWidget(lista)
        vertical_grafico_edit.addWidget(self.graph_widget)

        orientacao_botao.addWidget(inicio, 0, 0)
        orientacao_botao.addWidget(calendario_botao_inicio, 0, 1)
        orientacao_botao.addWidget(self.edit_inicio, 1, 0, 1, 2)
        orientacao_botao.addWidget(fim, 2, 0)
        orientacao_botao.addWidget(calendario_botao_fim, 2, 1)
        orientacao_botao.addWidget(self.edit_fim, 3, 0, 1, 2)
        orientacao_botao.addWidget(enviar_botao, 4, 0, 1, 2)

        orientacao_grafico_botao.addLayout(vertical_grafico_edit)
        orientacao_grafico_botao.addLayout(orientacao_botao)

        # Calendário
        self.calendario_inicio = QCalendarWidget()
        self.calendario_inicio.clicked.connect(self.selecionar_data_inicio)

        self.calendario_final = QCalendarWidget()
        self.calendario_final.clicked.connect(self.selecionar_data_final)

    def abrir_calendario_inicio(self):
        self.calendario_inicio.show()

    def abrir_calendario_final(self):
        self.calendario_final.show()

    def selecionar_data_inicio(self, date):
        data = date.toString("dd-MM-yyyy")
        self.edit_inicio.setText(data)
        self.calendario_inicio.hide()

    def selecionar_data_final(self, date):
        data = date.toString("dd-MM-yyyy")
        self.edit_fim.setText(data)
        self.calendario_final.hide()

    def adicionar_data_grafico(self):
        data = self.edit_inicio.text()
        if data:
            self.graph_widget.adicionar_data(data)

class GraphWidget(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        self.vp_data = []

        self.addLegend(offset=(10, 10))

        # Plot vermelho para VM
        self.vm_plot = self.plot([], pen='r', name="VM")

    def adicionar_data(self, data):
        dt = QDateTime.fromString(data, "dd-MM-yyyy")
        self.vp_data.append((dt, len(self.vp_data)))
        self.atualizar_eixo_x()

    def atualizar_eixo_x(self):
        ticks = [(i, dt.toString("dd-MM-yyyy")) for dt, i in self.vp_data]

        # Atualiza os ticks do eixo Y
        self.getPlotItem().getAxis('left').setTicks([ticks])

        # Atualiza os dados do gráfico
        self.vm_plot.setData([i for _, i in self.vp_data])
        