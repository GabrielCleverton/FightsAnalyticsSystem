import cv2
import mediapipe as mp

class PoseDetector:
    def __init__(self, static_image_mode= False, model_complexity = 1, smooth_landmarks = True ):
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            static_image_mode = static_image_mode,
            model_complexity = model_complexity,
            smooth_landmarks = smooth_landmarks,
            min_detection_confidence= 0.5,
            min_tracking_confidence= 0.5
        )

    def find_pose(self, img, draw = True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img_rgb)

        if self.results.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(
                    img,
                    self.results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )
        return img

    def find_position(self, img):
        lm_list = []
        if self.results.pose_landmarks:
            for id_landmark, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lm_list.append([id_landmark, cx, cy, lm.z])

        return lm_list

if __name__ == "__main__":
        cap = cv2.VideoCapture(0)
        detector = PoseDetector()

        print("Iniciando teste da câmera... (Aperte 'q' na janela do vídeo para sair)")

        while True:
            success, img = cap.read()
            if not success:
                print("Não consegui ler a câmera.")
                break
            img = detector.find_pose(img)
            lm_list = detector.find_position(img)
            if len(lm_list) != 0:
                print(f"Nariz detectado em: X={lm_list[0][1]}, Y={lm_list[0][2]}")

            # Mostra o resultado na tela
            cv2.imshow("Analisando movimentos:", img)

            #Sair do loop apertando q
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()




