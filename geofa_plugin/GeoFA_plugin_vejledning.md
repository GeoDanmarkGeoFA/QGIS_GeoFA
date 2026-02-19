# Vejledning GeoFA plugin
### Installation af pluginet
For at hente pluginet skal du gøre således i QGIS:

    1.	I menuen ”Plugins”, klik på 'Administrér og Installér Plugins'
    2.	Søg efter GeoFA i den viste dialog
    3.	Klik på GeoFA i listen
    4.	Klik på 'Installér Plugin'
<img width="1272" height="721" alt="image" src="https://github.com/user-attachments/assets/5f2e02e9-5eaf-4e75-a752-80545bd092e0" />

### Opsætning af brugernavn og kode til GeoFA plugin
Plugin’et kan godt bruges uden at have adgang til brugernavn og kode, dog har man så kun adgang til at få vist lagene og ikke editerer i lagene. Indstillinger til pluginet findes ved at:

    1.	Åbn pluginets indstillinger. Dette kan gøres ved en af følgende måder
        A.	Klik på fanen 'Indstillinger' og tryk på 'Indstillinger...'
        B.	Søg efter GeoFA i søgefeltet i nederste venstre hjørne af QGIS og dobbeltklik på søge resultatet GeoFA (Indstillinger)
For at ændre brugernavn og adgangskode samt lagopsætning gøres følgende (se næste side):

    3.	Indtast brugernavn og kode i boksen som vist på billedet, hvis der trykkes og holdes på knappen, ”Vis” så kan man se den 
    indtastede adgangskode.
    4.	Hvis man har indtastet brugernavn og adgangskode, så har man mulighed for at tilgå WFS-T lag, dvs. lag der er mulige at 
    editerer. Hvis ikke vil man ikke have mulighed for at tjekke denne boks af.
    5.	Denne tjekboks kan tjekkes af hvis man ønsker adgang til lagene i testmiljøet.

Hvis man allerede har tilføjet GeoFA lag så vil datakilden blive opdateret afhængig af de indstillinger der ændres. Hvis man ønsker at have forskellige lag med forskellige datakilder, så kan man omdøbe laget i lagpanelet, f.eks. kan ”Skoledistrikter” omdøbes til ”Skoledistrikter (WFS- T)”.

**OBS!** Ens brugernavn og kode vil stå som klartekst i datakilden til ens lag, så man skal ikke dele QGIS projekter til eksterne partnere hvor lag er tilføjet med brugernavn og kode.

Når et lag er valgt, så indlæses det sammen med en række domæneværdtabeller. Disse domæneværditabeller er gjort private og kan ses ved at
trykke på ”Filter legend”.

<img width="423" height="286" alt="image" src="https://github.com/user-attachments/assets/8d0c9aa8-c8e5-4654-8431-576f75009de9" />

<img width="1549" height="905" alt="image" src="https://github.com/user-attachments/assets/9618d40b-289e-4652-bbc7-35bc01dbfd42" />

### Oprettelse af bruger
Hvis man mangler sit login eller skal oprettes som ny bruger send mail til support@geopartner.dk, i emnefeltet skrives ”GeoFA brugeroplysninger”

### Anvendelse af pluginet
Når pluginet er installeret er menuen GeoFA blevet tilføjet øverst i QGIS. Denne menu indeholder GeoFA temaer.

Et datasæt tilføjes til lagpanelet ved at klikke på det ønskede lag i menuen:

<img width="796" height="196" alt="image" src="https://github.com/user-attachments/assets/4e762061-340d-4be5-ac65-c3a8acf2e9a4" />

Datasæt fra GeoFA kan også fremsøges fra søgefeltet i nederste venstre hjørne af QGIS, og datasæt tilføjes ved at klikke på søgeresultatet:

<img width="684" height="397" alt="image" src="https://github.com/user-attachments/assets/67657254-ab8f-473e-bf57-c6b7fc119b54" />
