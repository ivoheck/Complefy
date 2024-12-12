from suds.client import Client
from suds.transport.https import HttpTransport
from suds import WebFault
import logging

# Debugging aktivieren
logging.basicConfig(level=logging.DEBUG)


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
            return self.client.service.getAllSemester({})
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

    def get_veranstaltung_from_id(self, veranstaltung_id):
        try:
            return self.client.service.getVeranstaltungFromId(int(veranstaltung_id))
        except WebFault as e:
            print(f"SOAP Fault: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

    # Weitere Methoden mit ähnlichen Anpassungen
