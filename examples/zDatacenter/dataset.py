import os
import csv
import torch
from deepproblog.dataset import Dataset
from deepproblog.query import Query
from problog.logic import Term, Constant

path = os.path.dirname(os.path.abspath(__file__))

class SensorDataset(Dataset):
    def __init__(self, subset):
        self.subset = subset  # "train" or "test"
        self.data = []
        # CSV file format：
        # Start_timestamp,End_timestamp,Temperature,CPU_load,Humidity,Anomaly
        with open("{}/data/{}.csv".format(path, subset)) as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header
            for row in reader:

                # start_timestamp, end_timestamp, temperature, cpu_load, humidity, label = [l.strip() for l in row]
                _, _, temperature, cpu_load, humidity, label = [l.strip() for l in row]
                temperature = float(temperature)
                cpu_load = float(cpu_load)
                humidity = float(humidity)
                # self.data.append((temperature, cpu_load, humidity, label))
                self.data.append((temperature, cpu_load, label))

    # def label_to_float(self, label):
    #     return 0.0 if label == "False" else 1.0
    # def to_query(self, i):
    #     # temperature, cpu_load, humidity, label = self.data[i]
    #     temperature, label = self.data[i]
    #     # return Query(Term("anomaly", Constant(temperature), Constant(cpu_load), Constant(humidity), Constant(self.label_to_float(label))))
    #     # return Query(Term("anomaly", Constant(temperature), Constant(self.label_to_float(label))))
    #     return Query(Term("anomaly", Constant(temperature), Constant(label)))

    def to_query(self, i):
        temperature, cpu_load, label = self.data[i]
        # 假设原始标签为字符串，如 "True" -> anomaly, "False" -> no_anomaly
        label_term = Term(1) if label == "True" else Term(0)
        return Query(Term("anomaly", Constant(temperature),label_term))

    def __len__(self):
        return len(self.data)

train_dataset = SensorDataset("train")
test_dataset = SensorDataset("test")