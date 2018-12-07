"""
Ein Modul für diverse scripte, die nirgens anders rein passen
"""

def erstelle_MO():
    """ erstellt alles rund um die Matheolympiade """
    from .models import WettbewerbPrinzipiell, WettbewerbKonkret, ArtErfolg, ArtTag, Tag
    # tags
    arttag, created = ArtTag.objects.get_or_create(title='Wettbewerb', plural='Wettbewerbe')
    tag_mo, created = Tag.objects.get_or_create(title='Mathematikolympiade', slug='MO', art=arttag)
    arttag, created = ArtTag.objects.get_or_create(title='Fachbereich', plural='Fachbereiche')
    tag_mathe, created = Tag.objects.get_or_create(title='Mathematik', slug='mathe', art=arttag)
    tag_physik, created = Tag.objects.get_or_create(title='Physik', slug='physik', art=arttag) # gehört nicht her, aber...
    arttag, created = ArtTag.objects.get_or_create(title='Klassenstufe', plural='Klassenstufen') # für später
    # erfolge
    preis1, created = ArtErfolg.objects.get_or_create(title='1.Preis', slug='1_preis', wichtung=10)
    preis2, created = ArtErfolg.objects.get_or_create(title='2.Preis', slug='2_preis', wichtung=7)
    preis3, created = ArtErfolg.objects.get_or_create(title='3.Preis', slug='3_preis', wichtung=4)
    preis4, created = ArtErfolg.objects.get_or_create(title='Anerkennung', slug='anerkennung', wichtung=2)
    # generische wettbewerbe
    bundeslaender = {kurz: name for kurz, name in (zeile.split() for zeile in """BW Baden-Württemberg
BY Bayern
BE Berlin
BB Brandenburg
HB Bremen
HH Hamburg
HE Hessen
MV Mecklenburg-Vorpommern
NI Niedersachsen
NW Nordrhein-Westfalen
RP Rheinland-Pfalz
SL Saarland
SN Sachsen
ST Sachsen-Anhalt
SH Schleswig-Holstein
TH Thüringen""".split('\n'))}
    for klasse in range(5, 13): 
        print(klasse)
        liste_mos_zu_klasse = []
        tag, created = Tag.objects.get_or_create(title='Klassenstufe %s' % klasse, slug='klasse%s' % klasse, art=arttag)
        if klasse>7:
            demo, created = WettbewerbPrinzipiell.objects.get_or_create(
                title='Bundesrunde der Mathematikolympiade, Klasse %s' % klasse, 
                slug='DeMO_%s' % klasse, 
                datum='Mai/Juni', 
                wichtung=8)
            demo.erfolgsarten.add(preis1, preis2, preis3, preis4)
            liste_mos_zu_klasse.append(demo)
        else:
            demo = None
        for kurz, land in bundeslaender.items():
            print(kurz)
            lamo, created = WettbewerbPrinzipiell.objects.get_or_create(
                title='Landesrunde der Matheolympiade in %s, Klasse %s' % (land, klasse), 
                slug='LaMO_%s_%s' % (kurz, klasse), 
                datum='Februar', 
                fortsetzung=demo, 
                wichtung=4)
            if not created:
                print('AAAH')
            remo, created = WettbewerbPrinzipiell.objects.get_or_create(
                title='Regionalrunde der Matheolympiade in %s, Klasse %s' % (land, klasse), 
                slug='ReMO_%s_%s' % (kurz, klasse), 
                datum='November', 
                fortsetzung=lamo, 
                wichtung=2)
            if not created:
                print('AAAH')
            lamo.erfolgsarten.add(preis1, preis2, preis3, preis4)
            remo.erfolgsarten.add(preis1, preis2, preis3)
            liste_mos_zu_klasse += [lamo, remo]
        for mo in liste_mos_zu_klasse:
            mo.tags.add(tag_mathe, tag_mo, tag)
            mo.slug_prefix = 'MO'
            try:
                mo.save()
            except:
                print(mo)

