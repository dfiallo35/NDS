# Nations Development Simulation

### Integrantes

Lauren Guerra Hernandez C312
Paula Rodríguez Pérez C311
Dennis Fiallo Muñoz C311

### Ejecución del programa

Para ejecutar el código, primero debe instalar las dependencias de Python que se encuentran en los requirements.txt con `pip install -r requirements.txt`. Luego ejecuta `streamlit run main.py` con el terminal en la dirección de la carpeta src, en caso de estar en otra dirección debes incluir la dirección en el comando `streamlit run <dirección>main.py`, luego la interfaz visual se muestra en el navegador predeterminado.

### Introducción

El objetivo que se persigue con este poryecto es facilitar, mediante el uso de un DSL propio, la generación de simulaciones sobre el desarrollo de algunas Naciones en un tiempo definido y las respuestas de estas naciones a ciertos eventos, para luego recopilar datos sobre los cambios territoriales, el desarrollo, la población y las características de las Naciones y con estos analizar la influencia de las características de una Nación ya sean geográficas, políticas o económicas en el desarrollo que esta sea capaz de alcanzar.


### Modelo de Simulación

Se define la simulación como un sistema que se basa principalmente en eventos, aunque el tiempo, el cuál en la simulación se lleva como días transcurridos, también juega un papel importante en cuanto a en que momento se ejecuta cada evento. Para esto se utiliza una cola de prioridad modificada en la cual se almacenan los eventos, este Heap en lugar de devolver un solo elemento cuando se le hace pop, devuelve todos los eventos que tengan el mínimo valor de prioridad. La prioridad de un evento se define como el tiempo en días en el cual se ejecutará, es decir, el número del día en el cual se ejecutará el evento es la prioridad de este. En cada paso de la ejecución se pide todo el grupo de eventos que tengan la menor prioridad y se mandan a ejecutar todos de forma secuencial. En cada evento se puede definir si se repite o no, en caso de que se repita se agrega de nuevo al Heap con la prioridad correspondiente al tiempo en el cual se ejecutará nuevamente, para obtener este tiempo se obtiene una variable aleatoria a partir de la distribución que se le haya asignado al evento. También se pueden desactivar eventos, en caso de que se desee que no se ejecuten en adelante, esto con poner en `false` la propiedad `enabled` del evento y en caso de que se desee activar un evento basta con poner su valor en `true`.

Toda la simulación se desarrolla en un mismo mapa, en este se definen tanto elementos físicos como son los mares y naciones con todas sus propiedades, como todos los elementos importantes que están relacionados con el proceso de la simulación como son los eventos, decisiones, distribuciones y funciones. Todos estos elementos se pueden crear y modificar desde el DSL.

Las naciones se definen como agentes inteligentes, las cuales reaccionan a los cambios en el medio, como la simulación está dirigida por los eventos que ocurren, cada nación al ocurrir un evento que le afecte responde a este, tratando de contrarrestar sus efectos negativos. Para esto se utilizó la planificación, para con todas las decisiones posibles a tomar por las naciones se realice una selección ordenada de decisiones que le permitan lograr el objetivo que se propone. Estas decisiones están definidas como las acciones usuales que lleva la planificación, tienen una precondición y un efecto, que en este caso es un evento que define el cambio que se le realiza a la nación que tome esa decisión. 

Los eventos en el mapa están separados en dos tipos, los eventos de la simulación y los eventos que forman parte de la ejecución de las decisiones. Los eventos de simulación son los que se ejecutan en cada paso de la simulación, estos eventos son los que modifican el estado del mapa, o de algunas naciones en caso de que sea definido de esta forma específica. Los eventos de las decisiones son los que se ejecutan cuando una nación toma una decisión, tambien son los que se utilizan dentro del algoritmo de planificación como acciones para cambiar de estado.

Las decisiones son las acciones que pueden tomar las naciones para lograr sus objetivos. Una decisión está formada por una precondición que debe cumplirse para que la nación pueda tomar la decisión, y un efecto que es un evento que se ejecuta cuando la nación toma la decisión.

El flujo de la simulación consta de los siguientes pasos:

