import pytest

from source.classes.base_news_scraper import BaseNewsScraper, UninitializedWebsiteHandler
from source.classes.p12_scraper import P12Scraper
from source.classes.website_handler import NonCompliantURL


@pytest.fixture
async def new_instance() -> P12Scraper:
    p12scraper = P12Scraper()
    yield p12scraper
    await p12scraper.destroy()


@pytest.fixture
async def new_initialized_instance(new_instance: P12Scraper) -> P12Scraper:
    await new_instance.initialize_website_handler()
    return new_instance


def test_interface_success(new_instance: P12Scraper):
    assert isinstance(new_instance, BaseNewsScraper)


@pytest.mark.parametrize('input_url,output_title', [
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas', 'De genealogistas y analizantes'),
    pytest.param('https://www.pagina12.com.ar/775639-el-futuro-de-la-ia-y-su-impacto-en-el-conocimiento-cambiara-',
                 'El futuro de la IA y su impacto en el conocimiento: ¿cambiará la forma en que pensamos?'),
    pytest.param('https://www.pagina12.com.ar/591520-especialistas-argentinos-crean-un-robot-capaz-de-descubrir-f',
                 'Especialistas argentinos crean un robot capaz de descubrir fallas en las tuberías de cualquier ciudad'),
    pytest.param('https://www.pagina12.com.ar/810583-cambio-el-mundo',
                 'Cambió el mundo'),
])
async def test_get_title_success(new_initialized_instance: P12Scraper, input_url: str, output_title: str):
    title = await new_initialized_instance.get_title(input_url)
    assert title == output_title


@pytest.mark.parametrize('input_url', [
    pytest.param('https://www.pagina12.com.ar/349353471/'),
    pytest.param('https://www.pagina12.com.ar/349353471/test'),
    pytest.param('https://www.pagina12.com.ar/andytow/'),
    pytest.param('https://www.pagina12.com.ar/andytow/test'),
])
async def test_get_title_failure(new_initialized_instance: P12Scraper, input_url: str):
    with pytest.raises(NonCompliantURL):
        await new_initialized_instance.get_title(input_url)


async def test_get_title_call_failure(new_instance: P12Scraper):
    with pytest.raises(UninitializedWebsiteHandler):
        await new_instance.get_title('https://www.pagina12.com.ar/800250-genealogistas')


@pytest.mark.parametrize('input_url,output_date', [
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas', '30 de enero de 2025 - 00:34'),
    pytest.param('https://www.pagina12.com.ar/775639-el-futuro-de-la-ia-y-su-impacto-en-el-conocimiento-cambiara-',
                 '19 de octubre de 2024 - 00:01'),
    pytest.param('https://www.pagina12.com.ar/591520-especialistas-argentinos-crean-un-robot-capaz-de-descubrir-f',
                 '25 de septiembre de 2023 - 23:30'),
    pytest.param('https://www.pagina12.com.ar/810583-cambio-el-mundo',
                 '14 de marzo de 2025 - 00:01'),
])
async def test_get_date_success(new_initialized_instance: P12Scraper, input_url: str, output_date: str):
    date = await new_initialized_instance.get_date(input_url)
    assert date == output_date


@pytest.mark.parametrize('input_url', [
    pytest.param('https://www.pagina12.com.ar/349353471/'),
    pytest.param('https://www.pagina12.com.ar/349353471/test'),
    pytest.param('https://www.pagina12.com.ar/andytow/'),
    pytest.param('https://www.pagina12.com.ar/andytow/test'),
])
async def test_get_date_failure(new_initialized_instance: P12Scraper, input_url: str):
    with pytest.raises(NonCompliantURL):
        await new_initialized_instance.get_date(input_url)


async def test_get_date_call_failure(new_instance: P12Scraper):
    with pytest.raises(UninitializedWebsiteHandler):
        await new_instance.get_date('https://www.pagina12.com.ar/800250-genealogistas')


