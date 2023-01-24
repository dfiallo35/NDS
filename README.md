<h1> Evolución de Naciones</h1>

Se quiere simular el desarrollo de ciertas Naciones en un tiempo definido y en una zona geográfica generada. Estas Naciones van a contener ciertas Provincias de las que se proporciona su desarrollo y su población, mientras que de las naciones se proporcionarán los rasgos distintivos de estas. Además, pueden existir zonas neutrales o mares, los cuales representan áreas vacías. Se tomará como base principal para la simulación a los Eventos (a los cuales se les atribuye una distribución específica y un período de tiempo), todo suceso en la simulación será un Evento; estos pueden provocar una toma de decisiones por parte de una Nación, las cuales varían con respecto al evento al que se enfrentan y las características que posee esta Nación.
Se podrán recopilar datos sobre los cambios territoriales, el desarrollo, la población y las características de las Naciones y con estos analizar la influencia de las características de una Nación ya sean geográficas, políticas o económicas en el desarrollo que esta sea capaz de alcanzar.



<h2> DSL </h2>

Para facilitar la creación de escenarios para la simulación se implementó un Lenguaje de Dominio Específico que además de permitir la creación de forma sencilla de una simulación desde cero, creando cada uno de sus objetos y procesos, tiene la característica de que es Turing-Completo, por lo que cualquier programa es implementable con código del DSL.

<h4> Arquitectura del compilador y gramática</h4>

Para la lexemización, tokenización y parser se utilizaron los tokens definidos en `lexer.py` y la biblioteca de python `SLY`. Esta es una biblioteca para escribir analizadores y compiladores. Se basa libremente en las herramientas tradicionales de construcción de compiladores lex(tokenizar) y yacc (yet another compiler-compiler).

Para la obtención del AST se utilizó el algoritmo de análisis sintáctico (parser) LALR(1) implementado en SLY. Un analizador LALR (Look-Ahead LR)  es una versión simplificada de un analizador LR canónico, para analizar un texto de acuerdo con un conjunto de reglas de producción especificadas por una gramática formal para un lenguaje.

SLY utiliza una técnica de análisis conocida como análisis LR o análisis shift-reduce. El análisis LR es una técnica de abajo hacia arriba que intenta reconocer el lado derecho de varias reglas gramaticales. Cada vez que se encuentra un lado derecho válido en la entrada, se activa el método de acción apropiado y los símbolos gramaticales del lado derecho se reemplazan por el símbolo gramatical del lado izquierdo.

Al igual que con otros tipos de gramáticas LR, un analizador o gramática LALR es bastante eficiente para encontrar el único análisis de abajo hacia arriba correcto en un solo escaneo de izquierda a derecha sobre el flujo de entrada, porque no necesita usar el retroceso. El analizador siempre utiliza una búsqueda anticipada, representando LALR(1) una búsqueda anticipada de un token. Este parser presenta el inconveniente de que, como consecuencia de la técnica shift-reduce, no puede garantizar el análisis correcto en gramáticas ambiguas, siendo LR más poderoso en este aspecto.

El flujo que sigue el compilador es: pasar por el lexer para tokenizar el script con las clase `NDSLexer` que se ecuentra en `lexer.py`, luego pasa a parsear el código con `NDSParser` en `parser.py` el cual nos devuelve el AST del código, el cual se da como una lista de `ParserObj`. Ya con el AST se para a `execution.py` donde primero se hace un chequeo semántico donde en caso de errores lanza excepción para luego pasar a la ejecución de cada fragmento del código que se genera a partir del AST.

Todos los detalles acerca de las reglas de gramática utilizada se puede ver en `parser.out`, además de visualizar cada uno de los estados de la ejecución actual.

<h4> Diseño del Lenguaje</h4>

<h5> Tipos </h5>

- `element`: elementos que se usarán en la simulación, y se encuentran presentes en el mapa: `nation`, `province`, `sea`, `neutral`, `trait`, `decision`, `distribution`, `category`, `event`.
- `interger`: número entero.
- `decimal`: número flotante.
- `boolean`: booleano, puede ser `true` o `false`.
- `string`: cadena de texto.
- `list`: lista de elementos.
- `time`: tiempo el cual puede ser en años, meses o días(y, m, d respectivamente), se usa para definir los tiempos en la simulación.


<h5> Sintaxis </h5>

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


<h5> Loops </h5>