- Se toman todos los eventos de cola de prioridad que tengan el menor tiempo.
- Cada evento se ejecuta, en caso de que se deba generar se agrega de nuevo a la cola de prioridad con el tiempo en el cual se ejecutará nuevamente.
- Se buscan los cambios ocurridos en el mapa, en específico en cada nación y la que presente cambios negativos se realiza la planificación con el objetivo de llevar esta característica dañada a su valor anterior, los eventos generados por las decisiones se agregan a la cola de prioridad con el tiempo en el cual se ejecutarán, obtenido a partir de una disttribución uniforme.
- se repiten los pasos anteriores hasta que se alcance el tiempo máximo de la simulación.


##### Elementos de la Simulación

El modelo de simulación que se implementó se va a dividir en dos tipos de eventos:

+ **simulation event**: Evento que va a pertenecer a la simulación agregandose a una cola de prioridad según el tiempo en que se debe ejecutar. Este va a estar constituido por:
    + **distribución**: Distribución de la cual se va a tomar la variable aleatoria de las siguiente ejecución del evento.
    + **categoría**: Categoría a la que pertenece este evento, esto se usa para diferenciar los tipod de eventos y sus posibles acciones a tomar. Se usa como apoyo para la heurística de la toma de decisiones.
    + **activado**: Valor buleano que define si al inicio de la simulación el evento va a pertenecer a la cola de ejecución.

+ **decision event**: Evento destinado a ejecutarse como respuesta a ciertos cambios en el mapa. Este cuenta con:
    + **categoría**: Categoría a la que pertenece este evento, esto se usa para diferenciar los tipod de eventos y sus posibles acciones a tomar. Se usa como apoyo para la heurística de la toma de decisiones.

Los elementos principales de la simulación serían:

+ **nation**: Toda la simulación gira en torno a estas. Poseen ciertas características por defecto, pero es posible agregarle todo tipo de datos que sean necesarios para la simulación que se plantea.
    + **población**: Cantidad total de habitante.
    + **extension**: Extensión total de esta.
    + **vecinos**: Lista de naciones vecinas. Solo es necesario agregar como vecino en una de las naciones vecinas.
    + **kwargs**: Es posible agregar cualquier dato que se desee para la simulación.

+ **sea**: Elemento necesario en algunas simulaciones.
    + **extension**: Extensión total de esta.

+ **map**: Elemento que se usa coomo contenedor de todos los elementos de la simulación. Este es único y es generado la promera vez que se corre el código.


Como apoyo a la simulación se tienen los siguientes elementos que se pueden crear:

+ **decision**: Es donde se plantea el momento en que se va a ejecutar un **decision event** en caso de cumplirse la condición de activación. Este contiene:
    + **decision event**: Evento que debe ser ejecutado cuando se cumple la condición.
    + **condición**: Condición para que se tome la decisión.

+ **distribution**: En un principio se cuenta con las 123 distribuciones básicas que brinda el módulo de Python `scipy`. Para generar una nueva distribución es necesario:
    + **distribution**: Una de las distribuciones básicas.
    + **args/kwargs**: Se puede agregar cualquiera de los argumentos que se le pasan a una distribución de `scipy`.

+ **category**: Elementos utilizado para agrupar a los eventos en conjuntos según algunas características en común.



### DSL

Para facilitar la creación de escenarios para la simulación se implementó un Lenguaje de Dominio Específico que además de permitir la creación de forma sencilla de una simulación desde cero, creando cada uno de sus objetos y procesos, tiene la característica de que es Turing-Completo, por lo que cualquier programa es implementable con código del DSL.

##### Arquitectura del compilador y gramática

Para la lexemización, tokenización y parser se utilizaron los tokens definidos en `lexer.py` y la biblioteca de python `SLY`. Esta es una biblioteca para escribir analizadores y compiladores. Se basa libremente en las herramientas tradicionales de construcción de compiladores lex(tokenizar) y yacc (yet another compiler-compiler).

Para la obtención del AST se utilizó el algoritmo de análisis sintáctico (parser) LALR(1) implementado en SLY. Un analizador LALR (Look-Ahead LR)  es una versión simplificada de un analizador LR canónico, para analizar un texto de acuerdo con un conjunto de reglas de producción especificadas por una gramática formal para un lenguaje.

