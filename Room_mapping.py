from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

class RoomMapper:
    def __init__(self):
        self.knn = KNeighborsClassifier(n_neighbors=1)
        self.isTrained = False
        self.x = None
        self.y = None

    def trained(self):
        return self.isTrained
    
    def train(self):
        self.isTrained = True

        self.data = {
        'x': [0, 1, 0, 1],
        'y': [0, 0, 1, 1],
        'SSID1': [-30, -40, -35, -45],
        'SSID2': [-50, -60, -55, -65]
    }
        self.df = pd.DataFrame(self.data)

        # pobieranie danych z mongodb i trenowanie
        pass

    def getDeviceLocation(self, data):
        # tmp = self.knn.predict(data)
        return "d17"


if __name__ == "__main__":
    print("NO I MAIN")
