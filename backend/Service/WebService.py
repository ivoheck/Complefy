from suds.client import Client
from suds.transport.https import HttpTransport
from suds import WebFault


class MyStudyWebService:
    def __init__(self, wsdl_url):
        self.client = Client(wsdl_url, transport=HttpTransport())

    def get_semester_from_id(self, semester_id):
        try:
            return self.client.service.getSemesterFromId(int(semester_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_all_semester(self):
        try:
            return self.client.service.getAllSemester({})  # Dummy-Wert verwenden
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_gebiet_from_id(self, gebiet_id):
        try:
            return self.client.service.getGebietFromId(int(gebiet_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_gebiete_from_studiengang(self, studiengang_id):
        try:
            return self.client.service.getGebieteFromStudiengang(int(studiengang_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_gebiete_from_modul(self, modul_id):
        try:
            return self.client.service.getGebieteFromModul(int(modul_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_modul_from_id(self, modul_id):
        try:
            return self.client.service.getModulFromId(int(modul_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_module_from_veranstaltung(self, veranstaltung_id):
        try:
            return self.client.service.getModuleFromVeranstaltung(int(veranstaltung_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_module_from_gebiet(self, gebiet_id):
        try:
            return self.client.service.getModuleFromGebiet(int(gebiet_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_person_from_id(self, person_id):
        try:
            return self.client.service.getPersonFromId(int(person_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_all_personen(self):
        try:
            return self.client.service.getAllPersonen({})
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_personen_from_nachname(self, nachname):
        try:
            return self.client.service.getPersonenFromNachname(nachname)
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_raum_from_id(self, raum_id):
        try:
            return self.client.service.getRaumFromId(int(raum_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_rhythmus_from_id(self, rhythmus_id):
        try:
            return self.client.service.getRhythmusFromId(int(rhythmus_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_sprache_from_id(self, sprache_id):
        try:
            return self.client.service.getSpracheFromId(int(sprache_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_all_sprachen(self):
        try:
            return self.client.service.getAllSprachen({})
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_standort_from_id(self, standort_id):
        try:
            return self.client.service.getStandortFromId(int(standort_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_studiengang_from_id(self, studiengang_id):
        try:
            return self.client.service.getStudiengangFromId(int(studiengang_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_all_studiengaenge(self, semester_id=None):
        try:
            if semester_id:
                return self.client.service.getAllStudiengaenge(int(semester_id))
            else:
                return self.client.service.getAllStudiengaenge()
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_termin_from_id(self, termin_id):
        try:
            return self.client.service.getTerminFromId(int(termin_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_veranstaltung_from_id(self, veranstaltung_id):
        try:
            return self.client.service.getVeranstaltungFromId(int(veranstaltung_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def search_veranstaltungen(self, studiengang_id, gebiet_id, modul_id, text, dozent, sprache_id, semester_id=None):
        try:
            return self.client.service.searchVeranstaltungen(int(studiengang_id), int(gebiet_id), int(modul_id), text, dozent, int(sprache_id), semester_id)
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_veranstaltungen_from_person(self, person_id, semester_id=None):
        try:
            if semester_id:
                return self.client.service.getVeranstaltungenFromPerson(int(person_id), int(semester_id))
            else:
                return self.client.service.getVeranstaltungenFromPerson(int(person_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_veranstaltungen_from_modul(self, modul_id, fixed_semester=None):
        try:
            return self.client.service.getVeranstaltungenFromModul(int(modul_id), fixed_semester)
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_veranstaltungsart_from_id(self, veranstaltungsart_id):
        try:
            return self.client.service.getVeranstaltungsartFromId(int(veranstaltungsart_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_all_veranstaltungs_tags(self):
        try:
            return self.client.service.getAllVeranstaltungsTags({})
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    def get_ext_auth(self, hash_value, person_id):
        try:
            return self.client.service.getExtAuth(hash_value, int(person_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
