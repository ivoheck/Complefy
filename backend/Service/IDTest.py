from WebService import MyStudyWebService

def test_function(service, function_name, start_id, end_id, *args):
    print(f"Testing: {function_name}")
    valid_ids = []
    for i in range(start_id, end_id + 1):
        try:
            func = getattr(service, function_name)
            result = func(i, *args) if "ext_auth" not in function_name else func(args[0], i)
            if result and any(getattr(result, attr, None) for attr in dir(result) if not attr.startswith('__')):
                print(f"ID {i}: Valid")
                valid_ids.append(i)
            else:
                print(f"ID {i}: No data")
        except Exception as e:
            print(f"ID {i}: Error ({e})")
    print(f"Valid IDs for {function_name}: {valid_ids}")
    return valid_ids

def main():
    wsdl_url = 'https://mystudy.leuphana.de/mystudy_webservice.wsdl'
    service = MyStudyWebService(wsdl_url)

    start_id = 1
    end_id = 10000

    functions_to_test = [
        ("get_semester_from_id", []),
        ("get_gebiet_from_id", []),
        ("get_gebiete_from_studiengang", []),
        ("get_gebiete_from_modul", []),
        ("get_modul_from_id", []),
        ("get_module_from_veranstaltung", []),
        ("get_module_from_gebiet", []),
        ("get_person_from_id", []),
        ("get_raum_from_id", []),
        ("get_rhythmus_from_id", []),
        ("get_sprache_from_id", []),
        ("get_standort_from_id", []),
        ("get_studiengang_from_id", []),
        ("get_termin_from_id", []),
        ("get_veranstaltung_from_id", []),
        ("get_veranstaltungen_from_person", []),
        ("get_veranstaltungen_from_modul", []),
        ("get_veranstaltungsart_from_id", []),
        ("get_ext_auth", ["hash"])
    ]

    with open("valid_ids_ranges.txt", "w") as file:
        for function_name, args in functions_to_test:
            valid_ids = test_function(service, function_name, start_id, end_id, *args)
            file.write(f"{function_name}: {valid_ids}\n")

if __name__ == "__main__":
    main()