- `repeat`: ciclo for desde un inicio hasta un final, ambos indicados.
- `foreach`: ciclo for iterando en una lista.
- `while`: ciclo while


<h5> Condicionales </h5>

- Clásicos `if` y `else`.



<h4> Ejemplos de código</h4>

```
category social();
category economic();

nation Cuba(10, 100, [], [], industrialization: 10 , economic_resources:30000);
nation USA(10, 100, [], [], industrialization: 10 , economic_resources:30000);

distribution pg(expon, scale: 100);

decision event industrialization_increases(economic)<<n>>{
    n->economic_resources = n->economic_resources-5000;
    n->industrialization = n->industrialization*0.9;
}

decision industrialization_increases_dec(n->economic_resources >= 5000, industrialization_increases)<< n >>;


simulation event population_growth(pg, social, true, []){
    foreach <<nat>> (map->nations){
        nat->population= irvs(expon, loc: nat->population);
    }
}

simulation event decrease_industrialization(pg,economic,true,[]){
    foreach <<nat>> (map->nations){
        nat->industrialization=nat->industrialization*0.9;
    }
}

simulation event population_mortality(pg, social, true, []){
    foreach <<nat>> (map->nations){
        nat->population= nat->population - irvs(expon, loc: 0);
    }
}

simulate(100d);

```

<h3> Ejecución del programa</h3>

Para ejecutar el código, primero debe instalar las dependencias de Python que se encuentran en los requirements.txt con `pip install -r requirements.txt`. Luego ejecuta `streamlit run main.py` con el terminal en la dirección de la carpeta src, en caso de estar en otra dirección debes incluir la dirección en el comando `streamlit run <dirección>main.py`, luego la interfaz visual se muestra en el navegador predeterminado.

<h2> Simulación</h2>
Se define la simulación como un sistema que se basa principalmente en eventos, aunque el tiempo, el cuál en la simulación se lleva como días transcurridos, también juega un papel importante en cuanto a en que momento se ejecuta cada evento. Para esto se utiliza una cola de prioridad modificada en la cual se almacenan los eventos, este Heap en lugar de devolver un solo elemento cuando se le hace pop, devuelve todos los eventos que tengan el mínimo valor de prioridad. La prioridad de un evento se define como el tiempo en días en el cual se ejecutará, es decir, el número del día en el cual se ejecutará el evento es la prioridad de este. En cada paso de la ejecución se pide todo el grupo de eventos que tengan la menor prioridad y se mandan a ejecutar todos de forma secuencial

Toda la simulación se desarrolla en un mismo mapa, en este se definen tanto elementos físicos como son las naciones con todas sus propiedades, como todos los elementos importantes que están relacionados con el proceso de la simulación como son los eventos, decisiones, distribuciones y funciones. Todos estos elementos se pueden crear y modificar desde el DSL.

Las naciones se definen como agentes inteligentes, las cuales reaccionan a los cambios en el medio, como la simulación está dirigida por los eventos que ocurren, cada nación al ocurrir un evento que le afecte responde a este, tratando de contrarrestar sus efectos negativos. Para esto se utilizó la planificación, para con todas las decisiones posibles a tomar por las naciones se realice una selección ordenada de decisiones que le permitan lograr el objetivo que se propone. Estas decisiones están definidas como las acciones usuales que lleva la planificación, tienen una precondición y un efecto, que en este caso es un evento que define el cambio que se le realiza a la nación que tome esa decisión. 

Los eventos en el mapa están separados en dos tipos, los eventos de la simulación y los eventos que forman parte de la ejecución de las decisiones. Los eventos de simulación son los que se ejecutan en cada paso de la simulación, estos eventos son los que modifican el estado del mapa, o de algunas naciones en caso de que sea definido de esta forma específica. Los eventos de las decisiones son los que se ejecutan cuando una nación toma una decisión, tambien son los que se utilizan dentro del algoritmo de planificación como acciones para cambiar de estado.

Las decisiones son las acciones que pueden tomar las naciones para lograr sus objetivos. Una decisión está formada por una precondición que debe cumplirse para que la nación pueda tomar la decisión, y un efecto que es un evento que se ejecuta cuando la nación toma la decisión.



<h2> Inteligencia Artificial</h2>

<h4> Planificación</h4>

Para desarrollar la planificación se utilizó el algoritmo  para encontrar el camino más corto entre el estado inicial de la nación y el estado objetivo, 

