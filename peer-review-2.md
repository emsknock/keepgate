Original at https://github.com/henriimmonen/UniMarket/issues/3

Hyvältä vaikuttaa!

Sivuja on yleisesti melko helppo käyttää; mukavuutta parantaisi paljon parempi linkitys taaksepäin — nyt navigointi tapahtuu pääosin selaimen omalla "edellinen sivu" -napilla. Tyylitystä on tehty ja se on ehdoton plussa. Sivujen HTML voisi olla semanttisempaa: tällä hetkellä listat eivät ilmeisesti käytä <ul> tai <ol> -tagejä (paitsi flaskin flash-viestit) ja lomakkeet käyttävät <p> -tagejä kenttien erotteluun vaikka <label> kommunikoisi merkityksiä paremmin.

Koodi on eroteltu hyvin osiin ja funktiot ja muuttujat on mielestäni ihan järkevästi nimettyjä. Ole kuitenkin tarkka kirjoitustyylin johdonmukaisuudesta: nyt nimiä on välillä kirjoitettu tyyliohjeen vastaisesti camelCase:llä ja välillä oikein snake_case:llä ja sekä python-koodista, että HTML:stä löytyy ylimääräisiä välilyöntejä ja väärin sisennettyjä rivejä. Joitakin nimiä voisi myös vielä miettiä uudelleen ja nimetä kuvaavammin: esimerkiksi tiedoston templates/form.html nimestä ei oikeastaan voi lainkaan päätellä, mitä kyseisellä sivulla tehdään.

HTML-pohjat ovat tällä hetkellä turhaan toisteisia; jokaisessa on samat doctype- ja metatagit. Ohjeita tämän välttämiseen kurssimateriaalin 4. osan ulkoasun toteutus -kohdassa.

Hyvää työtä!