SLY utiliza una técnica de análisis conocida como análisis LR o análisis shift-reduce. El análisis LR es una técnica de abajo hacia arriba que intenta reconocer el lado derecho de varias reglas gramaticales. Cada vez que se encuentra un lado derecho válido en la entrada, se activa el método de acción apropiado y los símbolos gramaticales del lado derecho se reemplazan por el símbolo gramatical del lado izquierdo.

Al igual que con otros tipos de gramáticas LR, un analizador o gramática LALR es bastante eficiente para encontrar el único análisis de abajo hacia arriba correcto en un solo escaneo de izquierda a derecha sobre el flujo de entrada, porque no necesita usar el retroceso. El analizador siempre utiliza una búsqueda anticipada, representando LALR(1) una búsqueda anticipada de un token. Este parser presenta el inconveniente de que, como consecuencia de la técnica shift-reduce, no puede garantizar el análisis correcto en gramáticas ambiguas, siendo LR más poderoso en este aspecto.

El flujo que sigue el compilador es: pasar por el lexer para tokenizar el script con las clase `NDSLexer` que se ecuentra en `lexer.py`, luego pasa a parsear el código con `NDSParser` en `parser.py` el cual nos devuelve el AST del código, el cual se da como una lista de `ParserObj`. Ya con el AST se para a `execution.py` donde primero se hace un chequeo semántico donde en caso de errores lanza excepción para luego pasar a la ejecución de cada fragmento del código que se genera a partir del AST.

Todos los detalles acerca de las reglas de gramática utilizada se puede ver en `parser.out`, además de visualizar cada uno de los estados de la ejecución actual.

##### Diseño del Lenguaje

##### Tipos

- `element`: elementos que se usarán en la simulación, y se encuentran presentes en el mapa: `nation`, `sea`, `decision`, `distribution`, `category`, `simulation event`, `decision event` y `function`.
- `interger`: número entero.
- `decimal`: número flotante.
- `boolean`: booleano, puede ser `true` o `false`.
- `string`: cadena de texto.
- `list`: lista de elementos.
- `time`: tiempo el cual puede ser en años, meses o días(y, m, d respectivamente), se usa para definir los tiempos en la simulación.


##### Sintaxis

- Sintaxsis similar a Python en cuanto a las funcionalidades y dinamismo.
- Instrucciones separadas por `;`.
- Los bloques de código de los loops, condicionales y eventos se encierran en `{}`.
- Para el caso de los argumentos de las funciones o eventos se usa `()`.
- Parámetros y argumentos separados por `,`.
- Mientras que los parámetros se encierran en `<< >>`.
- Admite aritméticas como `+`, `-`, `/`, `//`, `*`, `**`, `%`.
- Uso de operadores `==`, `!=`, `>=`, `>`, `<=`, `<`.
- Uso de operadores lógicos `not`, `and`, `or`, `xor`.
- Para asignar las variables o hacer cambios en los valores de los `elements` se usa `=`.
- Para acceder a los valores de los elementos se usa `->`.
- Se puede asignar el tipo de los argumentos o el nombre de los parámetros usando  `:`.


##### Loops

- `repeat`: ciclo for desde un inicio hasta un final, ambos indicados.
- `foreach`: ciclo for iterando en una lista.
- `while`: ciclo while


##### Condicionales

- Clásicos `if` y `else`.



### Inteligencia Artificial

##### Planificación y A*

El algoritmo de planificación utilizado primeramente se define de forma general para que con este algoritmo se pueda resolver cualquier problema de planificación que herede de `PlanningProblem`,para esto solo debe contar con un estado inicial, una lista de acciones, cada una definida como `Action` o derivada de esta, las que son decisiones en el problema específico, y una función que pasado un estado devuelva si este es la meta a alcanzar o no. Para este problema en específico se definió una clase `PlanningDecisions` que hereda de `PlanningProblem` y que define todo lo necesario y además una función heurística que se explica más adelante.


