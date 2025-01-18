get_result_orl_working = """ Ich werde dir eine Liste von Einträgen im JSON-Format bereitstellen. Deine Aufgabe ist es, aus dieser Liste die fünf Einträge auszuwählen, die am besten zu einem weiteren gegebenen Text (Kontext-Prompt) passen. Du sollst dabei nur den Textinhalt (ohne die `id`- und `semester_id`-Felder) berücksichtigen und die Einträge nach ihrer Relevanz für den gegebenen Kontext bewerten.

### Anforderungen:
1. **Input**: Du erhältst die folgende JSON-Struktur:
   ```json
   [
       {
           "id": <integer>,
           "name": <string>,
           "inhalt": <string>,
           "ziel": <string>,
           "date_string": <string>
       },
       ...
   ]
                 Jeder Eintrag enthält die oben genannten Felder.

                 Kontext-Prompt: Ein zusätzlicher Text wird als Kontext bereitgestellt. Die Relevanz eines Eintrags wird durch den Grad bestimmt, wie gut die Inhalte des Eintrags (name, inhalt, ziel, termine) zum Kontext-Prompt passen.

                 Output: Gib die fünf relevantesten Einträge zurück, basierend auf ihrer Übereinstimmung mit dem Kontext-Prompt. Das Format des Outputs soll wie folgt aussehen:
                 [
    {
        "id": <integer>,
        "name": <string>,
        "inhalt": <string>,
        "ziel": <string>,
        "date_string": <string>
    },
    ...
]
                 Beispiel:
                Falls die Eingabeliste folgende Struktur hat:
                 
                 [
    {
        "id": 1,
        "name": "Beispielkurs 1",
        "inhalt": "Dies ist ein "Kurs" über Philosophie.",
        "ziel": "Ein besseres "Verständnis der Philosophie zu erlangen." ",
        "date_string": "Montag 14:15 Uhr"
    },
    {
        "id": 2,
        "name": "Beispielkurs 2",
        "inhalt": "Ein Kurs über "Datenanalyse mit Python".",
        "ziel": "Grundlagen der Datenanalyse zu erlernen.",
        "date_string": "Dienstage 17:15 Uhr"
    },
    {
        "id": 35,
        "name": "Beispielkurs 3",
        "inhalt": "Die geschichte der Philosophie",
        "ziel": "Geschichtliche Entwicklung der philosophischen Konzepte.",
        "date_string": "No dates found"
    }
]
                 Und der Kontext lautet: "Bitte finde Kurse, die sich mit Philosophie befassen."

                Dann sollte die Rückgabe folgende Struktur haben:
                 
                 [
    {
        "id": 1,
        "name": "Beispielkurs 1",
        "inhalt": "Dies ist ein Kurs über Philosophie.",
        "ziel": "Ein besseres Verständnis der Philosophie zu erlangen.",
        "date_string": "Montag 14:15 Uhr"
    },
    {
        "id": 35,
        "name": "Beispielkurs 3",
        "inhalt": "Die geschichte der Philosophie",
        "ziel": "Geschichtliche Entwicklung der philosophischen Konzepte.",
        "date_string": "No dates found"
    }
]
                 
                 Wichtig:
Gib nur die fünf relevantesten Einträge in for eine eizigen json zurück.
Halte die Struktur des Outputs strikt ein.
Falls keine fünf relevanten Einträge gefunden werden können, gib nur die gefundenen zurück.
Es soll immer nur EINE EINZIGE Json mit den ergebnissen zurück gegeben werden.
Entfährne alle anführungszeichen aus den values der json.
Hier ist die JSON-Datenstruktur, auf die du die obigen Anweisungen anwenden sollst:"""


get_result = """ Ich werde dir eine Liste von Einträgen im JSON-Format bereitstellen. Deine Aufgabe ist es, aus dieser Liste ein bis 7 passende Einträge auszuwählen, die am besten zu einem weiteren gegebenen Text (Kontext-Prompt) passen. Du sollst dabei den Textinhalt berücksichtigen und die Einträge nach ihrer Relevanz für den gegebenen Kontext bewerten.

### Anforderungen:
1. **Input**: Du erhältst die folgende JSON-Struktur:
   ```json
   [
       {
           "id": <integer>,
           "name": <string>,
           "inhalt": <string>,
           "date_string": <string>
       },
       ...
   ]
                 Jeder Eintrag enthält die oben genannten Felder.

                 Kontext-Prompt: Ein zusätzlicher Text wird als Kontext bereitgestellt. Die Relevanz eines Eintrags wird durch den Grad bestimmt, wie gut die Inhalte des Eintrags (name, inhalt) zum Kontext-Prompt passen.

                 Output: Gib die fünf relevantesten Einträge zurück, basierend auf ihrer Übereinstimmung mit dem Kontext-Prompt. Das Format des Outputs soll wie folgt aussehen:
                 [
    {
        "id": <integer>,
        "name": <string>,
        "inhalt": <string>,
        "date_string": <string>
    },
    ...
]
                 Beispiel:
                Falls die Eingabeliste folgende Struktur hat:
                 
                 [
    {
        "id": 1,
        "name": "Beispielkurs 1",
        "inhalt": "Dies ist ein "Kurs" über Philosophie.",
        "date_string": "Montag 14:15 Uhr"
    },
    {
        "id": 2,
        "name": "Beispielkurs 2",
        "inhalt": "Ein Kurs über "Datenanalyse mit Python".",
        "date_string": "Dienstage 17:15 Uhr"
    },
    {
        "id": 35,
        "name": "Beispielkurs 3",
        "inhalt": "Die geschichte der Philosophie",
        "date_string": "No dates found"
    }
]
                 Und der Kontext lautet: "Bitte finde Kurse, die sich mit Philosophie befassen."

                Dann sollte die Rückgabe folgende Struktur haben:
                 
                 [
    {
        "id": 1,
        "name": "Beispielkurs 1",
        "inhalt": "Dies ist ein Kurs über Philosophie.",
        "date_string": "Montag 14:15 Uhr"
    },
    {
        "id": 35,
        "name": "Beispielkurs 3",
        "inhalt": "Die geschichte der Philosophie",
        "date_string": "No dates found"
    }
]
                 
                 Wichtig:
Gib nur relevante Einträge zurück, maximal 7 wenn du keinen findest gib einfach eine lehre datenstrucktur zurück.
Halte die Struktur des Outputs strikt ein.
Es soll immer nur EINE EINZIGE Json mit den ergebnissen zurück gegeben werden.
Entfährne alle anführungszeichen aus den values der json.
Hier ist die JSON-Datenstruktur, auf die du die obigen Anweisungen anwenden sollst:"""