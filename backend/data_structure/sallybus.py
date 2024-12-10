class TimeFrame():
    def __init__(self):
        self.start_hour
        self.start_minute

        self.end_hour
        self.end_minute

class Sallybus():
    def __init__(self):
        self.monday = []
        self.tuesday = []
        self.wednesday = []
        self.thursday = []
        self.friday = []
        self.saturday = []
        self.sunday = []

    def add_time_frame(self,day,time_frame):
        if day == 'monday':
            self.monday.append(time_frame)

        elif day == 'tuesday':
            self.tuesday.append(time_frame)

        elif day == 'wednesday':
            self.wednesday.append(time_frame)

        elif day == 'thursday':
            self.thursday.append(time_frame)

        elif day == 'friday':
            self.friday.append(time_frame)

        elif day == 'saturday':
            self.saturday.append(time_frame)

        elif day == 'sunday':
            self.sunday.append(time_frame)
