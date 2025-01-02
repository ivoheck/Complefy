import os
import sys

# Verzeichnis des Projekts (Root-Verzeichnis) ermitteln
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))  # Passe die Anzahl der '..' an

# Projekt-Root zu sys.path hinzufügen, falls noch nicht enthalten
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import easyocr
from PIL import Image
import cv2
import numpy as np
from backend.time_slot_input.sallybus import Sallybus


class SallybusInfoFromImage:

    def __init__(self, image_np):
        self.image_np = image_np

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
        time_stamps_minutes = self.get_time_stamps_time(time_stamps_coords)
        return self.convert_to_sallybus(time_stamps_minutes)

    def convert_to_sallybus(self,time_stamps_minutes):
        sallybus = Sallybus()

        for day in self.days:
            day_data = time_stamps_minutes[day]

            for time_data in day_data:
                sallybus.add_time_frame(day,time_data)

        return sallybus


    def get_time_stamps_time(self,time_stamps_coords):
        time_stamps_minutes = {}

        for day in self.days:
            data = []
            time_stamp = time_stamps_coords[day]
            
            if time_stamp is not None:
                for i in time_stamp:
                    data.append((int(self.get_time_from_coords(i[0])),int(self.get_time_from_coords(i[1]))))

            time_stamps_minutes[day] = data

        return time_stamps_minutes


    def get_time_from_coords(self,time_stamp):
        #TODO: evtl besser machen
        y_8 = int(self.coords['8.00'][1])
        y_9 = int(self.coords['9.00'][1])

        h = y_9 - y_8
        quater = int(h/4)
        
        if time_stamp <= y_8:
            return 480 #8 uhr

        res_value = 480
        time_stamp = time_stamp - y_8
        while time_stamp > h:
            time_stamp -= h
            res_value += 60

        res_value += h * (time_stamp/h)
        return res_value


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
        #image = cv2.imread(self.image_path)

        image = cv2.cvtColor(self.image_np, cv2.COLOR_RGB2BGR)

        y_end = int(self.coords['19.00'][1])
        print('y_end ', y_end)
        min_count = 10

        subjects = {}
        cords = {}

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
                    cords[str(str(day_coords[0]) +' '+ str(y))] = [np.float64(day_coords[0]),np.float64(y)]
                    sub_points.append(y)

            subjects[day] = sub_points
            #print(sub_points)
        
        print(cords)
        return subjects
        

    def get_center_point(self,coordinates):
        x_coords = [point[0] for point in coordinates]
        y_coords = [point[1] for point in coordinates]

        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)

        center = [center_x, center_y]
        return center


    def get_raw_data(self):
        reader = easyocr.Reader(['de'])  
        results = reader.readtext(self.image_np)
        return results


def main():
    image = Image.open('stundenplan.png')
    image_np = np.array(image)
    SallybusInfoFromImage(image_np=image_np).get_info()

if __name__ == '__main__':
    main()