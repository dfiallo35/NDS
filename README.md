<h1> Evolución de Naciones</h1>

<h2> Simulación</h2>
Se quiere simular el desarrollo de ciertas Naciones en un tiempo definido y en una zona geográfica generada. Estas Naciones van a contener ciertas Provincias de las que se proporciona su desarrollo y su población, mientras que de las naciones se proporcionarán los rasgos distintivos de estas. Además, pueden existir zonas neutrales o mares, los cuales representan áreas vacías. Se tomará como base principal para la simulación a los Eventos (a los cuales se les atribuye una distribución específica y un período de tiempo), todo suceso en la simulación será un Evento; estos pueden provocar una toma de decisiones por parte de una Nación, las cuales varían con respecto al evento al que se enfrentan y las características que posee esta Nación.
Se podrán recopilar datos sobre los cambios territoriales, el desarrollo, la población y las características de las Naciones y con estos analizar la influencia de las características de una Nación ya sean geográficas, políticas o económicas en el desarrollo que esta sea capaz de alcanzar.



<h2> DSL </h2>

Para facilitar la creación de Eventos, Mapas y otros elementos fundamentales de la simulación se implementó un Lenguaje de Dominio Específico que además de permitir la creación de forma sencilla de una simulación desde cero, creando cada uno de sus objetos y procesos, tiene la característica de que es Turing-Completo, por lo que cualquier programa es implementable con código del DSL.

<h4> Arquitectura del compilador y gramática</h4>


Para la lexemización, tokenización y parser se utilizaron los tokens definidos en lexer.py y la biblioteca de python SLY. Esta es una biblioteca para escribir analizadores y compiladores. Se basa libremente en las herramientas tradicionales de construcción de compiladores lex(tokenizar) y yacc (yet another compiler-compiler).

Para la obtención del AST se utilizó el algoritmo de análisis sintáctico (parser) LALR(1) implementado en SLY. Un analizador LALR (Look-Ahead LR)  es una versión simplificada de un analizador LR canónico, para analizar un texto de acuerdo con un conjunto de reglas de producción especificadas por una gramática formal para un lenguaje.

SLY utiliza una técnica de análisis conocida como análisis LR o análisis shift-reduce. El análisis LR es una técnica de abajo hacia arriba que intenta reconocer el lado derecho de varias reglas gramaticales. Cada vez que se encuentra un lado derecho válido en la entrada, se activa el método de acción apropiado y los símbolos gramaticales del lado derecho se reemplazan por el símbolo gramatical del lado izquierdo.

Al igual que con otros tipos de gramáticas LR, un analizador o gramática LALR es bastante eficiente para encontrar el único análisis de abajo hacia arriba correcto en un solo escaneo de izquierda a derecha sobre el flujo de entrada, porque no necesita usar el retroceso. El analizador siempre utiliza una búsqueda anticipada, representando LALR(1) una búsqueda anticipada de un token. Este parser presenta el inconveniente de que, como consecuencia de la técnica shift-reduce, no puede garantizar el análisis correcto en gramáticas ambiguas, siendo LR más poderoso en este aspecto.

Las producciones se encuentran en parser.py y las acciones que se realizan para cada producción se encuentran en execution.py.

Todos los detalles acerca de las reglas de gramática utilizada se puede ver en parser.out, además de visualizar cada uno de los estados de la ejecución actual.


<h4> Diseño del Lenguaje</h4>

<h5> Ejemplos de código</h5>


<h4> Ejecución del programa</h4>