@pytest.mark.parametrize('input_url,output_author', [
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas', 'Alejandro Benedetto'),
    pytest.param('https://www.pagina12.com.ar/775639-el-futuro-de-la-ia-y-su-impacto-en-el-conocimiento-cambiara-',
                 'Dylan Resnik'),
    pytest.param('https://www.pagina12.com.ar/591520-especialistas-argentinos-crean-un-robot-capaz-de-descubrir-f',
                 'María Ximena Pérez'),
    pytest.param('https://www.pagina12.com.ar/810583-cambio-el-mundo',
                 'Emir Sader'),
])
async def test_get_author_success(new_initialized_instance: P12Scraper, input_url: str, output_author: str):
    author = await new_initialized_instance.get_author(input_url)
    assert author == output_author


@pytest.mark.parametrize('input_url', [
    pytest.param('https://www.pagina12.com.ar/349353471/'),
    pytest.param('https://www.pagina12.com.ar/349353471/test'),
    pytest.param('https://www.pagina12.com.ar/andytow/'),
    pytest.param('https://www.pagina12.com.ar/andytow/test'),
])
async def test_get_author_failure(new_initialized_instance: P12Scraper, input_url: str):
    with pytest.raises(NonCompliantURL):
        await new_initialized_instance.get_author(input_url)


async def test_get_author_call_failure(new_instance: P12Scraper):
    with pytest.raises(UninitializedWebsiteHandler):
        await new_instance.get_author('https://www.pagina12.com.ar/800250-genealogistas')


@pytest.mark.parametrize('input_url,output_image_url', [
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas',
                 'https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2025-01/907602-ro08fo0130web_0.jpg'),
    pytest.param('https://www.pagina12.com.ar/775639-el-futuro-de-la-ia-y-su-impacto-en-el-conocimiento-cambiara-',
                 'https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2024-10/881749-inteligencia-20artificial.jpg'),
    pytest.param('https://www.pagina12.com.ar/591520-especialistas-argentinos-crean-un-robot-capaz-de-descubrir-f',
                 'https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2023-09/770295-20-a-20gabriel-20iglesias.jpg'),
    pytest.param('https://www.pagina12.com.ar/810583-cambio-el-mundo',
                 'https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2025-03/920791-21-20op1-efe.jpg'),
])
async def test_get_image_url_success(new_initialized_instance: P12Scraper, input_url: str, output_image_url: str):
    image_url = await new_initialized_instance.get_image_url(input_url)
    assert image_url == output_image_url


@pytest.mark.parametrize('input_url', [
    pytest.param('https://www.pagina12.com.ar/349353471/'),
    pytest.param('https://www.pagina12.com.ar/349353471/test'),
    pytest.param('https://www.pagina12.com.ar/andytow/'),
    pytest.param('https://www.pagina12.com.ar/andytow/test'),
])
async def test_get_image_url_failure(new_initialized_instance: P12Scraper, input_url: str):
    with pytest.raises(NonCompliantURL):
        await new_initialized_instance.get_image_url(input_url)


async def test_get_image_url_call_failure(new_instance: P12Scraper):
    with pytest.raises(UninitializedWebsiteHandler):
        await new_instance.get_image_url('https://www.pagina12.com.ar/800250-genealogistas')


