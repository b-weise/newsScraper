import datetime
import os
from pathlib import Path

import pytest
from pandas import DataFrame

from source.classes.base_storage_manager import BaseStorageManager
from source.classes.db_manager import DBManager, RecordsMismatchException
from source.interfaces.db_tables import MatchingArticles, CachedUserAgents


def test_instance_success():
    db_filepath = Path('testing.db')
    dbm = DBManager(filepath=db_filepath)
    dbm.destroy()
    assert db_filepath.exists()
    os.remove(db_filepath)


@pytest.fixture
async def new_instance() -> DBManager:
    db_filepath = Path('testing.db')
    dbmanager = DBManager(filepath=db_filepath)
    yield dbmanager
    dbmanager.destroy()
    if db_filepath.exists():
        os.remove(db_filepath)


def test_interface_success(new_instance: DBManager):
    assert isinstance(new_instance, BaseStorageManager)


def test_basic_retrieve_success(new_instance: DBManager):
    result = new_instance.retrieve(columns=[MatchingArticles.ID])
    assert isinstance(result, DataFrame)


@pytest.mark.parametrize('input_data', [
    pytest.param(
        [MatchingArticles(
            Keyword='genealogistas',
            URL='https://www.pagina12.com.ar/803462-un-manto-de-caracoles-y-un-colibri',
            Title='Un manto de caracoles y un colibrí',
            Date=datetime.datetime.fromisoformat('2025-02-13T01:14:20-03:00'),
            Author='María Pia López',
            ImageURL='https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2025-02/913013-colibri-afp2.jpg',
            Body='“Promete un tiempo / en que la ferocidad no sea la única manera de tocarnos / los unos a los otros y dejarnos una huella. Y quién / no quiere esa promesa.”')]
    ),
    pytest.param(
        [MatchingArticles(
            Keyword='genealogistas',
            URL='https://www.pagina12.com.ar/95749-en-busca-de-la-genealogia-felina',
            Title='En busca de la genealogía felina',
            Date=datetime.datetime.fromisoformat('2018-02-16T02:40:46-03:00'),
            Author='Silvina Friera',
            ImageURL='https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2018-02/na31fo01_0.png',
            Body="""\
El amor por los felinos no admite moderación. El fanatismo que suscitan, en todas las épocas y culturas, es una pasión desmesurada. ¿Acaso existen las pasiones cautelosas y prudentes? Cómo no acordar con esa frase que plantea que “Dios creó al gato para concedernos el placer de acariciar a un tigre”. Los agnósticos y ateos se rinden ante la evidencia de esta especie de religión felinesca. “Me encanta en el gato ese temperamento independiente y casi ingrato que le impide apegarse a cualquiera; la indiferencia con que pasa del salón al tejado. Cuando lo acaricias se estira y arquea el lomo, es cierto, pero lo hace por el placer físico y no, como el perro, por esa tonta satisfacción que siente en amar y serle fiel a un dueño que devuelve el cumplido a patadas –decía François-René de Chateaubriand–. El gato vive solo, no necesita de la sociedad, no obedece excepto cuando él quiere, finge dormitar para ver más claramente y araña todo lo que puede”. En El tigre en la casa. Una historia cultural del gato (Sigilo), originalmente publicado en 1920 y que tradujo por primera vez al español Andrea Palet, con dibujos de Krysthopher Woods, el genial escritor y fotógrafo estadounidense Carl Van Vechten despliega una erudición descomunal al explorar las representaciones del gato en la ficción, la poesía, la pintura, la música, el folclore, las leyes, la religión y la historia. 
Van Vechten (1880-1964) –que fue periodista, crítico de música y teatro, ensayista, novelista y fotógrafo, y una de las figuras más iconoclastas de la Nueva York de principios del siglo pasado– escribe como si fuera un exquisito narrador inglés, con la espada de la ironía como su mejor aliada literaria. En su afán por revisitar la entusiasta genealogía felina, la perspectiva gatuna que adopta es un modo de ser y estar en el mundo. De pronto encuentra pequeñas maravillas, como la encantadora descripción del filósofo e historiador francés Hippolyte Taine: “Su lengua es esponja, cepillo, toalla y almohaza/ Y bien que sabe usarla/ Mi pobre trapo, más pequeño que un pulgar./ Su nariz toca la espalda, las patas traseras/ Cada trozo de piel rastrilla, escarba y allana/ ¿Acaso ha hecho más Goethe, podrá hacer más Voltaire?”. El escritor estadounidense -que como crítico fue uno de los descubridores de Irving Berlin y George Gershwin, y Gertrude Stein lo designó su albacea literario- propone una lectura política cuando advierte que el gato es “un anarquista aristocrático y tiránico”. 
Quizá lo más delicioso de Van Vechten es que no disimula su misantropía. Los gatos posiblemente piensen en los humanos como “una especie de árbol portátil, agradable para frotarse contra él, con ramas inferiores que ofrecen un asiento confortable y otras ramas altas de las que a veces caen trozos de cordero y otros frutos deliciosos”. Hay momentos donde no se puede evitar la carcajada. “Los gatos rara vez cometen errores, y nunca el mismo error dos veces. ¡Qué estúpido deben de encontrar al ser humano que constantemente tropieza con la misma piedra!”. Su defensa se aproxima a una sensibilidad que cuestiona el especismo, neologismo que se empezó a usar en los años 70. “El crimen del gato es que caza para sí mismo y no para el humano. ¿Hasta dueños de fábricas que se valen del trabajo infantil (…) me han dicho que los gatos son crueles!”, protesta el escritor que tomó más de 15.000 retratos fotográficos, que se conservan hoy en la Library of Congress (Washington), entre los que se destacan los de Bessie Smith, Marc Chagall, Truman Capote, Billie Holiday y Marlon Brandon.
El carácter místico del gato ha deleitado a sus admiradores y atemorizado a sus detractores a partir de que apareció en la historia, alrededor del 1.600 años antes de Cristo. Desde entonces ha sido reverenciado por los sacerdotes de Egipto, ha estado cercano a las brujas en la Edad Media, fue amigo de Mahoma, símbolo del tiempo en China; los felinos se pasean por el folclore y las leyendas de Europa, Asia y África. Van Vechten cita una frase del escritor británico Walter Scott: “¡Ah!, los gatos son unos tipos misteriosos. Tienen más cosas en la mente de las que nos imaginamos, sin duda a causa de su familiaridad con brujas y hechiceros”. No alcanzaría el espacio para dar cuenta de los proverbios que recopila. Algunos son magníficos. En Japón dicen: “Un perro recordará tres días de bondad durante tres años; un gato olvidará tres años de bondad en tres días”. Hay varios que provienen de la India: “Hasta el gato es un león en su propia guarida” o “El gato no caza ratones para Dios”.  
A Van Vechten no le gusta que en El pájaro azul, Maurice Maeterlinck –un amante de los perros– no trate muy bien al “tigre en miniatura”, al retratarlo como un oportunista que adula a sus amigos humanos para conseguir lo que quiere. “Pero ¿alguna vez adulan los gatos? Ninguno que yo haya conocido lo hace”, aclara el escritor. Entre sus preferencias elogia Diálogos de animales, de Colette. “Nadie como ella ha escrito acerca de los animales con una comprensión más empática” porque “los trata con subjetividad, intenta ponerse en su pellejo, los hace hablar por sí mismos”. Un capítulo aparte es el gato en la música. “Los gatos no abusan de la palabra como hacen los humanos; solo recurren a ella en los momentos importantes, para expresar amor, hambre, dolor, placer, peligro (…) Por eso es que su lenguaje es tan conmovedor. Y musical; el gatés conversacional, tanto el apasionado como el más coloquial, tiene una sonoridad única”.
El gato sobrevivirá porque “no es tan estúpido como el ser humano”. El libro de Van Vechten también emociona. “Feathers está muy cansada de este libro. Me lo ha dicho más de una vez. A veces mirándome con impaciencia mientras escribo. A veces con las patas, rascando con desdén las hojas de papel cuando las tiro al suelo. A veces, en mi mesa de trabajo, se interpone entre mis escritos y yo. Cuando empecé era una gatita, una bolita parecida a un crisantemo de pelo rojizo y rizado, naranja, blanco y negro, y ahora está a punto de convertirse en madre. Me hace sentir muy pequeño, muy poco importante (…) ¿Ves, Feathers?, estoy casi listo. Estoy escribiendo la última página. Puedes venir a mí ahora y pasar las horas en mi regazo”.""")]
    ),
])
def test_basic_store_success(new_instance: DBManager, input_data: list[DBManager.Base]):
    new_instance.store(input_data)
    result = new_instance.retrieve(columns=[MatchingArticles.ID])
    assert len(result) > 0


