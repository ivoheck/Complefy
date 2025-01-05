from WebService import MyStudyWebService

def test_mystudy_webservice():
    wsdl_url = 'https://mystudy.leuphana.de/mystudy_webservice.wsdl'
    service = MyStudyWebService(wsdl_url)

    try:
        print("==> Test: get_semester_from_id")
        print(service.get_semester_from_id(1))

        print("\n==> Test: get_gebiet_from_id")
        print(service.get_gebiet_from_id(1))

        print("\n==> Test: get_gebiete_from_studiengang")
        print(service.get_gebiete_from_studiengang(1))

        print("\n==> Test: get_gebiete_from_modul")
        print(service.get_gebiete_from_modul(1))

        print("\n==> Test: get_modul_from_id")
        print(service.get_modul_from_id(1))

        print("\n==> Test: get_module_from_veranstaltung")
        print(service.get_module_from_veranstaltung(1))

        print("\n==> Test: get_module_from_gebiet")
        print(service.get_module_from_gebiet(1))

        print("\n==> Test: get_person_from_id")
        print(service.get_person_from_id(1))

        print("\n==> Test: get_raum_from_id")
        print(service.get_raum_from_id(1))

        print("\n==> Test: get_rhythmus_from_id")
        print(service.get_rhythmus_from_id(1))

        print("\n==> Test: get_sprache_from_id")
        print(service.get_sprache_from_id(1))

        print("\n==> Test: get_standort_from_id")
        print(service.get_standort_from_id(1))

        print("\n==> Test: get_studiengang_from_id")
        print(service.get_studiengang_from_id(1))

        print("\n==> Test: get_termin_from_id")
        print(service.get_termin_from_id(1))

        print("\n==> Test: get_veranstaltung_from_id")
        print(service.get_veranstaltung_from_id(1))


        print("\n==> Test: get_veranstaltungen_from_person")
        print(service.get_veranstaltungen_from_person(1))

        print("\n==> Test: get_veranstaltungen_from_modul")
        print(service.get_veranstaltungen_from_modul(1))

        print("\n==> Test: get_veranstaltungsart_from_id")
        print(service.get_veranstaltungsart_from_id(1))

        print("\n==> Test: get_ext_auth")
        print(service.get_ext_auth("hash", 1))

    except Exception as e:
        print(f"Test Error: {e}")

if __name__ == "__main__":
    test_mystudy_webservice()
