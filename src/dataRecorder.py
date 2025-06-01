import csv

class DataRecorder:
    def __init__(self, filename="car_data.csv"):
        self.filename = filename
        self.data = []

    def record(self, sensors: list[float], action: str):
        self.data.append(sensors + [action])

    def save(self):
        with open(self.filename, mode="w", newline="") as f:
            writer = csv.writer(f)
            if not self.data:
                return
            writer.writerow([f"sensor_{i}" for i in range(len(self.data[0]) - 1)] + ["action"])
            writer.writerows(self.data)