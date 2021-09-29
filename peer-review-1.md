Original at https://github.com/antonlep/opetussovellus/issues/1

# Vertaisarviointi
Näyttää todella hyvältä!

Sovellusta on melko mukava käyttää, vaikka minkäänlaista tyylitystä ei ole (ainakaan vielä) tehty. Käytettävyyttä parantaisi kuitenkin huomattavasti pidemmälle selkeämpi otsikointi ja ohjetekstit: esimerkiksi aloitussivulla sisäänkirjautumatta voisi lukea vaikkapa "kirjaudu sisään nähdäksesi kurssien sisällön". Olisi mielestäni myös aiheellista käyttää [semanttista HTML:ää](https://developer.mozilla.org/en-US/docs/Glossary/Semantics); nyt esimerkiksi listat ovat vain `<br>` -tageillä eroteltuja [`<ul>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul) tai [`<ol>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ol) sijaan ja elementtejä on eroteltu `<hr>` -tageillä, vaikka ne [on tarkoitettu](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/hr) "temaattisiin muutoksiin" — viivat olisi parempi tehdä tyylitiedostoilla. Tämä kaikki parantaisi sovelluksen käytettävyyttä erityisesti ei-graafisilla selaimilla ja esimerkiksi näytönlukijaohjelmistoihin tukeutuville käyttäjille. Surullisenkuuluisa esimerkki ohjelmasta jota on käytännössä mahdotonta käyttää näkövammaisena on [meille kaikille tuttu Sisu](https://www.hs.fi/kaupunki/helsinki/art-2000007984231.html).

Koodi on mielestäni vallan hyvin eroteltu osiin, eli se on mukavan modulaarinen. Funktiot ja muuttujat ovat järkevästi nimettyjä ja ne löytyvät sieltä mistä niitä lähtee intuitiivisesti etsimään. SQL-lauseet on osattu laittaa monirivisiin stringeihin, mutta varsinkin pidemmissä lauseissa voisi tekstiä muotoilla vähän paremmin esimerkiksi sisennyksin — nyt pitkiä lauseita on ainakin allekirjoittaneelle todella hankala käsitellä. Esimerkkinä `questions.py` rivit 34–39:
```sql
SELECT Q.id, Q.name, COALESCE(X.count,0) sum FROM courses Q LEFT JOIN
(SELECT A.id, A.name, COUNT(*) FROM courses A LEFT JOIN textquestions B
ON A.id = B.course_id WHERE B.id IN (SELECT B.id FROM textquestions B 
LEFT JOIN textanswers C ON B.id = C.question_id WHERE B.visible = true
AND user_id = :user_id AND B.answer = C.answer GROUP BY B.id)
GROUP BY A.id) X ON Q.id = X.id WHERE Q.visible = true
```
vastaan vaikkapa
```sql
SELECT Q.id, Q.name, COALESCE(X.count,0) sum
FROM courses Q LEFT JOIN (
    SELECT A.id, A.name, COUNT(*)
    FROM courses A LEFT JOIN textquestions B ON A.id = B.course_id
    WHERE B.id IN (
        SELECT B.id
        FROM textquestions B LEFT JOIN textanswers C ON B.id = C.question_id
        WHERE B.visible = true
        AND user_id = :user_id
        AND B.answer = C.answer
        GROUP BY B.id
    )
    GROUP BY A.id
) X ON Q.id = X.id
WHERE Q.visible = true
```
Toinen koodia selkiyttävä muutos olisi parempi [DRY](https://en.wikipedia.org/wiki/Don't_repeat_yourself). Tällä hetkellä reittien käsittelijät luovat turhaan suuret määrät muuttujia, joita käytetään samoilla nimillä vain kerran. Pahimpana esimerkkinä `routes.py` rivit 13–23:
```python
def course_pages(course_id):
    user_id = session["user_id"]
    course = courses.get_course(course_id)
    user_in_course = courses.check_if_user_in_course(user_id, course_id)
    textmaterial = courses.get_latest_textmaterial(course_id)
    textquestions = questions.get_active_textquestions(course_id)
    course_stats = questions.get_statistics_for_one_course(user_id, course_id)
    if course:
        return render_template("course.html", course=course, textmaterial=textmaterial,
                                textquestions=textquestions, course_stats=course_stats,
                                user_in_course=user_in_course)
```
vastaan vaikkapa
```python
def course_pages(course_id):
    user_id = session["user_id"]
    course = courses.get_course(course_id)
    if course:
        return render_template(
            "course.html",
            course=course,
            textmaterial=courses.get_latest_textmaterial(course_id),
            textquestions=questions.get_active_textquestions(course_id),
            course_stats=questions.get_statistics_for_one_course(user_id, course_id),
            user_in_course=courses.check_if_user_in_course(user_id, course_id)
        )
```