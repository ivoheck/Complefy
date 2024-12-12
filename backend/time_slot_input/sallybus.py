class TimeFrame():
    start_time = 0
    end_time = 0

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
        if day == 'Montag':
            self.monday.append(time_frame)

        elif day == 'Dienstag':
            self.tuesday.append(time_frame)

        elif day == 'Mittwoch':
            self.wednesday.append(time_frame)

        elif day == 'Donnerstag':
            self.thursday.append(time_frame)

        elif day == 'Freitag':
            self.friday.append(time_frame)

        elif day == 'Samstag':
            self.saturday.append(time_frame)

        elif day == 'Sonntag':
            self.sunday.append(time_frame)
