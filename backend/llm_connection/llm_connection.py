import os
import sys

# Verzeichnis des Projekts (Root-Verzeichnis) ermitteln
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))  # Passe die Anzahl der '..' an

# Projekt-Root zu sys.path hinzufügen, falls noch nicht enthalten
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from openai import OpenAI
from secret import api_key
import json
import ast
from backend.llm_connection import promts


class ChatObject():

    def __init__(self):
        self.chat = [{"role":"system","content":"You are a helpful assistant"}]

    def add_user_promt(self, chat, promt):
        chat.append({"role":"user","content": str(promt)})
        return chat
    
    def add_respones(self, chat, respose):
        chat.append({"role":"user","content": str(respose)})
        return chat
    
    def get_chat(self):
        return self.chat


class LLMConnection():
    def __init__(self):
        base_url = "https://chat-ai.academiccloud.de/v1"
        
        self.model = "meta-llama-3.1-8b-instruct"
        self.model_lama_70 = "meta-llama-3.1-70b-instruct"
        self.client = OpenAI(
            api_key = api_key,
            base_url = base_url
        )

        self.chat_setup = {"role":"system","content":"You are a helpful assistant"}

    def text_completion(self,text):
        text_completion = self.client.completions.create(
            prompt=text,
            model= self.model,
        )

        return text_completion.choices[0].text
        

    def chat_completion(self,chat,question,model):

        chat = None
        #print(question)
        if chat is None:
            chat = self.chat_setup

        chat_completion = self.client.chat.completions.create(
            messages=[chat,question],
            model= model,
        )

        return chat_completion.choices[0].message.content
    
    def get_result_awnser(self,message,results):
        chat = [{"role":"system","content":"You are a helpful assistant"}]

        promt = """
                generire eine kurze antwort nachricht für basirend auf der aufforderung des nutzers und der ergebnisse, soetws wie: hier sind die ergebnisse...
                nim auch kurz bezug auf die gefundenen ergebnisse
            """
        promt += "die ergebnisse sind follgende: " + str(results)
        promt += "die aufforderung des nutzer ist: " + message
        complete_promt = {"role":"user","content":promt}
        
        return self.chat_completion(chat=chat,question=complete_promt,model=self.model_lama_70)
        
    def get_results(self,input_comps,input_promt):
        chat = [{"role":"system","content":"You are a helpful assistant"}]
                 
        promt =  promts.get_result
                 
        promt = promt + f"{input_comps} Der Kontext-Prompt lautet: {input_promt}"
        complete_promt = {"role":"user","content":promt}
        result =  self.chat_completion(chat=chat,question=complete_promt,model=self.model)
        start_index = result.find('[')  # Finde den Anfang der JSON-Daten
        end_index = result.rfind(']') + 1  # Finde das Ende der JSON-Daten

        json_string = result[start_index:end_index]
        #print(json_string)

        try:
            data_dict = ast.literal_eval(json_string)
            return (data_dict,None)
        except:
            return (None, json_string)
        
    