@pytest.mark.parametrize('input_url,output_body', [
    pytest.param('https://www.pagina12.com.ar/800250-genealogistas', """\
"Necesitamos la historia, pero de otra manera que el refinado paseante por el jardín de la ciencia, por más que este mire con altanero desdén nuestras necesidades y apremios rudos y simples. Necesitamos la historia para la vida y la acción, no para apartamos de la vida y la acción, y menos para encubrir la vida egoísta y la acción vil y cobarde" (Friedrich Nietzsche).
En la segunda intervención intempestiva titulada "Sobre la utilidad y los perjuicios de la historia para la vida", Friedrich Nietzsche se dispone analizar cada uno de los modos en que se presenta, en su forma platónico-hegeliana, la historia en el mundo moderno. Pasará revista a sus características, utilidades y perjuicios en relación a lo que él llama vida. El diagnóstico de Nietzsche en aquel momento era el siguiente: Europa, fines del siglo XIX, sufre de un mal completamente nuevo, raro y sin precedentes: “padece de una saturación, una hipertrofia, histórica”. El clínico Nietzsche se dedicará a indagar e investigar tan extraño síndrome, no sin prescribir algún que otro remedio.
Este texto está escrito y publicado entre los años 1873 y 1876. Por aquellos tiempos en los ámbitos académicos de la Alemania unificada, fortalecida y victoriosa, se contempla una fuerte hegemonía de los grandes pensadores ilustrados, Kant y, sobre, todo Hegel. Los neokantianos y neohegelianos pululaban por todas partes. El conocimiento científico, la actividad crítica y la Historia tienen su momento de gracia. Si al siglo XIX se lo ha denominado el siglo de la Historia, esto encuentra su razón más nítida en Alemania.
En el inicio del texto Friedrich Nietzsche aclara lo siguiente: "Es intempestiva esta consideración porque trato de interpretar como un mal, una enfermedad, un defecto, algo de lo que nuestra época está, con razón, orgullosa: su cultura Histórica". 
Es preciso señalar que por esos años los alemanes estaban tan poco orgullosos de Schopenhauer como fascinados por el gran Hegel y Nietzsche, como él mismo lo decía, todavía amaba al gran impugnador del hegelianismo. Sin embargo, Nietzsche no está discutiendo con los pensadores inscriptos en lo que se conoce como historicismo alemán. Como tampoco defendiendo o reivindicando a Schopenhauer. 
Por el contrario, puede sostenerse en relación a los primeros, en base a la influencia que ejercieron los trabajos de Nietzsche sobre Max Weber (representante central del historicismo), admitida por este último, que la producción del genealogista fue tan decisiva como valiosa para muchas de las mejores cabezas de esa corriente. 
A quienes sí tiene en la mira Nietzsche en este escrito es, sin dudas: al positivismo encarnado en la figura del señor Comte y a los hegelianos, específicamente al teólogo Strauss y al profesor Feuerbach. Ya les tocará a los utilitaristas ingleses, Spencer, Paul Ree y otros, aquí sólo los mira de reojo. 
Aclaramos que no todos los hegelianos se hallaban en la mira del cazador, Nietzsche mismo reconoce al "viejo profesor Bruno Bauer", maestro de Karl Marx, como a uno de sus más atentos lectores y defensores.
Entonces, Nietzsche pelea contra dos frentes: ni la idolatría de los hechos, puesto que estos son "siempre estúpidos y, en todo tiempo, han sido más semejantes a una vaca que a un Dios"; ni las ilusiones historicistas con sus graves consecuencias políticas: "el que ha aprendido a doblar el espinazo ante el poder de la historia acabará por decir mecánicamente, a la manera china, sí a todo poder, sea este un gobierno, una opinión pública o una mayoría numérica, y moverá sus miembros exactamente al ritmo en que tal poder tire los hilos". 
El que cree en el ilimitado poder de la historia deja de creer en su deseo y se convierte en un fascinado secuaz de lo existente. Y es así que no puede crear nada nuevo. Solo reproducción, imitación, esclavitud. 
Es que el problema de la sobresaturación histórica conduce, según Nietzsche, a varios puertos, todos fatalmente oscuros:
·A la separación contradictoria entre lo interno y lo externo. De este modo debilita fuertemente el accionar cotidiano de cada sujeto, de cada pueblo. Se crea un mundo interior completamente desvinculado con el acontecer presente. Se impone el imperio de la siesta provinciana. El ego, el gran conocedor, íntimo y sapiente yo, idéntico a sí mismo, es para Nietzsche uno de los mayores ideales construidos por el espíritu de la decadencia y el resentimiento.
·Hace que una época se imagine poseer la más rara de las virtudes, la justicia, en grado superior a cualquier otra época. Solo su retraso en el carnaval de la historia les da lugar a creerse capaces de juzgar lo que fue.
·Perturba los lazos sociales y amorosos del pueblo he impide que llegue a superarse, a construir lazos más fuertes y mayúsculos. Ancla pesada que inmoviliza las fuerzas vitales, las amarra y sujeta en el circo de la imitación.
·Implanta la creencia siempre nociva en la vejez de la humanidad, de ser el fruto tardío y epígono de un desarrollo continuo. En consecuencia, instaura una cultura encanecida, seria, responsable, incapaz de moverse con fuerza.
·Induce a una época a caer en el estado de ironía hacia sí misma luego, la actitud más peligrosa, el cinismo. "En esta actitud una época evoluciona más y más en la dirección de un practicismo calculador y egoísta que paraliza y, finalmente, destruye las fuerzas vitales".
***
"El hombre contempla con envidia a los animales porque él no quiere vivir más que como ellos sin hartazgo ni dolor. El hombre pregunta acaso al animal - ¿Por qué no me hablas de tu felicidad y te limillas a mirarme? El animal quisiera responder y decirle; - Esto pasa porque yo siempre olvido lo que iba a decir- pero, de repente, olvidó también esta respuesta y calló, de modo que el hombre se quedó sorprendido..." (F. N.)
En medio de una cultura que eleva los estudios y el conocimiento histórico al más noble pedestal, Nietzsche habla de lo a-histórico. El hombre se sorprende de sí mismo porque no aprende, no puede, no quiere olvidar y queda, siempre, encadenado al pasado. Nietzsche invita a los lectores a considerar la siguiente tesis: "Tanto lo histórico y lo a-histórico son igualmente necesarios para la salud de los cuerpos, los pueblos, las culturas".
El lugar de lo a-histórico impide al pasado convertirse en sepulturero del presente. Quien no sea capaz de instalarse en ese espacio sin tiempo en el que solo importa lo que está por nacer, sustraído, en el umbral del momento, de todo lo que una vez fue, en esa especie de atmósfera enrarecida desprendida del continuo rumiar de la historia, no podrá alcanzar la alegría ni, menos aún, alegrar a los otros.
Llegados a este punto, es necesario hacer una aclaración. 
La hipertrofia de la que habla Nietzsche es solidaria a la cultura del olvido y el silencio. La saturación histórica impide que la memoria de un pueblo esté activa. La memoria no es sinónimo del culto a la historia. Sirve a un pueblo para recordar qué no pasó en lo que pasó o, lo que nunca deja de pasar. 
La memoria está viva y quiere seguir viviendo, luchando, resistiendo contra la historia porque quiere historizarse. 
Lo que está haciendo Nietzsche no es una proclama y una apología del olvido en contra de la memoria. 
Todo lo contrario, nos recuerda que el culto al pasado interrumpe la memoria, la congela, y nos hace olvidar, frecuentemente, lo que está vivo en todo presente."""),
    pytest.param('https://www.pagina12.com.ar/775639-el-futuro-de-la-ia-y-su-impacto-en-el-conocimiento-cambiara-', """\
La inteligencia artificial ya aparece como una herramienta más de la vida cotidiana. Desde su irrupción popular, tan solo dos años atrás con el famoso ChatGPT, este desarrollo creció a un ritmo exponencial y está presente en el celular, en el trabajo, en las aulas y hasta en las galerías de arte. Pero la IA no es una herramienta más. Así lo explica en su último libro, Nexus, el historiador israelí Yuval Noah Harari, donde afirma que si bien no todos pueden ser expertos en inteligencia artificial, sí todos deben tener presente que esta “es la primera tecnología de la historia que puede tomar decisiones y generar nuevas ideas por sí misma”.
Harari dice que hasta ahora toda decisión sobre el uso de una herramienta terminaba en el humano. “Los cuchillos y las bombas no deciden por sí mismos a quién matar”, aclara. Pero la IA sí puede avanzar en este tipo de decisiones. Y no hace falta irse a un escenario bélico para verlo: puede decidir, por ejemplo, cuáles son los datos más importantes de un documento a la hora de resumirlo o qué palabras usar para completar un formulario.
Parados en este escenario se abre una cascada de preguntas acerca del futuro. Consultados por Página|12, un grupo de especialistas en IA respondió a una de ellas: ¿puede la inteligencia artificial cambiar la forma en que piensan, aprenden y generan nuevo conocimiento los humanos?
Que lo responda la IA
Carolina Tramallino es profesora adjunta de Lingüística General en la Facultad de Humanidades y Artes de la Universidad Nacional de Rosario e investigadora del Conicet en IRICE. Sus publicaciones se centran en el área de la lingüística computacional y de la inteligencia artificial. Desde allí hizo una serie de artículos donde indaga sobre cómo los estudiantes universitarios usan la IA en sus trayectorias académicas. En una publicación que hizo en la revista TE&ET reveló que un 90% de los estudiantes entrevistados aseguró haber usado el ChatGPT en ambientes educativos para resolver dudas relacionadas con los temas de estudio, estructurar textos, generar ideas, redactar mails o realizar correcciones de redacción.
Fernando Juca Maldonado, docente del área de tecnología de la Universidad Metropolitana, sede Machala, de Ecuador, publicó una investigación similar donde reveló que de un total de 247 alumnos encuestados, solo un 12% no estaba familiarizado con la IA. Los propios estudiantes reconocieron que usan esta herramienta para responder cuestionarios (18%), generar ideas (14%), analizar información (14%), resumir contenidos (10%) y generar contenido (8%) entre otras funciones.
Que la IA está instalada como una herramienta más en aquellos espacios clave de la enseñanza y generación de conocimiento es una realidad. Ahora cabe preguntarse qué consecuencias tendrá a largo plazo.
La IA y las tareas cognitivas
“La tecnología, por lo menos desde la revolución industrial, siempre reemplazó trabajo humano. Durante mucho tiempo lo que reemplazaba la tecnología, incluida la máquina de vapor, era el trabajo físico, la energía humana”, explicó Mariano Zukerfeld, doctor en Ciencias Sociales, investigador del Conicet y parte del Equipo de Estudios sobre Tecnología, Capitalismo y Sociedad.
El escenario cambió con la irrupción del capitalismo digital, que tuvo una primera etapa que fue desde mediados de 1970 hasta 2010 y una segunda etapa desde entonces caracterizada por las plataformas y la IA. “En la primera fase se empezaron a reemplazar tareas cognitivas rutinarias, por ejemplo, lo que hace un procesador de texto o una planilla de cálculo. Lo mismo respecto de aquellas tareas manuales rutinarias: la robótica empezó a reemplazar tareas físicas”.
“Lo novedoso desde 2005 es que se empezaron a reemplazar tareas cognitivas no rutinarias. Estas son, por ejemplo, las tareas creativas, que se consideraban reservadas para los humanos porque tenían un carácter de innovación, algo que era de creación. Esas tareas empezaron a ser realizadas de manera silenciosa, opinable, pero ya ahora de forma muy visible y asumida por algoritmos”, explicó.
Ai-Da, la robot artista. 
Un ejemplo claro de esto está asociado con una noticia de los últimos días: el robot Ai-Da, un humanoide dotado de inteligencia artificial, caracterizado con un cuerpo humano y brazos mecánicos, realizó una obra que será subastada el próximo 31 de octubre con un precio base de 130.000 dólares.
La coevolución del pensamiento
Por su lado, Ricardo Andrade, licenciado en Letras, filósofo de la tecnología y becario del Conicet, explicó a este diario que efectivamente la irrupción de la IA implica un “gran reto a nivel educativo y en relación con problemas filosóficos y sociológicos”. Sin embargo, consideró que este reemplazo no tiene por qué ser necesariamente algo negativo.
“No hablaría directamente de una pérdida de creatividad. Habrá más bien un cambio en términos de coevolución. ¿Por qué? Porque a medida que la inteligencia artificial se perfeccione, puede proporcionarnos herramientas para explorar con mayor detalle conocimientos y procesar información que, sin su ayuda, sería muy difícil avanzar”, sostuvo.
Y añadió: “Sería importante apropiarse de esta conquista tecnológica para pensar en cómo ese procesamiento de información puede ofrecer herramientas para entender y abordar la realidad a través del conocimiento. En este sentido, la tecnología y la inteligencia artificial modificarán nuestros comportamientos y la forma en que generamos conocimientos, ya que tendremos que pensar en función de lo que estas herramientas desarrollen. Así, surge la tensión coevolutiva”.
Red flags, dudas y desafíos
Tramallino consideró, tras estudiar el tema en ámbitos universitarios, que “hay que alfabetizar para brindar herramientas que se relacionen con la selección de la información, con poder discernir la calidad de los datos y que se ejerciten las habilidades de inteligencia lingüística” frente al avance de las herramientas generativas. “El problema es que podemos perder todas las reflexiones meta-lingüísticas que implican activar saberes. Como, por ejemplo, pensar en qué sinónimo puedo elegir para una palabra, realizar todas las asociaciones de sentido y pensar cómo puedo expresar con otras palabras una misma idea”, dijo.
“La lectura implica una interacción con el texto. Cuando leo, elaboro un significado que es resultado de una confluencia entre el sujeto, el texto y los factores contextuales. En este caso, no hay sujeto. No hay un enunciador en las respuestas de la IA, no hay un sujeto que se apropie del lenguaje. Carecemos de todo ese contexto de producción”, afirmó sobre el uso de estas herramientas en los ámbitos educativos y alertó sobre la falsa sensación de objetividad que pueden brindar estos programas.
Sobre este punto de la objetividad, aclaró: "Lo peligroso es que se crea el efecto ilusorio de una objetividad. Es un texto que no está atravesado por la lectura propia. Podemos caer en el peligro de creer que la ciencia es simple y objetiva en este afán de querer crear una respuesta. Lo preocupante es que impide tener noción de los diferentes puntos de vista cuando lo más importante es poder generar un pensamiento crítico. Se pierde la capacidad crítica del estudiante que empieza con la gestión de la información, seguida de la comprensión lectora".
Por su lado, Juca Maldonado añadió: “Algunos trataban de aprovecharse del hecho de que generaba todo y no había que hacer esfuerzo, otros para que los ayude a generar ideas. Dentro del ámbito académico sigue siendo un desafío tanto para estudiantes como para docentes cómo implementarla de manera ética sin que te suplante. Porque ese es el riesgo”.
Maldonado tomó la idea de Harari y puso la mirada hacia adelante: “La IA es el primer invento autónomo del humano. Ahí está el rol de tratar de aprovechar el uso de la tecnología y que sea una herramienta más para el proceso de aprendizaje. No es usarla para que haga algo por mí. El tema va más allá, porque es un agente autónomo que puede convertirse en un asistente para hacer el día a día mejor”. O peor, se podría pensar. Y de qué depende es aún una pregunta abierta."""),
    pytest.param('https://www.pagina12.com.ar/591520-especialistas-argentinos-crean-un-robot-capaz-de-descubrir-f', """\
Ingenieros de la Universidad Nacional de San Luis desarrollaron un robot diseñado para la exploración de cañerías de efluentes. Denominado EC-01, el dispositivo permite inspeccionar las principales tuberías de cualquier ciudad. Con dimensiones compactas de 40 centímetros de largo y equipado con ocho ruedas, este equipo de plástico especial resiste los efectos corrosivos de los ácidos presentes en las cañerías. También, tiene la capacidad de transmitir imágenes en tiempo real con una cámara que gira 360 grados y con una luz LED que puede iluminar los lugares más oscuros. Además de innovadora, la herramienta podría reemplazar los artefactos de origen extranjero que usan las empresas en la actualidad.
“La idea surgió cuando Obra Sanitaria Mercedes, el organismo que presta servicios de agua potable y depuración de efluentes, nos contó que alquilaban un dispositivo robótico de origen extranjero con la finalidad de explorar ramales de sus cañerías. Sin embargo, esta tecnología no estaba siempre disponible y su costo era oneroso”, cuenta Gabriel Iglesias, docente e investigador de la Facultad de Ingeniería y Ciencias Agropecuarias de la UNSL.
Lo que hace que este artefacto sea excepcional es su capacidad para navegar por cañerías de 16 centímetros de diámetro, la medida estándar en las redes principales de saneamiento. Los operadores pueden controlar el EC-01 desde una computadora conectada al robot, lo que les permite visualizar en tiempo real lo que la cámara captura. Esto facilita la detección de cualquier defecto, daño o bloqueo en la cañería, e incluso proporciona la distancia a la que se encuentra el problema.
Información rápida y precisa
La ventaja clave del robot puntano radica en su capacidad para localizar y solucionar problemas de manera certera. Así, evita la necesidad de excavar grandes áreas de calles o aceras para encontrar la causa de un bloqueo o daño en la red cloacal.
“El objetivo principal es localizar fallas en el interior de las cañerías de efluentes, que permitan informar el tipo de anomalía antes de realizar una intervención. Como el dispositivo indica de forma precisa la ubicación, evita la rotura de una cuadra completa para cambiar el tramo parcial de tubería donde se encuentra la falla”, enfatiza Iglesias. Esto no solo ahorra tiempo y recursos, sino también minimiza las molestias para la comunidad.
Aunque Iglesias lleva adelante el proyecto, el trabajo contó con la colaboración de Daniel Morán, director del Laboratorio de Mecatrónica de la UNSL, que también proporcionó la tecnología de impresión 3D para la creación del robot.
A pesar de los logros iniciales, aún hay desafíos técnicos por resolver. En particular, los especialistas trabajan en encontrar una estrategia para reducir parcialmente el caudal de líquido en las cañerías durante la inspección, ya que el agua turbia puede dificultar la visión. Sin embargo, no disminuye el impacto potencial de esta innovación en la mejora de la infraestructura de saneamiento.
A su vez, el equipo está inmerso en el desarrollo de una versión mejorada: el EC-02. Esta nueva herramienta incorpora ventajas significativas en su diseño y sistema de control. Buscarán aumentar la eficiencia y la capacidad de adaptación a una variedad de condiciones y desafíos en el monitoreo. “El plan para este año es probar este nuevo modelo y sus mejoras en cañerías de entornos reales y realizar relevamientos del estado de las mismas”, sostiene Iglesias.
Premio a la innovación
El Laboratorio de Mecatrónica de la UNSL desempeñó un papel crucial en el desarrollo del robot EC-01 y otros proyectos innovadores. Fundado en 1999, se convirtió en un centro de referencia para la enseñanza, investigación y desarrollo de la mecatrónica en la región. Sus actividades abarcan la docencia de grado y pregrado, la extensión y la investigación.
Uno de sus logros más notables es el robot CXN 2, un robot antropomorfo diseñado para fines didácticos y experimentales, que combina conocimientos de robótica, diseño asistido por computadora, impresión 3D y control electrónico. Además, contribuyó al desarrollo del robot EC-01, que obtuvo varios reconocimientos nacionales y provinciales.
“En 2022 el proyecto ganó dos distinciones. Por un lado, fue seleccionado para la exposición del concurso nacional INNOVAR 2022, que se llevó a cabo en Tecnópolis. Por otro lado, fue ganador de la primera edición del concurso INNOVACCION de la provincia de San Luis, que se llevó a cabo ese mismo año”, recuerda Iglesias.
En este contexto, proyectos como los desarrollados en la UNSL demuestran cómo la ciencia y la tecnología pueden trabajar juntas para abordar desafíos concretos, mejorar la vida de las personas y proporcionar soluciones para problemas cotidianos."""),
    pytest.param('https://www.pagina12.com.ar/810583-cambio-el-mundo', """\
Desde Río de Janeiro
En Brasil gobernamos bien, pero estamos perdiendo la lucha por la opinión pública. ¿Qué nos hace creer que somos un buen gobierno? El hecho de que abordemos el principal problema de Brasil: somos el país más desigual del continente más desigual.
Nuestro gobierno implementa un conjunto de políticas sociales como nunca antes en el país. No sólo políticas sociales, sino también un conjunto de medidas de ayuda a las personas con mayores dificultades. Entre ellas está la disminución del precio de los productos alimenticios.
Ves que la gente compra más cosas, que las tiendas están llenas de gente comprando. Está claro que existe una política que distribuye el ingreso. En Brasil hay casi pleno empleo. La situación más dramática continúa: el número de personas abandonadas, viviendo y durmiendo en las calles. Pero la gran mayoría de la gente no está en esa situación.
Sin embargo, por muy distorsionadas que estén las encuestas, a pesar del optimismo de la gente sobre el futuro de Brasil, la imagen de Lula no refleja eso. El líder político más importante de la historia de Brasil, el mejor presidente que ha tenido el país, no recibe el apoyo correspondiente de la opinión pública.
¿Por qué sucede esto? No se trata sólo de cambiar la persona responsable de la comunicación. El agujero es mucho más profundo.
¿Por qué estamos perdiendo la batalla de la opinión pública? ¿Por qué la gente no traduce la mejora de sus condiciones de vida en apoyo al gobierno, que es responsable de esa mejora?
Es evidente que esta transferencia no se produce. Compararlo con el pasado, con el gobierno de Bolsonaro, no funciona. La gente vive en el presente. Los más jóvenes, entonces, ni siquiera vivieron el gobierno de Bolsonaro.
Los medios de comunicación actúan como el principal sector de oposición al gobierno. Siempre distorsionan las noticias que son favorables al pueblo. Siempre tratando de encontrar o fabricar noticias u observaciones contra la imagen de Lula. Utilizan la encuesta de Folha que atribuye a Lula apenas un 24% de apoyo –real o no– como herramienta para transmitir la idea de que el gobierno, el Partido de los Trabajadores (PT) y Lula ya no son mayoría en el país. Los medios saben que, si no lograron destruir la imagen pública de Lula, la derecha no tiene ninguna posibilidad de volver al gobierno. Así que se dedican principalmente a eso.
La insatisfacción de la gente no parece satisfacerse con empleo e ingresos, que es lo que les proporcionamos. No basta con explicarles cómo el gobierno les proporciona esto.
Hay un sentimiento fuerte contra la política, que termina siendo contra el PT y Lula. Las acusaciones de corrupción calaron en un sector de la población, incluso sin prueba alguna. El encarcelamiento de Lula durante cierto tiempo parece, para este sector de la opinión pública, ser la aparente confirmación de la corrupción que los medios de comunicación intentan imponer sobre la imagen del PT y de Lula.
El PT lleva la peor parte de la ofensiva contra la política y el gobierno, aunque pone en práctica una política distinta en su contenido. No promueve el neoliberalismo. Por el contrario, hay que luchar de frente. Se enfrenta a la mercantilización de las relaciones sociales, incluidos el Estado y la política. La columna vertebral del neoliberalismo aún necesita ser destruida: la hegemonía del capital financiero especulativo en la economía.
Estas cuestiones exigen la formación de un grupo de análisis que produzca mensualmente abordajes sobre Brasil y el mundo, para abastecer a los activistas y a todo el campo democrático y popular."""),
])
async def test_get_body_success(new_initialized_instance: P12Scraper, input_url: str, output_body: str):
    body = await new_initialized_instance.get_body(input_url)
    assert body == output_body


@pytest.mark.parametrize('input_url', [
    pytest.param('https://www.pagina12.com.ar/349353471/'),
    pytest.param('https://www.pagina12.com.ar/349353471/test'),
    pytest.param('https://www.pagina12.com.ar/andytow/'),
    pytest.param('https://www.pagina12.com.ar/andytow/test'),
])
async def test_get_body_failure(new_initialized_instance: P12Scraper, input_url: str):
    with pytest.raises(NonCompliantURL):
        await new_initialized_instance.get_body(input_url)


async def test_get_body_call_failure(new_instance: P12Scraper):
    with pytest.raises(UninitializedWebsiteHandler):
        await new_instance.get_body('https://www.pagina12.com.ar/800250-genealogistas')
