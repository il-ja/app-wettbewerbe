Wettbewerbs-app
===============

Django-app zum speichern und darstellen der Datenbank mit einer komplexen Struktur von Wettbewerben und Veranstaltungen.

Kurzidee: neben Personen und Veranstaltungen gibt es Objekte für generische Wettbewerbe, die jeweils mit einem konkreten Wettbewerb pro Jahrgang verknüpft sind. Nachfolgende Stufe wird explizit im ForeignKey des generischen Wettbewerbs definiert, in jedem Jahr wird der Nachfolger mit der richtigen Jahrgangsnummer angefordert. Wettbewerbe gehören zu Veranstaltungen.
