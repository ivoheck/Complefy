from PyPDF2 import PdfReader


class GetCompSubsFromInput():

    def __init__(self):
        self.comp_MedN = "Medialitätsorientierte Zugänge zu den Naturwissenschaften"
        self.comp_MetN = "Methodenorientierte Zugänge zu den Naturwissenschaften"
        self.comp_PraN = "Praxisorientierte Zugänge zu den Naturwissenschaften"

        self.comp_MedS = "Medialitätsorientierte Zugänge zu den Sozialwissenschaften"
        self.comp_MetS = "Methodenorientierte Zugänge zu den Sozialwissenschaften"
        self.comp_PraS = "Praxisorientierte Zugänge zu den Sozialwissenschaften"

        self.comp_MedW = "Medialitätsorientierte Zugänge zu inter- und transdisziplinären Wissenschaften"
        self.comp_MetW = "Methodenorientierte Zugänge zu inter- und transdisziplinären Wissenschaften"
        self.comp_PraW = "Praxisorientierte Zugänge zu inter- und transdisziplinären Wissenschaften"

        self.comp_MedG = "Medialitätsorientierte Zugänge zu den Geisteswissenschaften"
        self.comp_MetG = "Methodenorientierte Zugänge zu den Geisteswissenschaften"
        self.comp_PraG = "Praxisorientierte Zugänge zu den Geisteswissenschaften"

        self.comps = [self.comp_MedN,self.comp_MetN,self.comp_PraN,self.comp_MedS,self.comp_MetS,self.comp_PraS,self.comp_MedW,self.comp_MetW,self.comp_PraW,self.comp_MedG,self.comp_MetG,self.comp_PraG]


    #Takes a filepath to a pdf TOR and returns all comps subjects found as strings inside a list
    def getCompSubsFromTOR(self,file_path):
        reader = PdfReader(file_path)

        list_of_finished_comps = []

        print(len(self.comps))

        text = ""
        for page in reader.pages:
            text += page.extract_text()

        if text == "":
            return list_of_finished_comps
 
        for comp in self.comps:
            if comp in text:
                list_of_finished_comps.append(comp)
    
        return list_of_finished_comps


def main(file_path):
    res = GetCompSubsFromInput().getCompSubsFromTOR(file_path=file_path)

    print(res)


if __name__ == "__main__":
    main("test.pdf")