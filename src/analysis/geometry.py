import numpy as np

class GeometryUtils:
    @staticmethod
    def calculate_angle(a,b,c):
        a = np.array(a[1:3])
        b = np.array(b[1:3])
        c = np.array(c[1:3])

        radians = np.arctan2(c[1]-b[1], c[0]-b[0])- np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return int(angle)

    @staticmethod
    def get_cords(landmarks, part_id):
        if len(landmarks) > part_id:
            return landmarks[part_id]
        return None
