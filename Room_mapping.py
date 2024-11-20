import pandas as pd
import pymongo
from sklearn.neighbors import KNeighborsClassifier


class RoomMapper:
    def __init__(self):
        self.knn = KNeighborsClassifier(n_neighbors=1)
        self.isTrained = False
        self.allNetworks = set()

        self.client = pymongo.MongoClient("mongodb://root:example@mongo:27017/")
        self.db = self.client["beacon_blink"]
        self.data = self.db["rooms"]

        self.X = []
        self.Y = []

    def trained(self):
        return self.isTrained

    def train(self):
        print("MODEL IS TRAINING", flush=True)

        number_of_all_scans = 0

        for room in self.data.find():
            number_of_all_scans += len(room["scan_results"])
            for scan in room["scan_results"]:
                self.Y.append(room["_id"])
                for network in scan:
                    self.allNetworks.add(network["bssid"])

        df = pd.DataFrame(-100, index=range(number_of_all_scans), columns=list(self.allNetworks))
        self.Y = pd.DataFrame(self.Y)

        index = 0

        for room in self.data.find():
            for scan in room["scan_results"]:
                for network in scan:
                    df.loc[index, network["bssid"]] = network["rssi"]
                    # print("DLA BSSID: ", network["bssid"] , " MOC: ", network["rssi"], flush=True)
                index += 1

        self.Y = self.Y.values.ravel()

        self.knn.fit(df, self.Y)
        self.isTrained = True

    def get_device_location(self, scan_results):
        X_predict = pd.DataFrame(-100, index=range(1), columns=list(self.allNetworks))

        for scan in scan_results.scan_results:
            if scan.bssid in self.allNetworks:
                X_predict.loc[0, scan.bssid] = scan.rssi

        tmp = self.knn.predict(X_predict)
        print("RESULTS: ", tmp, flush=True)

        return tmp[0]


if __name__ == "__main__":
    RM = RoomMapper()
    RM.train()
    print(RM.get_device_location(None))
