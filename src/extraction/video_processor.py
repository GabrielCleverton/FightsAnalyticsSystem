import cv2
import json
import os
import time



from src.extraction.pose_detector import PoseDetector
from src.database.db_manager import DBMANAGER
from src.analysis.geometry import GeometryUtils

class VideoProcessor:
    def __init__(self, video_source = 0):
        self.video_source = video_source
        self.detector = PoseDetector()
        self.db = DBMANAGER()
        self.geo = GeometryUtils()
    def processar(self):
        cap = cv2.VideoCapture(self.video_source)
        if isinstance(self.video_source, int):
            nome_video = f"WebCam Ao vivo{int(time.time())}"
        else:
            nome_video = os.path.basename(self.video_source)
        print(f"Iniciando gravação: {nome_video}")

        luta_id = self.db.iniciar_luta(nome_video)
        print(f"Luta ID {luta_id} iniciada")

        frame_count = 0

        while True:
            sucess, img = cap.read()
            if not sucess:
                print("Fim do vídeo ou erro na câmera")
                break
            frame_count = frame_count+1

            img = self.detector.find_pose(img, draw = True)
            lm_list = self.detector.find_position(img)
            if len(lm_list):
                ombro_dir = self.geo.get_cords(lm_list, 12)
                cotovelo_dir = self.geo.get_cords(lm_list, 14)
                punho_dir = self.geo.get_cords(lm_list, 16)
                ombro_esq = self.geo.get_cords(lm_list,11)
                cotovelo_esq = self.geo.get_cords(lm_list, 13)
                punho_esq = self.geo.get_cords(lm_list,15)

                quadril_y = (lm_list[23][2]+lm_list[24][2])/2

                ang_direito = self.geo.calculate_angle(ombro_dir, cotovelo_dir, punho_dir)
                ang_esquerdo = self.geo.calculate_angle(ombro_esq,cotovelo_esq,punho_esq)

                self.db.salvar_frame(
                    luta_id=luta_id,
                    frame_num=frame_count,
                    person_id=0,
                    ang_dir=ang_direito,
                    ang_esq=ang_esquerdo,
                    alt_quadril=quadril_y,
                    json_dump=json.dumps(lm_list)
                )

                cv2.putText(img, str(int(ang_direito)), (cotovelo_dir[1] - 50, cotovelo_dir[2]),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                cv2.putText(img, str(int(ang_esquerdo)), (cotovelo_esq[1] + 20, cotovelo_esq[2]),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

                # Placar no topo
                cv2.rectangle(img, (0, 0), (250, 80), (0, 0, 0), cv2.FILLED)
                cv2.putText(img, f"Frame: {frame_count}", (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
                cv2.putText(img, "Gravando...", (10, 60), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

                # Mostra a janela
            cv2.imshow("Sistema de Analise de Luta", img)

            # Aperte 'q' para sair
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    # --- BLOCO DE EXECUÇÃO ---
if __name__ == "__main__":
        # Teste com Webcam (0)
    processor = VideoProcessor(0)
    processor.processar()




