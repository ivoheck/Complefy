class Sallybus():
    #Every list contains a tupel of start and end time in minutes a a given appointment
    def __init__(self):
        self.monday = []
        self.tuesday = []
        self.wednesday = []
        self.thursday = []
        self.friday = []
        self.saturday = []
        self.sunday = []

    def __str__(self):
        return (
        f"monday: {self.monday}, "
        f"tuesday: {self.tuesday}, "
        f"wednesday: {self.wednesday}, "
        f"thursday: {self.thursday}, "
        f"friday: {self.friday}, "
        f"saturday: {self.saturday}, "
        f"sunday: {self.sunday}"
        )

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

    def as_dict(self):
        return {
            'monday': self.monday,
            'tuesday' :self.tuesday,
            'wednesday' : self.wednesday,
            'thursday' : self.thursday,
            'friday' : self.friday,
            'saturday' : self.saturday,
            'sunday' : self.sunday
        }
