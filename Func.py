import numpy as np
import cv2
from ultralytics import YOLO
from collections import deque

"""
este arquivo eh responsavel por fazer o processamento do frame gerando um frame anotado
"""

class YOLOSegmentation:
    #no lugar do yolov8n-seg.pt colocamos best.pt
    def __init__(self, model_path='best.pt', task='segment'):
        self.model = YOLO(model_path, task=task)
        self.valores_mm = [deque(maxlen=20), deque(maxlen=20)]

    
    def Remove_Outliers(self, data, iqr_multiplier=0.8):
        ''' 
        Função para tratamento dos dados removendo os outliers
        '''
        Q1, Q3 = np.percentile(data, [25, 75])
        IQR = Q3 - Q1
        lower_bound, upper_bound = Q1 - iqr_multiplier * IQR, Q3 + iqr_multiplier * IQR
        return np.array([value for value in data if lower_bound <= value <= upper_bound])

    
    def Process_Frame(self, frame):
        '''
        Esta função recebe os frames da câmera e utiliza do modelo neural treinado para verificar e retornar o frame anotado
        '''
        resultados = self.model(frame, max_det=1, save=False, retina_masks=True, show_labels=False, show_conf=False,
                                show_boxes=True, device= 0, imgsz=640)[0]
        annotated_frame = resultados.plot(conf=False, labels=False)

        for i, r in enumerate(resultados):
            for i, box in enumerate(r.boxes):
                masks_data_array = r.masks.data.cpu().numpy()[i, :, :]
                eixoy = np.count_nonzero(masks_data_array, axis=0)
                eixox = np.count_nonzero(masks_data_array, axis=1)
                maior = max(eixox)
                Referencia = max(eixoy)
                ValormmRef = Referencia / 46
                Valormm = (maior / ValormmRef)
                self.valores_mm[i].append(Valormm)

                if len(self.valores_mm[i]) >= 1:
                    coords = r.boxes.xyxy.data.cpu().numpy()[0]
                    x1, y1, x2, y2 = coords.tolist()
                    No_outliers = self.Remove_Outliers(self.valores_mm[i])
                    self.mediafinal = np.mean(No_outliers)
                    annotated_frame = cv2.putText(annotated_frame, str(round(self.mediafinal, 2)),
                                                   (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                                   (255, 255, 255), 2, cv2.LINE_AA)
        return annotated_frame