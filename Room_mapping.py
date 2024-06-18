from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import pymongo
import urllib.parse
import json


class RoomMapper:
    def __init__(self):
        self.knn = KNeighborsClassifier(n_neighbors=2)
        self.isTrained = False
        self.allNetworks = set()

        # self.client = pymongo.MongoClient("mongodb://root:example@deployment_default:27017/beacon_blink?authSource=admin")
        # self.db = self.client["beacon_blink"]
        
        self.X = []
        self.Y = []

    def trained(self):
        return self.isTrained
    
    def train(self):
        # print("SERVER INFO: ", self.client.server_info())
        # print("DATABASE: ", self.client.list_database_names())

        # self.data = self.db["rooms"]

        with open('rooms_3.json', 'r') as file:
            self.data = json.load(file)

        numberOfAllScans = 0

        for room in self.data:
            numberOfAllScans += len(room["scan_results"])
            for scan in room["scan_results"]:
                self.Y.append(room["name"])
                for network in scan:
                    self.allNetworks.add(network["ssid"])

        df = pd.DataFrame(-100, index=range(numberOfAllScans), columns=list(self.allNetworks))
        self.Y = pd.DataFrame(self.Y)

        index = 0
        for scanResults in self.data:
            for scan in scanResults["scan_results"]:
                for network in scan:
                    df.loc[index, network["ssid"]] = network["rssi"]
                index += 1

        self.Y = self.Y.values.ravel()

        self.knn.fit(df, self.Y)

        self.isTrained = True

    def getDeviceLocation(self, scanResults):
        
        with open('predict_room_2.json', 'r') as file:
            scanResults = json.load(file)

        X_predict = pd.DataFrame(-100, index=range(len(scanResults["scan_results"])), columns=list(self.allNetworks))

        for scan in scanResults["scan_results"]:
            if scan["ssid"] in self.allNetworks:
                X_predict.loc[0, scan["ssid"]] = scan["rssi"]

        tmp = self.knn.predict(X_predict)
        
        return tmp


if __name__ == "__main__":
    RM = RoomMapper()
    RM.train()
    print(RM.getDeviceLocation(None))
