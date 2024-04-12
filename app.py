import sys
import pyqtgraph as pg
from multiprocessing import Process
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QDateTime
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget,QHBoxLayout, QDockWidget, QStyleFactory, QSpacerItem, QSizePolicy,QDoubleSpinBox, QLineEdit, QCalendarWidget, QGridLayout, QListWidget
from PyQt6.QtSvgWidgets import QSvgWidget
from func_sup import *

class janela(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar a janela principal
        self.setWindowTitle('Supervisorio')
        self.setGeometry(100, 100, 800, 600)  # Definir tamanho inicial (opcional)

        # Adicionar a barra lateral à janela principal
        self.barra_lateral()

        # Adicionar a barra de navegação à janela principal
        barra_navegacao = self.cabecalho()
        # Criar uma barra de ferramentas Adicionar a barra de navegação à barra de ferramentas
        toolbar = self.addToolBar("Barra de Navegação")
        toolbar.setMovable(False)
        toolbar.addWidget(barra_navegacao)

        # Adicionar a barra de status à janela principal
        self.status_bar()


        
        self.informacoes_widget = Tela_Desalinhamento()
        # self.tela_dadoshistoricos = None
 
        # Criar um layout vertical para organizar os widgets
        layout = QVBoxLayout()

        layout.addWidget(self.informacoes_widget)
        
        # Criar um widget central para a janela principal e definir o layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        central_widget.setStyleSheet(f'background-Color: {fundo}')
        self.setCentralWidget(central_widget)
        
    ''' -------------------------------barra de status -------------------------------'''

    def status_bar(self):

        self.controlador = controlador()
        # Criar uma barra de status e adicionar uma mensagem inicial
        self.statusBar = self.statusBar()

        # Criar um QHBoxLayout e um QWidget para conter o QLineEdit
        orivelocidade = QHBoxLayout()
        widget_status = QWidget()

        #coloca o QHBoxLayout dentro do widget
        widget_status.setLayout(orivelocidade)

        # Adicionar um QLineEdit ao orivelocidade
        label_velocidade = QLabel('VELOCIDADE:')
        label_velocidade.setStyleSheet('color: white')
        input_velocidade = QDoubleSpinBox()
        input
        orivelocidade.addWidget(label_velocidade)
        orivelocidade.addWidget(input_velocidade)

        # Remover os limites definindo valores muito grandes e muito pequenos
        input_velocidade.setRange(0, 60)
        input_velocidade.setStyleSheet("color: white")

        # Conectar o sinal 'valueChanged' do QDoubleSpinBox à função de envio
        input_velocidade.valueChanged.connect(self.controlador.esp_velocidade) # usamos valuechanged toda vez que queremos que um valor seja alterado junto com a alteracao do usuario

        # Adicionar o QWidget à barra de status
        self.statusBar.addPermanentWidget(widget_status)

        # Configurar o QLineEdit conforme necessário

        input_velocidade.setFixedSize(70, 50)# Ajuste o tamanho conforme necessário

        #estilo do status bar (barra inferior)
        self.statusBar.setMinimumHeight(100)
        self.statusBar.setStyleSheet(f'background-color: {paleta_azul_cinza};')

    ''' -------------------------------barra de lateral -------------------------------'''  

    def barra_lateral(self):
        # Criar botões de exemplo para a barra lateral
        desalinhamento_botao = QPushButton('Desalinhamento')

        dados_historico = QPushButton('Dados Historicos')
        dados_historico.clicked.connect(self.mudar_tela_dadoshistoricos)

        furos_rasgos_botao = QPushButton('Furos e Rasgos')

        # Criar um botão para alternar entre fullscreen e normal
        fullscreen_button = QPushButton('Toggle Fullscreen')
        fullscreen_button.clicked.connect(self.toggle_fullscreen)

        #define os estilos dos botoes de desalinhamento e de furos e rasgos
        fullscreen_button.setStyleSheet(f'background-Color: {paleta_azul_cinza}; color: white; border-radius: 10px')
        desalinhamento_botao.setStyleSheet(f'background-Color: {paleta_azul_cinza};color: white; border-radius: 10px;')
        dados_historico.setStyleSheet(f'background-Color: {paleta_azul_cinza};color: white; border-radius: 10px;')

        furos_rasgos_botao.setStyleSheet(f'background-Color: {paleta_azul_cinza};color: white; border-radius: 10px')

        #define um tamanho minimo para os botoes
        fullscreen_button.setMinimumSize(80, 50)
        dados_historico.setMinimumSize(80, 50)
        desalinhamento_botao.setMinimumSize(100, 150)
        furos_rasgos_botao.setMinimumSize(100, 150)

        # Criar um layout vertical para os botões
        layout_lateral = QVBoxLayout()

        layout_lateral.addWidget(fullscreen_button)
        layout_lateral.addWidget(desalinhamento_botao)
        layout_lateral.addWidget(furos_rasgos_botao)
        layout_lateral.addWidget(dados_historico)

        # Criar um widget para a barra lateral
        lateral_widget = QWidget()
        lateral_widget.setLayout(layout_lateral)
        lateral_widget.setStyleSheet(f'background-Color: {paleta_azul_escuro}')

        # Criar um QDockWidget para envolver o widget lateral
        dock_widget = QDockWidget("MENU")

        # Remover a capacidade de fechar e mover o QDockWidget
        dock_widget.setFeatures(QDockWidget.DockWidgetFeature(0))  # Nenhuma característica

        dock_widget.setStyleSheet(f'background-Color: {paleta_azul_escuro}; color: white')
        dock_widget.setMaximumWidth(200)  # Definir a largura máxima da barra lateral

        dock_widget.setWidget(lateral_widget)
        # Adicionar o QDockWidget à janela principal
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock_widget)

    ''' -------------------------------barra de navegacao -------------------------------'''

    def cabecalho(parent):
        # Criar widget para a barra de navegação
        nav_widget = QWidget(parent)
        orientador_QV = QVBoxLayout()
        pesquisador_QV = QVBoxLayout()
        nav_layout = QHBoxLayout(nav_widget)

        # Adicionar um espaço flexível no início para centralizar os elementos
        nav_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        # Adicionar label "Projeto Câmeras Inteligentes na Indústria 4.0"
        label_projeto = QLabel('Projeto Câmeras Inteligentes na Indústria 4.0')
        label_projeto.setStyleSheet('color: white; margin: 15px; margin-bottom: 0px')
        nav_layout.addWidget(label_projeto)

        #titulo do orientador
        titulo_orientador = QLabel('Orientadores:')
        titulo_orientador.setStyleSheet('color: white; margin: 15px; margin-bottom: 0px')

        #label do orientador
        label_orientador = QLabel('Marco Antônio e Rogério Passos')
        label_orientador.setStyleSheet('color: white; margin: 15px; margin-bottom: 0px; margin-top: 0px')

        orientador_QV.addWidget(titulo_orientador)
        orientador_QV.addWidget(label_orientador)

        nav_layout.addLayout(orientador_QV)

        # Criar widget para desenhar o SVG
        svg_widget = QSvgWidget('./logo.svg')

        # Define uma porcentagem para o tamanho mínimo do SVG
        porcen_logogain = 0.2

        # Define a porcentagem setada anteriormente
        svg_widget.setFixedSize(int(svg_widget.sizeHint().width() * porcen_logogain),
                                int(svg_widget.sizeHint().height() * porcen_logogain))  # Definir o tamanho mínimo com base no SVG

        # Adicionar o widget SVG ao layout horizontal
        nav_layout.addWidget(svg_widget)

        # Adicionar label dos pesquisadores
        titulo_pesquisador = QLabel('Pesquisadores')
        titulo_pesquisador.setStyleSheet('color: white; margin: 15px; margin-bottom: 0px')
        label_pesquisadores = QLabel('Arthur José, Filipe Gomes,\nJoão Lourenço, Lucas Cesar')
        label_pesquisadores.setStyleSheet('color: white; margin: 15px; margin-bottom: 0px; margin-top: 0px')
        
        titulo_coordenador = QLabel('Coordenador:\nLeonardo Gonçalves')
        titulo_coordenador.setStyleSheet('color: white; margin: 15px; margin-bottom: 0px')

        pesquisador_QV.addWidget(titulo_pesquisador)
        pesquisador_QV.addWidget(label_pesquisadores)

        nav_layout.addLayout(pesquisador_QV)
        nav_layout.addWidget(titulo_coordenador)

        # Adicionar um espaço flexível no final para centralizar os elementos
        nav_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))


        # Definir o layout da barra de navegação como o layout da barra de navegação
        nav_widget.setLayout(nav_layout)

        # Definir a cor de fundo da barra de navegação
        nav_widget.setStyleSheet(f'background-Color: {paleta_azul_cinza}')

        return nav_widget
        

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def mudar_tela_dadoshistoricos(self):
        
        self.tela_dadoshistoricos = tela_dados_historicos()
        self.tela_dadoshistoricos.show()

#Função para Inicialização do Pyqt de maneira que permita a utilização do multiprocesso
def StartTela():
    app = QApplication(sys.argv)
    window = janela()
    window.show()
    sys.exit(app.exec())
    
if __name__ == '__main__':
    Rede = Process(target= video_thread)
    TelaPyqt = Process(target=StartTela)
    
    Rede.start()
    TelaPyqt.start()
    
