from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import pymongo
import urllib.parse
import json


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

        numberOfAllScans = 0

        for room in self.data.find():
            numberOfAllScans += len(room["scan_results"])
            for scan in room["scan_results"]:
                self.Y.append(room["name"])
                for network in scan:
                    self.allNetworks.add(network["ssid"])

        df = pd.DataFrame(-100, index=range(numberOfAllScans), columns=list(self.allNetworks))
        self.Y = pd.DataFrame(self.Y)

        index = 0

        for room in self.data.find():
            for scan in room["scan_results"]:
                for network in scan:
                    df.loc[index, network["ssid"]] = network["rssi"]
                    # print("DLA SSID: ", network["ssid"] , " MOC: ", network["rssi"], flush=True)
                index += 1

        self.Y = self.Y.values.ravel()

        self.knn.fit(df, self.Y)
        self.isTrained = True

    def getDeviceLocation(self, scanResults):
        X_predict = pd.DataFrame(-100, index=range(1), columns=list(self.allNetworks))
        
        for scan in scanResults.scan_results:
            if scan.ssid in self.allNetworks:
                X_predict.loc[0, scan.ssid] = scan.rssi

        tmp = self.knn.predict(X_predict)
        print("RESULTS: ", tmp, flush=True)
        
        return tmp[0]

if __name__ == "__main__":
    RM = RoomMapper()
    RM.train()
    print(RM.getDeviceLocation(None))
