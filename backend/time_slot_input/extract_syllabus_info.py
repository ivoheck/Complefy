import pandas as pd


class GetSallybusInfo():

    def __init__(self):
        self.weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

    def from_myStudy_exel_export(self,file_path):
        df = pd.read_excel(file_path)

        current_day = ''
        for value in df.iloc[:,0]:
            if value == 'Andere Termine':
                break

            elif value in self.weekdays:
                current_day == value

            elif pd.isnan(value):
                current_day = None

            

            

            


def main(file_path):
    res = GetSallybusInfo().from_myStudy_exel_export(file_path)




if __name__ == "__main__":
    main('Stundenplan.xlsx')