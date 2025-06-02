

class DataRecorder:

    def __init__(self, file_name, col_names):
        self.file = open(file_name, "w")
        self.cols = len(col_names)
        self.add_entry(col_names)

    def __del__(self):
        self.file.close()

    def add_entry(self, data_list: list[str]):
        assert len(data_list) == self.cols, "Invalid list"
        for i in range(len(data_list)-1):
            self.file.write(data_list[i] + ",")
        self.file.write(data_list[-1] + "\n")

