import easyocr
import cv2
import numpy as np

class SallybusInfoFromImage:

    def __init__(self, image_path):
        self.image_path = image_path

        self.days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag']
        self.time = ['8.00', '9.00', '10.00', '11.00', '12.00', '13.00', '14.00', '15.00', '16.00', '17.00', '18.00', '19.00']

        self.coords = {}

    def get_info(self):
        results = self.get_raw_data()
        self.get_coords(results)

        #print(self.coords)
        subjects = self.find_subjects()
        clustert_subjects = self.cluster_time_points(subjects)
        time_stamps_coords =  self.get_time_stamps_coords(clustert_subjects)
        res = self.get_time_stamps_time(time_stamps_coords)

    def get_time_stamps_time(self,time_stamps_coords):
        time_stamps_minutes = {}

        for day in self.days:
            data = None

            for time_stamp in time_stamps_coords[day]:
                data.append(self.get_time_from_coords(time_stamp[0]),self.get_time_from_coords(time_stamp[1]))

            time_stamps_minutes[day] = data


    def get_time_from_coords(self,time_stamp):
        #TODO: evtl besser machen
        y_8 = int(self.coords['8.00'][1])
        y_9 = int(self.coords['9.00'][1])


        




    def get_time_stamps_coords(self,clustert_subjects):

        res = {'Montag':None, 'Dienstag':None, 'Mittwoch':None, 'Donnerstag':None, 'Freitag':None}

        for day in self.days:
            day_data = clustert_subjects[day]
            data = []
            if len(day_data[0]) == 0:
                data = None

            elif len(day_data[0]) == len(day_data[1]):
                start = day_data[0]
                stop = day_data[1]

                for begin,end in zip(start,stop):
                    data.append((begin,end))

            else:
                start = day_data[0]
                stop = day_data[1]

                # Ergebnislisten
                reduced_start = []
                used_end = []

                for s in start:
                    # Finde den nächsten Endpunkt, der größer oder gleich dem Startpunkt ist
                    end_candidates = [e for e in stop if e >= s]
    
                    if not end_candidates:
                        # Wenn kein passender Endpunkt vorhanden ist, überspringen
                        continue
    
                    nearest_end = min(end_candidates)
    
                    # Überprüfen, ob der Startpunkt zwischen einem vorherigen Startpunkt und einem Endpunkt liegt
                    if reduced_start and reduced_start[-1] <= s < nearest_end:
                        # Überspringen, da dieser Startpunkt zwischen einem anderen Startpunkt und einem Endpunkt liegt
                        continue
    
                    # Startpunkt übernehmen und Endpunkt als verwendet markieren
                    reduced_start.append(s)
                    used_end.append(nearest_end)
                    stop.remove(nearest_end)  # Verwendeten Endpunkt aus der Liste entfernen

                for begin,end in zip(reduced_start,used_end):
                    data.append((begin,end))      

            res[day] = data

        return res


    def split_list(self,nums, threshold=2):
        if not nums:
            return []
    
        result = []
        current_group = [nums[0]]
    
        for i in range(1, len(nums)):
            if nums[i] - nums[i - 1] > threshold:
                result.append(current_group)
                current_group = [nums[i]]
            else:
                current_group.append(nums[i])
    
        result.append(current_group)
        return result
    
    def clean_split_list(self,split_list):
        start = []
        stop = []
        big_lim = 4

        for split in split_list:
            if len(split) > big_lim:
                start.append(split[0])

            elif len(split) >= 1:
                stop.append(split[0])

        return (start,stop)

    def cluster_time_points(self,subjects):
        clustert_subjects = {}

        for day in self.days:
            sub_list = subjects[day]
            split_list = self.split_list(sub_list)
            clean_list = self.clean_split_list(split_list=split_list)
            clustert_subjects[day] = clean_list

        return clustert_subjects


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

        subjects = {}
        #cords = {}

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
                    #cords[str(str(day_coords[0]) + str(y))] = [np.float64(day_coords[0]),np.float64(y)]
                    sub_points.append(y)

            subjects[day] = sub_points
            #print(sub_points)
        
        return subjects
        #print(cords)
        

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