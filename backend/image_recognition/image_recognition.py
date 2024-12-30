import easyocr
import cv2

class SallybusInfoFromImage:

    def __init__(self, image_path):
        self.image_path = image_path

        self.days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
        self.time = ['8.00', '9.00', '10.00', '11.00', '12.00', '13.00', '14.00', '15.00', '16.00', '17.00', '18.00', '19.00']

        self.coords = {}
        self.subjects = {}

    def get_info(self):
        results = self.get_raw_data()
        self.get_coords(results)

        #print(self.coords)
        self.find_subjects()

    def get_coords(self,results):
        for result in results:
            string_data = result[1]

            if string_data in self.days:
                #get center coordinate of days
                self.coords[string_data] = self.get_center_point(result[0])
                print(string_data + ' found')

            if string_data in self.time:
                #get left up coordinate of time
                self.coords[string_data] = result[0][0]
                print(string_data  + ' found')

    def find_subjects(self):
        image = cv2.imread(self.image_path)

        y_end = int(self.coords['19.00'][1])
        print('y_end ', y_end)
        min_count = 10

        for day in self.days:
            print(day)
            day_coords = self.coords[day]
            y_start = int(day_coords[1])

            detected_count = 0
            first_y = -1 
            sub_points = []

            for y in range(y_start,y_end):
                color = image[y,int(day_coords[0])]
                if color[0] == 72:
                    sub_points.append(y)

            print(sub_points)

    def get_center_point(self,coordinates):
        x_coords = [point[0] for point in coordinates]
        y_coords = [point[1] for point in coordinates]

        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)

        center = [center_x, center_y]
        return center


    def get_raw_data(self):
        reader = easyocr.Reader(['de'])  
        results = reader.readtext(self.image_path)
        return results


def main():
    SallybusInfoFromImage('stundenplan.png').get_info()

if __name__ == '__main__':
    main()