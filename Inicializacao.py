import cv2
from Func import *
import pickle
import struct

'''
Classe para comunicação com o ESP32 para controle da velocidade da correia
'''
class controlador():
    # esp = serial.Serial(port='COM10', baudrate=115200, timeout=0.1)
    def esp_velocidade(self, velocidade):
        # self.esp.write(bytes(f'{velocidade}', 'utf-8'))
        print(f'essa e a nova velocidade: {velocidade}')

'''
#Função para escrita com pickle, recebendo a imagem a ser anotada e o caminho 
'''
def storeData(data, path): 
    # initializing data to be stored in db 
    db = (data)
    # Its important to use binary mode 
    dbfile = open(path, 'wb')
    # source, destination 
    pickle.dump(db, dbfile)                   
    dbfile.close()
'''
 Função a ser chamada como segundo processo na função multiprocessing da main(app.py), nela é inicializada a câmera, os dados passam pela rede do arquivo FUNC.py
 O retorno da rede anotado é compilado com pickle para ser utilizado na tela  
'''
def video_thread(video_source=1, frame_width=640, frame_height=480):
    cap = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    Tframe = YOLOSegmentation() 
   
    while True:
        success, frame = cap.read()
        if success:
            annotated_frame = Tframe.Process_Frame(frame)
            
            a = pickle.dumps(annotated_frame)
            # Pack the length of the frame and the frame
            message = struct.pack("Q", len(a))+a
            storeData(annotated_frame, './1234.pkl')
            
        else:
            print("erro")
