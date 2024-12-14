import pandas as pd
from backend.time_slot_input.sallybus import Sallybus


class GetSallybusInfo():

    def __init__(self):
        self.weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

    def from_myStudy_exel_export(self,df):
        sallybus = Sallybus()

        current_day = ''
        for value in df.iloc[:,0]:
            if value == 'Andere Termine':
                break

            elif value in self.weekdays:
                current_day = value

            elif pd.isna(value):
                current_day = ''

            else:
                start_h = int(value.split('-')[0].split(':')[0])
                start_m = int(value.split('-')[0].split(':')[1])
                end_h = int(value.split('-')[1].split(':')[0])
                end_m = int(value.split('-')[1].split(':')[1])

                time_frame = (((start_h * 60) + start_m),((end_h * 60) + end_m))
                sallybus.add_time_frame(current_day,time_frame)

        return sallybus.as_dict()

            

def main(file_path):
    df = pd.read_excel(file_path)
    res = GetSallybusInfo().from_myStudy_exel_export(df)
    print(res.tuesday[0].start_time)


if __name__ == "__main__":
    main('Stundenplan.xlsx')