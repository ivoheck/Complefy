from zeep import Client
from zeep.exceptions import Fault


class MyStudyWebService:
    def __init__(self, wsdl_url):
        self.client = Client(wsdl=wsdl_url)

    def get_semester_from_id(self, semester_id):
        try:
            return self.client.service.getSemesterFromId(semester_id)
        except Fault as e:
            print(f"Error: {e}")
    
    def get_all_semester(self):
        try:
            return self.client.service.getAllSemester()
        except Fault as e:
            print(f"Error: {e}")
    
    def get_gebiet_from_id(self, gebiet_id):
        try:
            return self.client.service.getGebietFromId(gebiet_id)
        except Fault as e:
            print(f"Error: {e}")

    def get_gebiete_from_studiengang(self, studiengang_id):
        try:
            return self.client.service.getGebieteFromStudiengang(studiengang_id)
        except Fault as e:
            print(f"Error: {e}")

    def get_modul_from_id(self, modul_id):
        try:
            return self.client.service.getModulFromId(modul_id)
        except Fault as e:
            print(f"Error: {e}")

    def get_person_from_id(self, person_id):
        try:
            return self.client.service.getPersonFromId(person_id)
        except Fault as e:
            print(f"Error: {e}")

    def get_all_personen(self):
        try:
            return self.client.service.getAllPersonen()
        except Fault as e:
            print(f"Error: {e}")
    
    def get_raum_from_id(self, raum_id):
        try:
            return self.client.service.getRaumFromId(raum_id)
        except Fault as e:
            print(f"Error: {e}")
    
    def get_veranstaltung_from_id(self, veranstaltung_id):
        try:
            return self.client.service.getVeranstaltungFromId(veranstaltung_id)
        except Fault as e:
            print(f"Error: {e}")

 