@pytest.mark.parametrize('input_data', [
    pytest.param(
        [MatchingArticles(
            Keyword='genealogistas',
            URL='https://www.pagina12.com.ar/803462-un-manto-de-caracoles-y-un-colibri',
            Title='Un manto de caracoles y un colibrí',
            Date=datetime.datetime.fromisoformat('2025-02-13T01:14:20-03:00'),
            Author='María Pia López',
            ImageURL='https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2025-02/913013-colibri-afp2.jpg',
            Body='“Promete un tiempo / en que la ferocidad no sea la única manera de tocarnos / los unos a los otros y dejarnos una huella. Y quién / no quiere esa promesa.”')]
    ),
    pytest.param(
        [MatchingArticles(
            Keyword='genealogistas',
            URL='https://www.pagina12.com.ar/95749-en-busca-de-la-genealogia-felina',
            Title='En busca de la genealogía felina',
            Date=datetime.datetime.fromisoformat('2018-02-16T02:40:46-03:00'),
            Author='Silvina Friera',
            ImageURL='https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2018-02/na31fo01_0.png',
            Body='El amor por los felinos no admite moderación. El fanatismo que suscitan, en todas las épocas y culturas, es una pasión desmesurada. ¿Acaso existen las pasiones cautelosas y prudentes? Cómo no acordar con esa frase que plantea que “Dios creó al gato para concedernos el placer de acariciar a un tigre”. Los agnósticos y ateos se rinden ante la evidencia de esta especie de religión felinesca. “Me encanta en el gato ese temperamento independiente y casi ingrato que le impide apegarse a cualquiera; la indiferencia con que pasa del salón al tejado. Cuando lo acaricias se estira y arquea el lomo, es cierto, pero lo hace por el placer físico y no, como el perro, por esa tonta satisfacción que siente en amar y serle fiel a un dueño que devuelve el cumplido a patadas –decía François-René de Chateaubriand–. El gato vive solo, no necesita de la sociedad, no obedece excepto cuando él quiere, finge dormitar para ver más claramente y araña todo lo que puede”. En El tigre en la casa. Una historia cultural del gato (Sigilo), originalmente publicado en 1920 y que tradujo por primera vez al español Andrea Palet, con dibujos de Krysthopher Woods, el genial escritor y fotógrafo estadounidense Carl Van Vechten despliega una erudición descomunal al explorar las representaciones del gato en la ficción, la poesía, la pintura, la música, el folclore, las leyes, la religión y la historia.')]
    ),
    pytest.param(
        [
            MatchingArticles(
                Keyword='genealogistas',
                URL='https://www.pagina12.com.ar/803462-un-manto-de-caracoles-y-un-colibri',
                Title='Un manto de caracoles y un colibrí',
                Date=datetime.datetime.fromisoformat('2025-02-13T01:14:20-03:00'),
                Author='María Pia López',
                ImageURL='https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2025-02/913013-colibri-afp2.jpg',
                Body='“Promete un tiempo / en que la ferocidad no sea la única manera de tocarnos / los unos a los otros y dejarnos una huella. Y quién / no quiere esa promesa.”'),
            MatchingArticles(
                Keyword='genealogistas',
                URL='https://www.pagina12.com.ar/95749-en-busca-de-la-genealogia-felina',
                Title='En busca de la genealogía felina',
                Date=datetime.datetime.fromisoformat('2018-02-16T02:40:46-03:00'),
                Author='Silvina Friera',
                ImageURL='https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2018-02/na31fo01_0.png',
                Body='El amor por los felinos no admite moderación. El fanatismo que suscitan, en todas las épocas y culturas, es una pasión desmesurada. ¿Acaso existen las pasiones cautelosas y prudentes? Cómo no acordar con esa frase que plantea que “Dios creó al gato para concedernos el placer de acariciar a un tigre”. Los agnósticos y ateos se rinden ante la evidencia de esta especie de religión felinesca. “Me encanta en el gato ese temperamento independiente y casi ingrato que le impide apegarse a cualquiera; la indiferencia con que pasa del salón al tejado. Cuando lo acaricias se estira y arquea el lomo, es cierto, pero lo hace por el placer físico y no, como el perro, por esa tonta satisfacción que siente en amar y serle fiel a un dueño que devuelve el cumplido a patadas –decía François-René de Chateaubriand–. El gato vive solo, no necesita de la sociedad, no obedece excepto cuando él quiere, finge dormitar para ver más claramente y araña todo lo que puede”. En El tigre en la casa. Una historia cultural del gato (Sigilo), originalmente publicado en 1920 y que tradujo por primera vez al español Andrea Palet, con dibujos de Krysthopher Woods, el genial escritor y fotógrafo estadounidense Carl Van Vechten despliega una erudición descomunal al explorar las representaciones del gato en la ficción, la poesía, la pintura, la música, el folclore, las leyes, la religión y la historia.'),
        ]
    ),
])
def test_matching_articles_io_success(new_instance: DBManager, input_data: list[DBManager.Base]):
    new_instance.store(input_data)
    result = new_instance.retrieve(table=MatchingArticles)
    for index in range(len(input_data)):
        assert input_data[index].URL == result.URL.iloc[index]
        assert input_data[index].Title == result.Title.iloc[index]
        assert input_data[index].Date.replace(tzinfo=None).isoformat() == result.Date.iloc[index].isoformat()
        assert input_data[index].Author == result.Author.iloc[index]
        assert input_data[index].ImageURL == result.ImageURL.iloc[index]
        assert input_data[index].Body == result.Body.iloc[index]