Para desarrollar la planificación se utilizó un algoritmo de búsqueda con un recorrido BFS que se detiene cuando encuentra la meta especificada o alcanza el máximo número de pasos especificado, en caso de que no se encuentre la meta se devuelve `None`. 

Para mejorar el rendimiento de este algoritmo se utilizó una función heurística que en un estado, para cada acción que se puede tomar se calcula un valor estimado de tomar esta acción, esto a partir de la distancia que está el estado actual del estado meta y se toman en cuenta también las categorías de la acción y del evento al que se está dando respuesta, esto para que se prioricen las acciones que se encuentren más cerca del estado meta y que sean de categorías más similares. Con el costo de la heurística y  el costo de la acción se calcula (en este caso igual a 0) el valor final de la acción, `f(s)=g(s)+h(s)`, por lo que algoritmo de búsqueda + heurística = A*. En este punto también para acciones con un valor superior al estimado se quitan de la posibilidad de ser escogidas, de las acciones que quedan luego de esta poda se colocan en la cola cada una de estas acciones con el estado que generan y además se va construyendo un árbol para cuando se llegue al estado meta sea posible devolver cada estado con la acción que lo genera y tomar en orden todas las acciones a realizar.

##### NLP

Para consultar algunos datos de las naciones que provee `World Bank Data` (población total, esperanza de vida, índice de capital humano, migración, desempleo, inflación) se puede realizar una consulta en lenguaje natural donde se especifiquen cuáles de estas características se quiere determinar, el o los países de interés así como el año del cuál se quiere ver la información. 

El texto con la consulta del usuario será normalizado inicialmente, eliminando `stopwords` y dejando solamente el `lema` de las palabras. Para ello se emplea la biblioteca de python `spacy`. Una vez realizado este proceso se analiza el `part-of-speech tag` de los `token`, así como el tipo de entidad, en este último caso para determinar si se ha especificado algún país (`GPE`) o un año a analizar (`DATE`). 

Para determinar el tipo de información que se pide (población total, esperanza de vida, índice de capital humano, migración, desempleo, inflación) se emplea la clase `Matcher` de `spacy`, donde se buscan coincidencias de `tokens` a partir de un patrón determinado para cada tipo de dato.

Una vez analizado el texto se procede, en dependencia de las coincidencias con el tipo de dato, a obtener la información de `World Bank Data` utilizando la biblioteca de python `world_bank_data` que retrona en `dataframes` de `pandas` la información.



### Ejemplos de código

```
#categories
    category social();
    category economic();
    category political();
    category military();
    category territorial();

    #nations
    nation Cuba(11256372, 109884 , [], [], industrialization: 30, tourism:80);
    nation USA(9147593, 337341954, [], [], industrialization: 80 , tourism:70);
    nation Canada(38246108, 9984670, [], [], industrialization: 70 , tourism:30);
    nation Mexico(128455567, 1964375 , [], [], industrialization: 60 , tourism:70);

    #distributions
    distribution pg(expon, scale: 20);
    distribution block(expon, scale: 50);


    #decisions
    decision event industrialization_increases(economic)<<n>>{
        n->aviable_economic_resources = n->aviable_economic_resources-500;
        n->industrialization = n->industrialization*1.2;
    }    
    decision industrialization_increases_dec(n->aviable_economic_resources >= 5000, industrialization_increases)<< n >>;

    decision event tourism_increases(economic)<<n>>{
        n->aviable_economic_resources = n->aviable_economic_resources-7000;
        n->tourism = n->tourism*1.2;
    }
    decision tourism_increases_dec(n->aviable_economic_resources >= 7000, tourism_increases)<< n >>;


    #events
    simulation event decrease_industrialization(pg,economic,true,[]){
        foreach <<nat>> (map->nations){
            nat->industrialization=nat->industrialization*0.9;
        }
    }

    simulation event population_growth(pg, social, true, []){
        foreach <<nat>> (map->nations){
            nat->population= irvs(expon, loc: nat->population);
        }
    }

    simulation event population_mortality(pg, social, true, []){
        foreach <<nat>> (map->nations){
            nat->population= nat->population - irvs(expon, loc: 0);
        }
    }


    simulate(10d);

    plot(Cuba, ['tourism', 'industrialization'] , 'line');

```