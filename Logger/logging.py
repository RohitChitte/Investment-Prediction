from datetime import datetime
import os

class App_Logger:
    def __init__(self):
        self.file_object = open(os.getcwd()[:63]+"\Logger\log.txt", 'a')

    def log(self,log_message):
        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        self.file_object.write(
            str(self.date) + "/ " + str(self.current_time) + "\t" + log_message +"\n")

if __name__== "__main__":
    obj = App_Logger()
    obj.log("Testing log function")