@pytest.mark.parametrize('input_data', [
    pytest.param(
        [
            CachedUserAgents(
                UserAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3',
            ),
            CachedUserAgents(
                UserAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.1',
            ),
        ]
    ),
])
def test_cached_useragents_io_success(new_instance: DBManager, input_data: list[DBManager.Base]):
    new_instance.store(input_data)
    result = new_instance.retrieve(table=CachedUserAgents)
    for index in range(len(input_data)):
        assert input_data[index].UserAgent == result.UserAgent.iloc[index]


@pytest.mark.parametrize('input_data', [
    pytest.param(
        [
            MatchingArticles(
                Keyword='genealogistas',
                URL='https://www.pagina12.com.ar/803462-un-manto-de-caracoles-y-un-colibri',
                Title='Un manto de caracoles y un colibrí',
                Date=datetime.datetime.fromisoformat('2025-02-13T01:14:20-03:00'),
                Author='María Pia López',
                ImageURL='https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2025-02/913013-colibri-afp2.jpg',
                Body='“Promete un tiempo / en que la ferocidad no sea la única manera de tocarnos / los unos a los otros y dejarnos una huella. Y quién / no quiere esa promesa.”'
            ),
            CachedUserAgents(
                UserAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3',
            ),
            CachedUserAgents(
                UserAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.1',
            ),
        ]
    ),
    pytest.param(
        [
            CachedUserAgents(
                UserAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3',
            ),
            CachedUserAgents(
                UserAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.1',
            ),
            MatchingArticles(
                Keyword='genealogistas',
                URL='https://www.pagina12.com.ar/95749-en-busca-de-la-genealogia-felina',
                Title='En busca de la genealogía felina',
                Date=datetime.datetime.fromisoformat('2018-02-16T02:40:46-03:00'),
                Author='Silvina Friera',
                ImageURL='https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2018-02/na31fo01_0.png',
                Body='El amor por los felinos no admite moderación. El fanatismo que suscitan, en todas las épocas y culturas, es una pasión desmesurada. ¿Acaso existen las pasiones cautelosas y prudentes? Cómo no acordar con esa frase que plantea que “Dios creó al gato para concedernos el placer de acariciar a un tigre”. Los agnósticos y ateos se rinden ante la evidencia de esta especie de religión felinesca. “Me encanta en el gato ese temperamento independiente y casi ingrato que le impide apegarse a cualquiera; la indiferencia con que pasa del salón al tejado. Cuando lo acaricias se estira y arquea el lomo, es cierto, pero lo hace por el placer físico y no, como el perro, por esa tonta satisfacción que siente en amar y serle fiel a un dueño que devuelve el cumplido a patadas –decía François-René de Chateaubriand–. El gato vive solo, no necesita de la sociedad, no obedece excepto cuando él quiere, finge dormitar para ver más claramente y araña todo lo que puede”. En El tigre en la casa. Una historia cultural del gato (Sigilo), originalmente publicado en 1920 y que tradujo por primera vez al español Andrea Palet, con dibujos de Krysthopher Woods, el genial escritor y fotógrafo estadounidense Carl Van Vechten despliega una erudición descomunal al explorar las representaciones del gato en la ficción, la poesía, la pintura, la música, el folclore, las leyes, la religión y la historia.'
            ),
        ]
    ),
    pytest.param(
        [
            CachedUserAgents(
                UserAgent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1.1 Safari/605.1.1',
            ),
            MatchingArticles(
                Keyword='genealogistas',
                URL='https://www.pagina12.com.ar/95749-en-busca-de-la-genealogia-felina',
                Title='En busca de la genealogía felina',
                Date=datetime.datetime.fromisoformat('2018-02-16T02:40:46-03:00'),
                Author='Silvina Friera',
                ImageURL='https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2018-02/na31fo01_0.png',
                Body='El amor por los felinos no admite moderación. El fanatismo que suscitan, en todas las épocas y culturas, es una pasión desmesurada. ¿Acaso existen las pasiones cautelosas y prudentes? Cómo no acordar con esa frase que plantea que “Dios creó al gato para concedernos el placer de acariciar a un tigre”. Los agnósticos y ateos se rinden ante la evidencia de esta especie de religión felinesca. “Me encanta en el gato ese temperamento independiente y casi ingrato que le impide apegarse a cualquiera; la indiferencia con que pasa del salón al tejado. Cuando lo acaricias se estira y arquea el lomo, es cierto, pero lo hace por el placer físico y no, como el perro, por esa tonta satisfacción que siente en amar y serle fiel a un dueño que devuelve el cumplido a patadas –decía François-René de Chateaubriand–. El gato vive solo, no necesita de la sociedad, no obedece excepto cuando él quiere, finge dormitar para ver más claramente y araña todo lo que puede”. En El tigre en la casa. Una historia cultural del gato (Sigilo), originalmente publicado en 1920 y que tradujo por primera vez al español Andrea Palet, con dibujos de Krysthopher Woods, el genial escritor y fotógrafo estadounidense Carl Van Vechten despliega una erudición descomunal al explorar las representaciones del gato en la ficción, la poesía, la pintura, la música, el folclore, las leyes, la religión y la historia.'
            ),
            CachedUserAgents(
                UserAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3',
            ),
        ]
    ),
])
def test_store_failure(new_instance: DBManager, input_data: list[DBManager.Base]):
    with pytest.raises(RecordsMismatchException):
        new_instance.store(input_data)
