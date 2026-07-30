import datetime

class DateHelper:

    def __init__(self):
        pass

    def data_atual_texto(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')