def main():
    #print(LLMConnection().chat_completion(chat=None,question={"role":"user","content":"How tall is the Eiffel tower?"}))
    print( '\n \n' , LLMConnection().get_results(input_comps=""" [
    {
        "id": 1138195,
        "name": "Die Kunst des Theoretisierens - Ein Leitfaden zur Sozialtheorie",
        "inhalt": "Sozialtheorien stellen das epistemische Fundament dar, auf dem die Disziplin der Soziologie seit ihrer Entstehung Studien über gesellschaftliche Zusammenhänge durchführt. Dadurch wird nicht nur abstraktes Wissen erzeugt, sondern auch eine Veränderung der betreffenden Zusammenhänge bewirkt. So haben beispielsweise Diskurse über ökonomische Privilegien, Geschlechter und Rassismus vielfältige soziale Bewegungen geprägt.  Die Autor*innen solcher Theorien werden mitunter als brillante Genies wahrgenommen, denen außergewöhnliche kognitive Fähigkeiten zugeschrieben werden, die ihnen erlauben würden, gesellschaftliche Selbstverständlichkeiten zu hinterfragen und zu akademisch anerkannten Erkenntnissen zu gelangen. Wie gelangen Sozialtheoretiker*innen aber zu ihren Annahmen, Beschreibungen und Erklärungen? Es stellt sich die Frage, ob diese tatsächlich als gedankliche Geistesblitze außergewöhnlich begabter Individuen zu verstehen sind, oder ob sich ein Muster, eine Schablone, ein System ausmachen lässt, mit dessen Hilfe Theorien praktisch entwickelt werden können. Anders gefragt: Ist die Praxis des Theoretisierens sozialer Zusammenhänge lehr- und erlernbar?   Richard Swedberg (2012, 2014) nimmt genau dies an und entwickelt das Konzept des &#34;Theorizing&#34;, um diese Praxis zu erfassen und zu vermitteln. Auf der Grundlage seines Ansatzes werden wir im Rahmen dieses Seminars diese Praxis in vier Teilschritte differenzieren und durch die Beobachtung aktueller Phänomene eigene empirisch begründete Sozialtheorien formulieren. Das Seminar ist entsprechend dieser Unterscheidungen in vier Teile (und fünf Termine) gegliedert und wird Schritt für Schritt von den Teilnehmenden angewandt. Dabei sind der Auswahl der Phänomene nur wenig Grenzen gesetzt. ",
        "ziel": "Das Ziel des Seminars ist, dass die Studierenden lernen eine eigene, empirisch begründete Theorie eines sozialen Phänomens formulieren, wobei nicht die fertige Theorie im Vordergrund steht, sondern die Schritte, die Notwendig sind, um zu einer überzeugenden Theorie zu gelangen. ",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1138391,
        "name": "Die Shoah im Film",
        "inhalt": "Die Ermordung der europäischen Jüdinnen und Juden wurde schon seit den 1940er Jahren in Dokumentar- und Spielfilmen ins Bild gesetzt. Seither hat sich die Darstellung vielfach verändert. An den Veränderungen können die Wendungen entziffert werden, die in verschiedenen Gesellschaften im Zusammenhang mit der Erinnerung an die Shoah auftraten. Die Vorlesung möchte diese Veränderungen durch die Jahrzehnte hindurch sowohl im Dokumentar- als auch im Spielfilm verfolgen und an Beispielsequenzen erläutern. Sie strebt einen Überblick über die filmische Erinnerung an dieses historisch zentrale Ereignis des 20. Jahrhunderts an und legt dabei einen Fokus auf die im deutschsprachigen Bereich produzierten Filme. ",
        "ziel": "Studierende lernen die Geschichte des Holocaust-Films kennen, wie sie sich insbesondere im deutschsprachigen Raum entwickelt hat. ",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1139364,
        "name": "Ethik der Digitalisierung",
        "inhalt": "Das  Internet und ein zunehmendes Maß an Digitalisierung in den unterschiedlichsten Bereichen unseres Lebens verändert die Art wie wir lernen, Geschäfte machen, in Kontakt treten oder auch nur ein Taxi bestellen. Ob unser Leben dadurch besser oder schlechter wird – in jedem Fall wird es schneller, globaler und letztlich komplexer. Wenn Ethik Kants frage „Was soll ich tun?“ beantworten soll, wie passt dann ein Leben in Zeiten der Digitalisierung zu diesem ethischen Anspruch? Ändert sich etwas an seinem Wert und seinen Möglichkeiten druch die uns zur Verfügung stehenden Informationstechnischen Möglichkeiten. Ändert sich etwas an der Art, wie wir über Ethik nachdenken?",
        "ziel": "Diese aktuellen Fragen sollen im Seminar problematisiert werden mit dem Ziel, eine Ethik der Digitalisierung zu entwickeln.",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1139454,
        "name": "Feminist Social and Political Philosophy (FSL)",
        "inhalt": "This lecture-based class introduces feminist philosophical approaches to thinking the social and political world. It entails, first, an exploration of feminist engagements with, appropriations from, and critiques of the modern, western canon of social and political philosophy – including the ways it has thought justice, equality, the social contract, freedom and rights. Here the focus is primarily on feminist and queer engagements with liberal social and political thought, which is itself shown to be a highly heterogeneous enterprise. In the second part of the seminar, students address feminist contributions to social and political philosophy that break with or move beyond liberal traditions.  Students will engage work by Susan Okin, Mary Wollstonecraft, John Stuart Mill and Harriet Taylor, Nancy Fraser, Angela Davis, Emma Goldman, Judith Butler and others. ",
        "ziel": "•\tGain an understanding of feminist critiques of and contributions to social and political philosophy •\tCritically engage with feminist thinking around key concepts within social and political philosophy, including ideas of justice, equality, freedom and rights •\tExplore a range of liberal and non-liberal approaches to feminist philosophy ",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1141659,
        "name": "Filme als Briefe. Internationale Konflikte im essayistischen Kino",
        "inhalt": "Filme, die wie Briefe aussehen oder klingen, erinnern an persönliche Ansprachen. Und doch wenden sie sich an ein Publikum. Wie greifen hierbei Privates und Öffentliches ineinander? Filmautor*innen wie Jean-Luc Godard, Anne-Marie Miéville, Chris Marker, Emily Jacir, Eric Baudelaire verknüpfen ihre Gedanken zu den Gefechten zwischen Israel und Palästina, zum Vietnam-Krieg oder zu anderen Dekolonisierungskämpfen mit dem Blick auf den jeweils eigenen Standort, auf die Reichweite ihrer eigenen Aktivität. Wie interpretieren solche Filme Versand, Transport und Ankunft der Botschaft? Wie unterscheidet sich deren filmische Materialität von derjenigen des Postverkehrs? Letzterer ist immer schon mit den Aspekten der Entfernung, der Trennung, des Verlustes und des Wunsches nach Überbrückung und Verständigung verknüpft. Dies verbinde ihn „konstitutiv“ mit den Problemen des Exils oder der Diaspora, wie der amerikanisch-iranische Theoretiker und Filmemacher Hamid Naficy schreibt. Vorgestellt und diskutiert werden im Seminar insbesondere Brieffilme oder Filmbriefe, deren Autor*innen die Umstände postkolonialer oder kriegerische Auseinandersetzungen thematisieren. Zu reflektieren ist hierbei nicht zuletzt das Verhältnis zwischen dem jeweiligen Aktualitätseindruck der Filme und ihrer postalischen Kommunikation. Die Philosophin Sybille Krämer unterscheidet das durch die Trennung von Absender*innen und Empfänger*innen charakterisierte postalische Prinzip der Kommunikation deutlich vom persönlichen (oder „erotischen“) Prinzip des direkten Dialogs. Strebe das unmittelbare Gespräch eine Verständigung oder gar Vereinigung der sich Begegnenden an, so vermag das postalische Prinzip, trotz der Suche nach Verbindungen oder Berührungen, die räumlichen, zeitlichen Entfernungen wie auch die sachlichen Differenzen mit aufzubewahren. ",
        "ziel": "Lernziele des Seminars betreffen die Kenntnisse zur Geschichte des Essayfilms, das Erlernen verschiedener Methoden der Filmanalyse, die Reflexion von Grundbegriffen der Kritischen Theorie und des Poststrukturalismus sowie die Kompetenzen, um an den aktuellen Diskursen zur Ästhetik und Funktion von Infrastrukturen teilzunehmen. Hinzu kommt die Einübung in Methoden des Bibliografierens, des Zitierens, des kritischen Lesens und Argumentierens.  In den Seminarsitzungen werden jeweils ein Film in Ausschnitten vorgeführt und dazu vorhandene wissenschaftliche Forschungen vorgestellt und diskutiert. Zudem wird jeweils im Voraus ein film- bzw. geisteswissenschaftlich relevanter Text zugänglich sein, um diesen im Seminar erst gruppenweise, dann im Plenum zu diskutieren. Bezüglich der Hausarbeit bietet es sich für die Studierenden an, im Hinblick auf eine/n der vorgestellten Filme und Forschungen, die eigene Fragestellung zu entwickeln und dieser selbständig recherchierend und diskutierend nachzugehen. Nicht zuletzt besteht das Lernziel des Seminars darin, die eigenen Seminar- und Diskussionsbeiträge in ihrer postalischen Struktur – als Sendung und Adressierung – zu reflektieren.",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1139024,
        "name": "Human Machine (Exkursions-Seminar)",
        "inhalt": "Die Beziehung zwischen Mensch und Maschine ist seit der Industrialisierung ein zentrales Thema künstlerischer Auseinandersetzungen. Die Verknüpfung zweier aktueller Megathemen – der Klimakrise und der Digitalisierung, insbesondere der künstlichen Intelligenz (KI) – erhöht die gesellschaftliche und kulturelle Relevanz dieser Debatte. Grundlegende philosophische, ökonomische, ökologische und ethische Konzepte werden infrage gestellt. Kate Crawford weist darauf hin, dass ein zentraler Mythos der KI-Industrie darin besteht, Intelligenz als unabhängig von sozialen, kulturellen, historischen und politischen Kräften zu betrachten. Das Konzept einer „überlegenen“ Intelligenz hat jedoch seit Jahrhunderten tiefgreifende Probleme verursacht. Die Künste können in diesem Kontext ein spezifisches ästhetisches Wissen generieren: Sie stellen Konzepte zur Diskussion, entwickeln Szenarien und stoßen Spekulationen über die Zukunft an. Utopien und Fiktionen – etwa über empfindungsfähige Maschinen, die sich gegen den Menschen wenden, oder Phantasien über menschliche Unsterblichkeit – prägen die westliche kulturelle Vorstellungskraft bis heute.  Das Seminar „Human Machine“ steht im Kontext eines Programms der Jungen Akademie/E-Werk Luckenwalde, in dem internationale Künstler*innen aus verschiedenen Disziplinen digitale Technologien und KI erforschen. Sie hinterfragen die westliche Fortschrittsgeschichte und Dualismen wie das „Natürliche“ und das „Künstliche“ und eröffnen neue Narrative und Denkmuster für eine nachhaltige Zukunft.   Im Rahmen einer Exkursion werden wir die offenen Ateliers von Künstler*innen (der aktuellen Stipendiat*innen 24/25) des Programms besuchen. Die Begegnung mit den künstlerischen Arbeiten (Artefakte, ggf. Interviews) bildet die Grundlage für medienbasierte wissenschaftliche Reflexionen.",
        "ziel": "Das Seminar vertieft das Verständnis für die kulturellen und sozialen Auswirkungen von KI und die Verflechtung digitaler Technologien mit ökologischen Fragestellungen. Es regt zur Auseinandersetzung mit künstlerischen Perspektiven an, um die Rolle der Kunst bei der Entwicklung neuer Denkansätze und Handlungsmöglichkeiten zu untersuchen.  Die Teilnahme an der Exkursion ist obligatorisch. Vorkenntnisse werden nicht vorausgesetzt; die Bereitschaft zur aktiven Auseinandersetzung mit den Themen ist jedoch erforderlich.",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1141658,
        "name": "L&#39;héritage littéraire de Bourdieu : Annie Ernaux, Didier Eribon et Edouard Louis.",
        "inhalt": "Le séminaire propose d&#39;analyser comment les principales thèses de Bourdieu ont été reprises - et adaptées ou modifiées - dans des textes de fiction (roman, autofiction, auto-socio-biographie, autobiographie). L&#39;objectif est à la fois de repérer l&#39;influence de Bourdieu sur des écrivains de générations différentes et d&#39;étudier le transfert entre des théories sociologiques et des textes littéraires. (Das Seminar analysiert den Einfluss und Transfer von Bourdieus Thesen in literarische Texte (Autobiografie, Autofiktion, Auto-Sozio-Biografie, Roman). ",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1138782,
        "name": "Pop-Theorie-Wissen",
        "inhalt": "Populäre Musik (Popmusik) ist heutzutage für die meisten Menschen ein wichtiger Bestandteil des Alltags. Doch was umfasst Popmusik eigentlich und wie hat sie sich entwickelt? In diesem Seminar setzen wir uns mit diesen und weiteren Fragen und Themenbereichen zu Theorien der Popmusik auseinander. ",
        "ziel": "Studierende kennen die Entwicklung populärer Musik und erkunden verschiedene Theorien und Aspekte der Popmusik. ",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1138643,
        "name": "Populäre Musik  – Hören, beschreiben, begreifen eines kulturellen Phänomens",
        "inhalt": "Im Kurs geht es ears on um Musik. Jede Woche hören wir unterschiedliche Songs und Tracks der populären Musik zu bestimmten Themen. Ausgehend vom Höreindruck nähern wir uns der Musik, ihrer Machart, Wirkung und Hintergründen. Dabei stehen nicht Künstler*innen oder Bands im Vordergrund, sondern der Eindruck des fertig produzierten Songs bwz. Tracks. Musiktheorie oder Kenntnisse in Musikproduktion, Songwriting etc. sind hilfreich, aber nicht erforderlich.",
        "ziel": "Die Studierenden lernen, ad hoc auf einen Höreindruck reagieren und diesen beschreiben zu können. Sie erweitern ihr Repertoire der Musik sowie der Sprache über Musik. Studierende reflektieren ihre eigene Hörweise.",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1139946,
        "name": "Queering Jewish Heritage: Iridescence and Potentiality (FSL)",
        "inhalt": "Recent decades have seen an explicit articulation of the intersection of Jewish and queer identities, and a growing visibility of queering perspectives in contemporary cultural production and onto Jewish Heritage, especially in North-America but also more recently in Europe. In contemporary Jewish cultures, queer approaches to gender, sexuality, identity, family and communal life have grown in recognition, across a diversity of Jewish communities. In this context, the Jewish past is being revisited with queer eyes. Nonetheless, many LGBTQ + and Jewish identified persons still experience conflicts and tensions, coping mechanisms and negotiations of identities.  In much of modern history, externally imposed perceptions of Jewish persons as ‘queer’, coming from the Christian and secular majority society, were articulated as part of antisemitism. Besides contributing to a critical awareness of the complex intersectionality of queer+Jewish histories, academic and artistic researchers also contribute to the agency of queer+Jewish identifications through the reclamation of a queer Jewish Heritage.  This seminar explores these intersections of Jewish and Queer cultures and heritage. In academia, theoretical advances were initiated at the intersection of Jewish identity and queer theory, exploring potential correlations between the inventions of the modern notions of “the Jew” and “the homosexual”, links between homophobia and antisemitism, contradicting models of masculinities and further intersectional concerns (Boyarin 1997; Boyarin, Itzkovitz & Pellegrini 2003). Jewish Studies scholars (e.g. Sienna 2019), have retraced queer dimensions over the past two millennia, initiating a reversal of the “writing out” of queers from Jewish history. LGBTQ Jews in North America have developed specific cultural and/or religious practices (Balka & Rose 1991, Shneer & Aviv 2002). Liberal branches of Judaism have witnessed queering developments within religion, sooner or later followed by other denominations. Some authors have proclaimed a queer “revolution” in liberal Judaism (Romain & Mitchell 2020). Gay synagogues (Shokheid 1995) and a Lesbian rabbinic discourse (Alpert, Elwell & Idelson 2001) have emerged in North-America in the late 20th Century. Queer interpretations of religion have been combined with transformative ambitions for communities (Drinkwater, Lesser & Shneer 2009). This involves &#34;midrash&#34; (i.e. narrative interpretations of the underlying significance of a biblical text) created by contemporary queer-oriented artists/authors (e.g. Ladin 2018, Ramer 2020) and poets (Hammer 2017). The queering of Jewish cultures has affected various areas of communal life, such as e.g. families (Fishman 2015), education (Shneer 2002) and the Yiddish language (Shandler 2006).  The seminar will explore Queer+Jewish cultural production, and its relation to the cultural heritage of Jewish peoples. For example, historical research has been conducted on the roles gay Jewish theater and film-makers played since the 1960s in exploring the intersections of Jewish + gay identities and on integrating LGBTQ communities into a wider Jewish historical narrative (Friedman 2007). Literary studies have contributed insights on how 20th century Jewish American literature and theatre was inhabited by queer sensibilities (though often in stealth-mode, “passing” as heterosexual, implicit or denied), which may have prepared the ground for the wider acceptance of queerness in contemporary Jewish American culture (Hoffman 2009). The seminar will also interrogate how, in this fast-evolving context, Heritage professionals in Europe have been especially inert, with rare and small-scale efforts to thematize the intersection of Jewish and Queer cultures, e.g. the Jewish Museum in Berlin with a critical self-evaluation of the lack of queer perspectives in its own collections (Waßmer 2018), some elements in its exhibitions (e.g. 2013: “Are there Gay Jews?” within the exhibition “The Whole Truth”), and through online media (https://www.jmberlin.de/en/topic-lgbtqi); and in the UK the oral history project “Rainbow Jews” in the 2010s, initiated by the organization “Liberal Judaism”, focusing on the lives of LGBTQ people in the UK since the 1950s. The seminar contents will be enriched by ‘direct’ insights coming from the lecturer’s own ongoing DFG-funded research project on “queering Jewish Cultural Heritage in Europe”.",
        "ziel": "The seminar aims to gain an overview of the specific intersection of Jewish and Queer cultures, especially in their relation to the making of cultural heritage. It covers aspects of gender, sexualities, identities and various cultural practices (in religion, education, language, the arts), as well as issues of intersectional discriminations in the specific case of Jewish + LGBTQI+ identities. The seminar allows students to combine theoretical and empirical insights from interdisciplinary sources from the humanities, social sciences, Jewish studies and queer studies, and to get acquainted with ongoing empirical research. The themes and issues will be approached both in historical and especially in contemporary contexts.",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1139446,
        "name": "Recht, Imagination und Wirklichkeit",
        "inhalt": "Das Seminar befasst sich mit der imaginären Dimension des Rechts: Wie stellt sich die Welt vor dem geistigen Auge der Juristinnen und Juristen dar? Welche Rolle spielt die Rechtssprache bei der Erzeugung der juristischen Wirklichkeit? Und wie real ist eigentlich die künstlich-virtuelle Welt des Rechts? Diesen Fragen geht die Veranstaltung aus einer interdisziplinären und grundlagenorientierten Perspektive nach. Besonderes Augenmerk liegt dabei auf dem Titelbild von Hobbes’ „Leviathan“ und dem Kunstmärchen „Des Kaisers neue Kleider“.",
        "ziel": "Ziel der Veranstaltung ist es, moderne Theorien zur politischen Imagination und zur sprachlichen Konstruktion der Wirklichkeit mit rechtsontologischen Fragestellungen zu verknüpfen. Zugleich soll der kritisch-reflexive Umgang mit theoretischen Texten geübt werden.",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1139457,
        "name": "Robert Musil: Der Mann ohne Eigenschaften ",
        "inhalt": "„Sie müßten aber dem Zuschauer die Handlung mitteilen. Sie können nicht sagen, dieser Ulrich hatte keine Eigenschaften, und eine Handlung gibt’s auch nicht, und was das Jahrhundert angeht, wissen wir nicht, was herauskommt, und der Film hat keinen Anfang, kein Ende, und einen Mittelteil schon gar nicht. Das wäre z.B. für eine Vorankündigung ungeeignet.“ (Alexander Kluge)   Was ihn für eine Verfilmung ungeeignet erscheinen lässt, darin mögen auch Gründe liegen, wieso &#34;Der Mann ohne Eigenschaften&#34; (1930) bis heute wenig gelesen wird. Dabei zählt sein Autor Robert Musil mit James Joyce, Thomas Mann, Marcel Proust und Virginia Woolf zu den zentralen Vertreter:innen der Klassischen Moderne. Das Seminar bietet eine vertiefte Auseinandersetzung mit einem der wichtigsten Romanprojekte des 20. Jahrhunderts. Situiert im österreichischen Vielvölkerstaat am Vorabend des ersten Weltkriegs widersetzt sich der Roman schon in seiner formalen Anlage ideologischen Denkmustern und verlangt seinen Leser:innen eine „Kontingenztoleranz“ (Makropoulos 1987) ab, die heute nicht weniger relevant ist als zu Zeiten seines Erscheinens.  Musils Text bringt mit seinen Figuren eine Vielzahl an Welthaltungen und Denkformen zur Anschauung und greift dabei auch zeitgenössische entwicklungspsychologische und ethnografische Diskurse auf. Aspekte des Gesellschaftsromans wie die Krise der (männlichen) Identität, Militarismus und Antisemitismus stehen dabei ebenso im Zentrum der Analyse wie poetologische Fragen sowie die philosophische und weltanschauliche Ebene des Textes.  ",
        "ziel": "- Entwicklung analytischer und interpretatorischer Zugänge zu Robert Musils &#34;Der Mann ohne Eigenschaften&#34; - Kenntnisse der literarästhetischen, geistesgeschichtlichen und wissenschaftlichen Zusammenhänge des Textes - Verständnis für die Stellung des Romans als eines der bedeutendsten literarischen Werke der europäischen Moderne - Einführung in die literaturwissenschaftliche Textanalyse, Kritische Auseinandersetzung mit grundsätzlichen Problemen der Erzähl- und Interpretationstheorie  ",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1138293,
        "name": "Von Caligari zu Hitler. Das deutsche Kino in der Weimarer Republik",
        "inhalt": "„From Caligari to Hitler“ lautet der Titel einer 1947 erschienenen Studie, die der deutsch-jüdische Architekt, Soziologe, Journalist und Filmtheoretiker Siegfried Kracauer (1889-1966) im US-amerikanischen Exil, in das er 1941 vor den Nazis geflohen war, schrieb. Kracauer setzt sich in dieser Studie unter mentalitätsgeschichtlichen Gesichtspunkten mit der Geschichte des deutschen Films von dessen Anfängen bis zur Machtergreifung des Nationalsozialisten auseinander. Wie er im Vorwort erklärt, möchte er durch seine Analysen der Filme „tiefenpsychologische Dispositionen, wie sie in Deutschland von 1918 bis 1933 herrschten“, sichtbar machen. Im Seminar sollen einige besonders prominente Stumm- und Tonfilme, die Kracauer in seinem Buch thematisiert, genauer untersucht werden, darunter „Der Student von Prag“ (1913), „Das Cabinett des Dr. Caligari“ (1920), „Die freudlose Gasse“ (1925), „Metropolis“ (1927), „M – Eine Stadt sucht einen Mörder“ (1931) und „Mädchen in Uniform“ (1931). Neben der Rekonstruktion und Diskussion von Kracauers Thesen zu diesen Filmen soll es auch um die Erarbeitung eigener Deutungsansätze gehen.   Literaturhinweis zur Vorbereitung: Siegfried Kracauer: Von Caligari zu Hitler. Eine psychologische Geschichte des deutschen Films. 11. Aufl., Frankfurt a. M. 2021 (stw 479) ",
        "ziel": "Auseinandersetzung mit der Frühgeschichte des deutschen Films; Kennenlernen der filmsoziologischen und mentalitätsgeschichtlichen Überlegungen und Thesen Kracauers; Einsichtnahme in Zusammenhänge des Mediums &#39;Film&#39; mit gesellschaftspolitischen Entwicklungen in Deutschland vor, während und nach der Weimarer Republik; Einübung in Verfahren der Filmanalyse",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1139045,
        "name": "Von der Akte zum Algorithmus: Medien der Polizei",
        "inhalt": "Im Zentrum des Seminars steht die Frage, wie polizeiliche Praktiken durch Prozesse der Dokumentation und Beschreibung geprägt sind. Die Polizei wird dabei nicht bloß als eine staatliche Institution mit besonderen Aufgaben und einer bestimmten gesellschaftlichen Wirkung beschrieben, sondern als ein Medienverbund verstanden, das über Bilder, Texte und Daten operiert. Wir beschäftigen uns im Zuge dessen historisch mit der Entstehung der Polizei als Regierungsinstrument im 17. Jahrhundert und schreiben ihre Geschichte bis zum algorithmic policing der Gegenwart fort. Hier liegt ein besonderer Fokus: statistische Tools der Vorhersage, Überwachungssysteme und KI-gestützte Analyseformen nehmen zunehmend Einfluss auf die polizeiliche nehmen. Kritisch diskutiert werden die epistemischen Grundlagen und ästhetischen Formen solcher Systeme sowie ihre gesellschaftlichen und politischen Auswirkungen.",
        "ziel": "Das Seminar bietet den Teilnehmenden die Möglichkeit, medienästhetische und gesellschaftskritische Perspektiven miteinander zu verbinden, und regt dazu an, die Mechanismen und Wirkungsweisen polizeilicher Praktiken anhand von sehr unterschiedlichen Quellen (theoretischen Texten zur Polizeiwissenschaft, Fotografien, Filme oder Romane) zu analysieren. Ziel der Veranstaltung ist es, ein interdisziplinäres Verständnis für die Polizei als medienästhetisches und technologisches Phänomen zu entwickeln. Studierende sollen mediale Formen der Dokumentation und Kontrolle kritisch reflektieren und ihre Rolle in Bezug auf gesellschaftliche Machtverhältnisse analysieren können.",
        "semester_id": 48,
        "termine": []
    },
    {
        "id": 1139365,
        "name": "Wie sind Subjekte in einer objektiven Wirklichkeit möglich?",
        "inhalt": "Philosophie des Geistes     Ich glaube, dass die Philosophie des Geistes heute das wichtigste Gebiet innerhalb der Philosophie darstellt. Im Mittelpunkt der Veranstaltung stehen etwa folgende Fragen:  Was verstehen wir unter Wirklichkeit? Müssen wie sie uns dualistisch oder monistisch vorstellen? Was bedeutet die Subjekt-Objekt-Spaltung? In welchem Sinne sind die Ergebnisse  der exakten Wissenschaften objektiv? Sind sie wahr? Was macht ein Subjekt zum Subjekt? Sind Subjekte spezielle Objekte? Gibt es eine objektive Realität? Ist eine Ethik von  Individuen nicht in sich widersprüchlich?. . .     Von der Philosophie des Geistes führt ein unmittelbarer Weg zu den heute brennenden Fragen sowohl der Wirtschafts- und Medizinethik, als auch der Solidargemeinschaft und der Neurologie; deswegen scheint mir das Thema für einen einführenden Kurs sehr geeignet.",
        "ziel": "An einem paradigmatischen Beispiel sollen die Studenten die Art des philosophischen Denkens vorgestellt bekommen, möglichst gut verstehen und - in seminaristischer Form -  selbst üben können.",
        "semester_id": 48,
        "termine": []
    }
]""",input_promt='suche englische ergebnisse'))
    return

if __name__ == '__main__':
    main()