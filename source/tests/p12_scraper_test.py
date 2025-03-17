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


@pytest.mark.parametrize('input_keyword,expected_output', [
    pytest.param('genealogistas', [
        {'article_url': 'https://www.pagina12.com.ar/803462-un-manto-de-caracoles-y-un-colibri',
         'title': 'Un manto de caracoles y un colibrí',
         'date': '13 de febrero de 2025 - 01:14',
         'author': 'María Pia López',
         'image_url': 'https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2025-02/913013-colibri-afp2.jpg',
         'body': """\
“Promete un tiempo / en que la ferocidad no sea la única manera de tocarnos / los unos a los otros y dejarnos una huella. Y quién / no quiere esa promesa.”
Claudia Masin. “Una vez”
Durante la pandemia, usamos la advertencia: estás muteado. Nos pasaba. Nos veían o veíamos a otres haciendo gestos, muecas, mientras no había sonido. Esa desavenencia entre imágenes y palabras no dejaba de resultar cómica y, a la vez, de señalar que siempre hay un problema o un destiempo en la comunicación. Ya distante -varios años han pasado- y sin embargo algo de esa experiencia permanece como puro presente: porque la existencia maquínica se reveló segunda piel o extensión del cuerpo, porque muchas interacciones se siguen dando en la proliferante secuencia de pantallas. Días enteros somos terminales conectadas al whatsApp o a las redes sociales, sosteniendo en la ubicuidad de las ventanitas el agotamiento de nuestra dispersión. Pienso, cuando estoy así, que solo la imagen y el sonido se conjugarán, si me distancio, si escribo un rato, si hago yoga, si me siento a charlar con alguien, si cocino o limpio -las manos alejadas de la pantalla, la mirada reconociendo la espacialidad. Si recupero la presencia, tan acotada siempre, tan escueta, tan efímera: sólo podemos estar en un lugar y en cierto tiempo.
Pero decía, esa experiencia no es personal, y bien lo sabe la oligarquía de las empresas digitales, que construyen poder y acopian capital con la mutación de nuestro ocio en productividad, nuestra libertad en encadenamiento, nuestra imaginación en creación de contenidos. A la vez, lo que circula y se vuelve victorioso en la circulación tecnologizada es lo enfático, maniqueo, gritón, cruento. No es casual que los presidentes de Argentina y de Estados Unidos pretendan encarnar este momento de triunfo del capitalismo digital al tiempo que ponen en escena la brutalidad en los modos discursivos y en las comprensiones del mundo. Como el que nos tocó tiene un costado roto, considera que las fallas de sonido -esas reapariciones del error en el ¡estás muteado!- surgen de una voluntad conspirativa y no del mero trastabillar de unos aparatos técnicos.
La brutalidad en el trato de la lengua no es ajena a la violencia que se ejerce sobre las personas, no se puede separar de la crueldad con la que se suprimen programas de atención médica, con la que se cierran servicios hospitalarios, se despiden trabajadores, se hambrean jubiladas, se minimizan las catástrofes ambientales o se agita, en el mar de fondo de la sociedad, el tembladeral del racismo y el clasismo.
El 1 de febrero muchas ciudades se vieron conmovidas por movilizaciones organizadas para responder a los bruscos ataques gubernamentales contra personas cuya definición de género u orientación sexual son disidentes respecto de la norma. En la ciudad de Buenos Aires se trató de una marcha del orgullo antifascista y antirracista. Pero fue, también, una insurrección poética, de una poesía trazada en los cuerpos, sus danzas, sus modos de encontrarse, en los carteles, en las banderas. La poesía habitó las calles como gesto con el cual confrontar el achatamiento de una lengua que se vuelve altisonante para amenazar.
Algo muy potente surge de ese gesto. Imaginé la multitud como un colibrí que insiste en ese vuelo flotador alrededor de unas flores, imaginé ese flotar como una insistencia en el sentido, en la procura de una precisión, un matiz, una palabra. Multitud colibrí. Que resignificó el orgullo LGTBIQNB+, confrontó con el racismo -¿no implica el racismo el modo más achatado de la lengua, allí donde un rasgo se vuelve el todo y en nombre de ese rasgo absolutizado se justifican dominios y agresiones?- y propuso una interpretación política: el rasgo del presente es el fascismo.
No faltaron luego una serie de interpretaciones, y más allá de la denostación, hubo quienes con gesto paternalista dijeron qué bonita marcha pero las cosas se juegan de verdad en las elecciones o quienes se pusieron a sancionar como atrasadas las consignas. Atrasan cien años, dijeron, como antes se dijo: se pasaron tres pueblos. Nuestra insurrección poética también podría ser una insumisión ante el modo lineal de pensar la temporalidad, donde todo se reduce a atraso/novedad, como si el progreso siguiera siendo un fantasma organizador, cuando bien sabemos que la historia lejos está de ser aprehendida -y hecha- con ese simplismo de juego de la oca -avanzar o retroceder. Cuando sabemos, digo, que los hechos portan un sentido que no es el de la expresión de una fecha o una pertenencia a una época. Ni atrasamos ni nos pasamos, más bien se está poniendo en juego una experimentación fenomenal sobre las vidas y su politización, que no se priva de sus enlaces anacrónicos ni de su imaginación intempestiva. Me dirán: ¡son metáforas! Claro, pero no son de las que alimentan el vuelo ni sostienen la flotación, más bien parecen piedras capaces de derribar al colibrí.
En los días previos al 1 de febrero circuló un llamado a movilizar. Un flyer decía: existen sólo dos géneros: fascistas y antifascistas. Decía mucho: no se trataba sólo de movilizarse desde las identidades sexo-genéricas, sino a partir de una composición política, de la decisión de situarse frente y contra las políticas del gobierno. ¿Por qué llamarle fascistas a esas políticas? Intuyo que fue para nombrar la ferocidad con la que están apostando a construir un nuevo orden autoritario, en el que la preservación de la vida se somete a la lógica de la mercancía, y en el que se reponen jerarquías de clase, raza, género. Es decir, fascismo como horizonte, como intento de clausurar las experiencias de transformación política. A eso nombran batalla cultural y encuentra en la apología de la crueldad su rasgo dominante. Frente a eso, antifascismo es la apelación y reunión de disímiles y conjugables experiencias: de esos esfuerzos por construir lazo social, de las poesías de las luchas, del orgullo de las vidas deseantes, de las tenacidades militantes, de las vocaciones genealogistas que quieren construir otras historias, de los cansancios ante los agravios, del trabajo mal pago y de la falta de trabajo. Antifascismo es la exploración de una temporalidad, por fuera de su sentido lineal. Busca su poesía del porvenir, no de la certidumbre de una historia que ya aconteció ni se ampara en un concepto certificado en alguna academia.
A veces, cuando se retira la marea, deja partes de la arena como un manto bordado de caracoles. De pedacitos de caracoles. Brillan ahí, como si fueran piedras preciosas. Son los restos rotitos y magníficos. No hay manto más bello que ése que el mar deja a su paso. Y que cada día será distinto. Quizás esta época, en la que los victoriosos hacen gala del gesto fascista de tratar a muchas vidas como desechos, nos exija esa otra política, la de construir con nuestros restos ese manto, con nuestros pedacitos esa incrustación en la arena, con nuestros sueños ese mar que llega y se retira, siempre -decía un poeta- joven."""},
        {'article_url': 'https://www.pagina12.com.ar/803490-de-genealogistas-y-analizantes-ii',
         'title': 'De genealogistas y analizantes II',
         'date': '13 de febrero de 2025 - 00:38',
         'author': 'Alejandro Benedetto*',
         'image_url': 'https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2025-02/913074-ro08fo0113web.jpg',
         'body': """\
“Los hombres hacen su propia historia, pero no la hacen a su libre arbitrio, bajo circunstancias elegidas por ellos mismos, sino bajo aquellas circunstancias con que se encuentran directamente, que existen y les han sido legadas por el pasado. La tradición de todas las generaciones muertas oprime como una pesadilla el cerebro de los vivos. Y cuando éstos aparentan dedicarse precisamente a transformarse y a transformar las cosas, a crear algo nunca visto, en estas épocas de crisis revolucionaria es precisamente cuando conjuran temerosos en su auxilio los espíritus del pasado, toman prestados sus nombres, sus consignas de guerra, su ropaje, para, con este disfraz de vejez venerable y este lenguaje prestado, representar la nueva escena de la historia universal” Karl Marx.
En 1873, en la segunda de las intervenciones intempestivas titulada Sobre la utilidad y el perjuicio de la historia para la vida, Friedrich Nietzsche describe tres modos en los que los seres humanos modernos se relacionan con la historia, a los que agregará una cuarta forma sugerida por él.  
También advierte sobre las terribles consecuencias que conlleva que una de estas maneras se imponga por sobre las demás, ya que, como veremos, todas estas formas de imitar, conservar y criticar son fundamentales para la vida de un pueblo o de un sujeto. 
La primera. Historia Monumental. Puede pertenecer tanto a los seres de acción como a los inactivos. Su principal lema es: "Dejad a los muertos que entierren a los vivos".
Este tipo de historia pertenece a quienes veneran los monumentos, los hechos gloriosos, la pulcritud y claridad de los efectos en sí, la verdad icónica y luminosa del gran acontecimiento. 
Puede servir como modelo, como recordatorio de que, si se pudo crear algo grande y magnifico en el pasado, puede volver a crearse nuevamente en el presente. 
El peligro está cuando el monumento queda desgajado de las causas que lo provocaron y de él se sirven seres viles y resentidos para repudiar todo presente. Así los grandes acontecimientos se transforman en una especie de mito, de poetización. 
De esta manera podemos ver como el desmedido amor a los grandes monumentos del pasado, su devoción y respeto, por los grandes hombres de la historia no parte de intenciones nobles. 
Por el contrario, oculta un inmenso odio a todo lo grande, fuerte, creador y vivo de su tiempo. Por eso hacen público su amor por los de antaño. 
Estos personajes, con su disfraz de expertos, logran suprimir el arte creador sentenciando; "Todo lo que no es monumental no es necesario: Mirad, lo que es grande ya está ahí". No quieren la grandeza, porque no la pueden, de allí que intentan enterrarla. Son como médicos que solo suministran venenos.
La segunda. Historia Anticuario. Pertenece a quienes preservan y veneran. Su lema dice así: "Aquí se pudo vivir, por lo tanto, se puede vivir y aquí se podrá vivir; somos tenaces ya que no nos derrumbaran de un día a otro”.
Desde lejos se ve la piedad, el amor y el eterno agradecimiento que aflora en este tipo de individuos cuando miran hacia atrás. Respetan como nadie el pasado, la tradición y el linaje, pero terminan momificando la vida. 
El alma queda poseída en los objetos, incrustada a ellos, como al pasado mismo. Cada cosa por mínima o decrepita que sea conserva su fuerza, su valor. Preservar es la tarea suprema. Guardar para futuras generaciones esas cosas que para ellos resultaron buenas. 
El alma anticuario hace de los objetos conservados un nido familiar. La historia de su pueblo se confunde con su historia. El hombre anticuario posee la furia del coleccionista, que acumula incansablemente cosas por el solo hecho de que han existido alguna vez. El alma anticuaria queda envuelta en el olor de lo rancio.
La tercera. Historia Crítica perteneciente a la juventud, cuyo lema señala que: "Ser injusto y vivir son una y la misma cosa" 
Se necesita de vez en cuando, para poder vivir, destruir lo establecido, rasgar la continuidad de lo dado. Abrir un agujero en la constante permanencia de lo idéntico. Es por esto que el crítico rompe sin importar a quién, ni qué. De allí su injusticia. Mas el que juzga aquí no es él, sino la vida. Es ella la que no respeta nobleza ni bajeza, honores ni diplomas. 
¿Por qué ella es injusta? No porque otorga o destruye sin medidas, sino porque no pudiendo dar a cada uno lo suyo, da a cada uno lo de ella. ¿Qué es lo de ella? Una potencia obscura, insaciablemente ávida de sí misma. 
Es difícil, dice Nietzsche, no darse cuenta hasta qué punto vivir y ser injusto es una y la misma cosa. La Historia Crítica niega el pasado, lo destruye de raíz y, por ello mismo, corre el riesgo de imposibilitarlo todo.
***
“La Humanidad nunca vive por completo en el presente, en las ideologías del superyo perviven el pasado, la tradición de la raza y el pueblo…desempeñando un papel poderoso en la vida humana, independientes de las relaciones puramente económicas” (Sigmund Freud)
Ahora bien, la Genealogía es entendida por Nietzsche como un nuevo modo de vincularse con la historia, una actitud, disposición, una tarea: Historia Efectiva es el nombre de ese otro hacer. 
Este tipo de historia invierte la relación de lo próximo y lo lejano. Atañe, no a las cimas alejadas de los grandes monumentos, las alturas icónicas de los hombres sublimes, la tradición noble y remota de un pueblo, sino a la sangre, el deseo, al amor, el suelo, el clima, la alimentación. 
Está más próxima a la medicina que a la filosofía, circunda los cuerpos, las enfermedades, la salud, el sexo, los olores, la decrepitud, las diferentes formas de la muerte, las miserias cotidianas, los amores, el odio en todas sus modalidades. 
Su principio anti-metodológico dice: “más cerca del arte que de la ciencia o, en su defecto, ciencia, pero jovial”. 
Su posición política se define así: "Contra el demagogo que niega el cuerpo porque sostiene el ideal y contra el historiador que se niega a sí mismo para sostener la historia. Porque ellos imitan la muerte para entrar en el reino de los muertos".  
Señala tres posibles usos de la historia efectiva, aquí seguimos los precisos señalamientos de Michel Foucault en Nietzsche. La genealogía. 
La historia monumental, la veneración de los monumentos, deviene parodia. Hay que hacer un uso paródico de la historia: oponiéndose a la historia reminiscencia o reconocimiento, parodiar los monumentos para trastocar la realidad establecida. 
La historia Anticuario, aquella que preserva y conserva el pasado, deviene disociación sistemática. Oponiéndose a la historia como simple continuidad, disocia y destruye identidades perpetuadas. 
Por último, la historia Crítica, diatriba contra las injusticias del pasado por la verdad que el hombre detenta hoy, deviene destrucción del sujeto de conocimiento. Oponiéndose a la historia conocimiento sacrifica y destruye la verdad, más aún, al sujeto de conocimiento mismo. 
Porque si el saber no sirve para hacer tajos en los sedimentos sofocantes de la evocación melancólica, en las letras encarnadas en el cuerpo sufriente, en el silencio mortífero de todo lo que quiso alguna vez, y sigue queriendo, morir, no sirve para nada.
*Psicoanalista. Docente. Escritor."""},
        {'article_url': 'https://www.pagina12.com.ar/800250-genealogistas',
         'title': 'De genealogistas y analizantes',
         'date': '30 de enero de 2025 - 00:34',
         'author': 'Alejandro Benedetto',
         'image_url': 'https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2025-01/907602-ro08fo0130web_0.jpg',
         'body': """\
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
Todo lo contrario, nos recuerda que el culto al pasado interrumpe la memoria, la congela, y nos hace olvidar, frecuentemente, lo que está vivo en todo presente."""},
        {'article_url': 'https://www.pagina12.com.ar/298391-la-fiesta-del-monstruo',
         'title': 'La fiesta del monstruo',
         'date': '11 de octubre de 2020 - 04:33',
         'author': 'Liliana Bellone*',
         'image_url': 'https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2020-10/110281-polish-20201011-042650240.jpg',
         'body': """\
Uno de los más famosos cuentos de Borges sobre el peronismo se llama “La fiesta del monstruo” en Nuevos cuentos de Bustos Domecq (1977). Este texto, escrito en colaboración con Bioy Casares en 1947 (o sea un año después de la asunción de Perón a la presidencia) y publicado en 1955, año de la llamada “Libertadora”, en el semanario “Marcha” de Montevideo, muestra la jornada del 17 de octubre como el accionar de “la chusma”, gente proveniente del sur, del llamado “gran Buenos Aires”, que “invade” la civilizada ciudad, haciendo gala de grosería y barbarie. Siguiendo el esquema de El matadero de Echeverría, que presenta la dicotomía irresoluble civilización-barbarie, el populacho asesina a un joven judío que se niega a saludar la figura del “Monstruo” (Perón, quien hablaría en Plaza de Mayo). Desde el registro del lenguaje popular, Borges y Bioy pintan un abigarrado cuadro que corresponde a la triste caracterización clasista y oligárquica de “aluvión zoológico” pergeñada por el legislador Sanmartino, vocero de la burguesía.
En 1955, Borges firma un artículo donde habla no sólo de dictadura, sino de humillación, ultrajes y tortura, es “L `illusion comique”, publicado en la celebérrima revista Sur de Victoria Ocampo, en noviembre de 1955, o sea pocos meses después del golpe de estado militar.
Son muchas las anécdotas y expresiones del escritor contra el peronismo en entrevistas y conferencias, pero en los textos, ese entramado tan consistente porque allí se juegan todas las partidas, aparece pintada su ceguera política, que no hace otra cosa que ser “patéticamente fiel a su clase”, como afirma el ensayista y poeta cubano, Roberto Fernández Retamar en Calibán (1971) y luego en Fervor de la Argentina (1993).
Así, en El hacedor (1960), dos cuentos ejemplifican esta posición, “El simulacro” y “Martín Fierro”. En el primero, un hombre monta un espectáculo teatral que escenifica un funeral, entre grotesco y circense en un “pueblito del Chaco” durante los días de julio de 1952, fecha que remite inmediatamente a la muerte de Evita, a quien se representa en la dramatización con una muñeca rubia. El actor (o simulador) dice ser Perón y la gente se acerca a saludarlo, mientras deposita en una alcancía una cuota de dos pesos, en un acto de borramiento de límites, como si el teatro invadiera la realidad o viceversa (a la manera de la escena de los cómicos en Hamlet, dice el narrador). La conclusión es la triste constatación de que también Perón y Evita eran simulacros, y que nadie los conocía, nadie sabía en realidad quiénes eran. En este cuento hay sin dudas reminiscencias de la concepción dramática del barroco que muestra la contaminación teatro-realidad (Shakespeare, Calderón de la Barca).
En “Martín Fierro” en el libro mencionado, el narrador evoca dos tiranías en el país, la primera, la de Rosas, con degollados y proscriptos y la segunda, la de Perón, con "cárcel y muerte”. Este cuento entronca con “El otro”, en El libro de arena (1975), donde el Borges maduro, ciego y escéptico conversa con el “otro”, él mismo, joven, idealista, lector de Dostoievski, ingenuo casi, y le comenta como un visionario que “Buenos Aires, hacia mil novecientos cuarenta y seis, engendró otro Rosas, bastante parecido a nuestro pariente”. En esta alusión irónica a Perón y al parentesco con Rosas, puede leerse que hay un territorio compartido, más allá de lo concreto: el territorio de los fantasmas. Si Perón es parecido a Rosas, y Rosas es pariente de Borges, puede inferirse que no está lejos el “parentesco” Borges-Perón, en ese universo de sueño donde transcurre la materia del relato.
Perón era militar de carrera, egresado del Colegio Militar de la Nación, en donde solamente ingresaban los hijos de las familias acomodadas del país y sus abuelos paternos pertenecían a la elite porteña ya que el abuelo Tomás Liberato Perón había sido profesor en la Facultad de Medicina de la Universidad Nacional de Buenos Aires y había combatido en la guerra contra el Paraguay, o sea que, como el abuelo Francisco Borges y el bisabuelo Isidoro Suárez, era un héroe de la Patria.
Hay algunos genealogistas que encontraron relaciones entre las familias de Borges y de Perón, lo que es muy atendible, pues las viejas familias criollas estaban bastante emparentadas. Por otro lado, los antepasados de Borges y Perón provenían del mismo círculo de la alta burguesía argentina, de raíces europeas. 
Tomás Liberato Perón, héroe de la guerra del Paraguay, era hijo de un inmigrante de Cerdeña, dedicado a fabricar botas para la policía de Rosas, la famosa y temida “Mazorca” y se había casado con una escocesa, Ann Hughes Mac Kenzie. Los antepasados de Borges provienen de Portugal y la abuela materna era inglesa, Frances Ann-Fanny- Haslam de Borges, tan bien retratada por su nieto en “Historia del guerrero y la cautiva”, en El Aleph (1949). Los Perón pertenecían a la elite porteña y Mario Tomás Perón, el padre de Juan Domingo, nacido y criado en la culta Buenos Aires, inició la rebeldía cuando se casó con Juana Sosa, de ascendencia mapuche y empleada doméstica de unos hacendados ingleses amigos.
En Siete noches (1980), el escritor narra su experiencia al leer La Divina Comedia, lo que él llama “modus operandi” que consistía en leer primero un terceto en inglés y luego en italiano. Realizaba la lectura mientras viajaba en tranvía, desde su casa en Las Heras y Pueyrredón, en el norte de la ciudad de Buenos Aires, hacia Almagro Sur, ya que trabajaba en la Biblioteca de ese barrio. Esa lectura-revelación se realiza en un momento histórico determinado que el escritor sitúa “antes de la dictadura”, indicando casi sin margen de error al primer gobierno peronista, momento en que perderá su puesto pues renunciará por haber sido designado como inspector de aves y conejos.
Anudamiento entre el uno y el otro: “La fiesta del monstruo”, Juan Perón, civilización y barbarie, reflejos de un engañoso espejo. Tal vez esta cuestión explica los límites de la tesis largamente sostenida por la ideología colonialista, al tratar de arrojar luz sobre relaciones históricas, económicas y sociales, dentro de un supuesto marco teórico, que se sostiene solamente por lo que Lacan llama imaginario, sin arribar a lo simbólico. La relación imaginaria conlleva la desconfianza hacia el otro, la falta del crédito, el odio y, paradójicamente, el amor, lo que será siempre engañoso, un “espejismo”.
El horror a lo popular en "Ragnarök"
Este cuento de El hacedor (1960), escrito en primera persona, narra, como en muchos otros casos, un sueño. El ámbito ambiguo y casi irreal es la Facultad de la Filosofía y Letras de la Universidad Nacional de Buenos Aires, en cuyas aulas Borges dio clases durante años luego de 1955 y alude al gran Pedro Henríquez Ureña, amigo y colega suyo, como evidentes rasgos autobiográficos. En el mundo confuso del sueño, descienden “los dioses”, una “turba” que emite chillidos y silbidos, que más parecen cacareos de aves que voces. Como en el cuento “Juan Muraña” (El informe de Brodie, 1970), donde el personaje Trápani cuenta que en sueños vio que su tío Juan le mostraba una garra de buitre, mientras la sacaba de abajo del saco, a la altura del corazón, como si fuese un arma, el narrador ve que uno de ellos también tiene una garra en lugar de mano. Sueños de los personajes de Borges que reiteran sus propios sueños. La imagen del hombre relacionada con aves depredadoras, se repite en la literatura argentina culta y popular, Los caranchos de La Florida de Benito Lynch o el “gavión” o “gavilán” de las letras de tango. Por otro lado, “Ragnarök” remite a la batalla final de los tiempos en la mitología nórdica, una lucha apocalíptica donde gigantes y dioses serán vencidos de acuerdo con una fatalidad abrumadora. Estas divinidades primitivas y temibles, titánicas, ocupan el centro del sueño borgeano, restos diurnos de sus lecturas y gustos literarios, pero de acuerdo con la condensación y el desplazamiento que son los mecanismos del sueño, según Freud, las imágenes de las ferales criaturas escandinavas entroncan con la fisonomía de los guapos de los arrabales porteños. Entonces, como en “La fiesta del monstruo”, surge el terror ante la “chusma”, ante los distintos que provienen de los lugares marginales y exigen un lugar en el Otro, los pobres y desheredados que reclaman su derecho y causan espanto en las clases acomodadas. El narrador los describe feos, atroces, bestiales, como en “La fiesta del monstruo”.
Las garras de buitre conllevan la referencia a Marechal y a su “gavilán” en Don Juan o a Los caranchos de la Florida de Benito Lynch. “Los dioses” primitivos que han resurgido no saben hablar, han olvidado las palabras, provienen de la barbarie, pues las grandes religiones-la cultura- los han expulsado. Son un peligro. En el devenir onírico y que coincide con el devenir narrativo, el narrador describe la indumentaria de “los dioses”, que coincide con la vestimenta de los compadritos con sus trajes chillones y ajustados, atuendos del lupanar y del garito.
Los dioses antiguos se metamorfosean en esos orilleros desafiantes con rostros fieros, mestizos y achinados que portan armas en las sisas de sus chaquetas y sacos. Entonces, en el sueño, surge la defensa, la contrapartida ante el terror al “otro” y el cuento finaliza con la violencia reprimida y desplazada:n”Sacamos los pesados revólveres (de pronto hubo revólveres en el sueño) y alegremente dimos muerte a los Dioses”.
Las interpretaciones pueden ser las que permiten un sueño o una pieza literaria, podría hablarse del horror al “otro”, de un deseo reprimido de castigo al distinto, al “otro” descalificado y disminuido, demonizado, para justificar su desaparición, etc. Lo cierto es que lo importante son los desplazamientos y sustituciones que han ocurrido en el relato, lo que muestra el complejo laborar del inconsciente. No pocas veces, Borges trabaja con el material que le proporcionan sus propios sueños, pues equipara sueño con literatura, entonces sueña con Alonso Quijano, con un rey feroz y antiguo, con Rosas, con Sarmiento, con Quevedo, con Roma y Cartago, con Pitágoras, con Conrad y con Emerson. De este modo recupera lo que el realismo y el naturalismo habían perdido y que los románticos y los hijos del romanticismo como Poe habían descubierto, esto es, la concepción de la literatura como depositaria y subsidiaria del territorio de las fantasías.
El sentimiento negativo hacia lo popular que aparece en “La fiesta del monstruo” y en “Ragnarök”, contrasta sin duda con los textos borgeanos de su juventud, cuando elogia al payador, al habla criolla, al poeta del suburbio, Evaristo Carriego, al arrabal y al coraje y al honor de los guapos de Palermo o del Sur.
En 1976, Borges declara en el “Prólogo” a la Moneda de hierro: “Sé que este libro misceláneo que el azar fue dejándome a lo largo de 1976, en el yermo universitario de East Lanssing y en mi recobrado país, no valdrá mucho más ni mucho menos que los anteriores volúmenes”. Y más adelante agrega: “pero tal vez me sea perdonado añadir que descreo de la democracia, ese curioso abuso de la estadística.” Este prólogo está fechado en Buenos Aires, el 27 de julio de 1976, a escasos dos meses del golpe de estado. El escritor espera ser perdonado por no confiar en la democracia…
(*) Premio Casa de las Américas de Cuba de Novela, 1993"""},
        {'article_url': 'https://www.pagina12.com.ar/115740-la-telenovela-de-la-boda-real-britanica',
         'title': 'La telenovela de la boda real británica',
         'date': '19 de mayo de 2018 - 10:35',
         'author': 'Marta Núñez',
         'image_url': 'https://images.pagina12.com.ar/styles/focal_3_2_470x313/public/2018-05/na19fo01_12.jpg',
         'body': """\
PáginaI12 En Gran Bretaña
Desde Londres
What a circus, what a show. Con esta letra del musical “Evita” los británicos se mofaron de los procesos políticos y sociales tercermundistas: Argentina y el peronismo eran el ejemplo. 
Como un boomerang, ahora la misma lírica se le puede aplicar a la boda del príncipe Harry, “l’enfant terrible” de la monarquia, con la actriz estadounidense Meghan Markle, que tiene embelesada a la sociedad británica en vísperas del gran evento este sábado 19 de mayo.
Mientras la estricta etiqueta monárquica trata de regular esta unión que acentúa la tendencia de casamientos reales con “commoners” (meros mortales sin sangre azul), en paralelo se desarrolla la saga de una familia común, la de Meghan (padres divorciados, medios hermanos celosos, un padre que a ultima hora no puede asistir y consecuentes dudas sobre quién llevará a la novia al altar), que debe estar desesperando a los encargados del protocolo.
Desde ya, el príncipe Harry ha dado más de un disgusto a la Reina. Recordemos el episodio de su desnudo en Las Vegas, su paso en falso al ir disfrazado de nazi a una fiesta de disfraces, y sin ir más lejos sus desmadres en la localidad de Lobos, provincia de Buenos Aires, en 2004, que informara en exclusiva Raúl Kollmann para PáginaI12, hecho que casi provoca un conflicto diplomático (un incontrolable Harry de 20 años que se escapaba de la custodia de Scotland Yard y se emborrachaba hasta perder el sentido en los boliches bonaerenses obligó a que la policía provincial pidiera la intercesión de la Cancillería y que la embajada británica se hiciera cargo de él).
Ahora, al casarse con Meghan agrega una de cal y otra de arena. Meghan añade a su prosapia de commoner un toque multicultural, ya que es norteamericana afrodescendiente, algo que “democratiza” a la monarquía en estos tiempos de las sociedades del espectáculo. Pero hizo fruncir más de un ceño entre los más acerbos devotos de una monarquía que creen que debería mantenerse ajena a los cambios sociales.
La Inglaterra profunda ama todo lo que sea tradiciones. Compromisos, bodas, bautismos y funerales son tratados como eventos ritualizados por costumbres muy enraizadas en el imaginario colectivo (recuerden aquella divertidísima película, Cuatro bodas y un funeral). Y salvo para una minoría republicana, la vida de la familia real es un tema entrañable para los súbditos de este reino.
Aunque Meghan ha hablado abiertamente de descender de esclavos, hay bienintencionados genealogistas que dicen haber descubierto que su duodécima abuela era prima segunda de Jane Seymour, una de las esposas de Enrique VIII. Sus no tan bienintencionados medios hermanos la están despellejando viva. Sam, su hermana, la llama “trepadora” y Thomas se atrevió a escribirle a Henry una carta abierta pidiéndole que desistiera del terrible error de casarse con su hermana.
Todo suma al “what a circus, what a show”.
Windsor, la localidad donde tiene lugar la boda, está engalanada con banderas y fotos de la pareja real, y se espera que acudan 100.000 personas a este pequeño pueblo de 32 mil habitantes. De hecho, ya muchos han acampado con sus bolsas de dormir en los lugares que les ofrecerán una mejor visión del paso de la carroza real. Y Londres no se queda atrás en cuanto al clima de fiesta que se respira en las calles, ayudado por unos días misericordiosamente primaverales y soleados.
La pareja es tapa de cientos de revistas y de periódicos, y se aprovecha el evento para recordarnos reglas de protocolo (¡como si todos fuéramos invitados!), y se hacen apuestas sobre el secreto bien guardado de la casa diseñadora del vestido de la novia. El negocio de la boda no se queda atrás y hay “merchandise” en venta para todos los gustos y bolsillos.
La llorosa Meghan que aparecía ayer en las tapas de algunos periódicos angustiada por la ausencia de su padre y el no saber quién la acompañaría al altar ya puede sonreír otra vez: el príncipe Carlos acaba de salir a su rescate, encantado de hacerse cargo de ese papel."""},
    ]),
])
async def test_search_success(new_initialized_instance: P12Scraper, input_keyword: str,
                              expected_output: list[dict[str, str]]):
    results = await new_initialized_instance.search(input_keyword)

    def sort_by_title(results_list):
        return sorted(results_list, key=lambda article: article['title'])

    assert sort_by_title(results) == sort_by_title(expected_output)


async def test_search_call_failure(new_instance: P12Scraper):
    with pytest.raises(UninitializedWebsiteHandler):
        await new_instance.search('genealogistas')
