from WebService import MyStudyWebService

wsdl_url = 'https://mystudy.leuphana.de/mystudy_webservice.wsdl'
service = MyStudyWebService(wsdl_url)


try:
    print("==> Test: Abrufen eines Semesters anhand der ID")
    semester = service.get_semester_from_id(1)
    print("Semester:", semester)

    print("\n==> Test: Abrufen aller Semester")
    all_semesters = service.get_all_semester()
    print("Alle Semester:", all_semesters)

    print("\n==> Test: Abrufen eines Gebiets anhand der ID")
    gebiet = service.get_gebiet_from_id(1)
    print("Gebiet:", gebiet)

    print("\n==> Test: Abrufen von Gebieten eines Studiengangs")
    gebiete = service.get_gebiete_from_studiengang(1)
    print("Gebiete:", gebiete)

    print("\n==> Test: Abrufen eines Moduls anhand der ID")
    modul = service.get_modul_from_id(1)
    print("Modul:", modul)

    print("\n==> Test: Abrufen einer Person anhand der ID")
    person = service.get_person_from_id(1)
    print("Person:", person)

    print("\n==> Test: Abrufen aller Personen")
    all_personen = service.get_all_personen()
    print("Alle Personen:", all_personen)

    print("\n==> Test: Abrufen eines Raums anhand der ID")
    raum = service.get_raum_from_id(1)
    print("Raum:", raum)

    print("\n==> Test: Abrufen einer Veranstaltung anhand der ID")
    veranstaltung = service.get_veranstaltung_from_id(1)
    print("Veranstaltung:", veranstaltung)

    # Weitere Tests können hier hinzugefügt werden, indem die entsprechenden Methoden aufgerufen werden.
    
except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")