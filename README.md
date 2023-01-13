<h1> Evolución de Naciones</h1>

<h2> Simulación</h2>
Se quiere simular el desarrollo de ciertas Naciones en un tiempo definido y en una zona geográfica generada. Estas Naciones van a contener ciertas Provincias de las que se proporciona su desarrollo y su población, mientras que de las naciones se proporcionarán los rasgos distintivos de estas. Además, pueden existir zonas neutrales o mares, los cuales representan áreas vacías. Se tomará como base principal para la simulación a los Eventos (a los cuales se les atribuye una distribución específica y un período de tiempo), todo suceso en la simulación será un Evento; estos pueden provocar una toma de decisiones por parte de una Nación, las cuales varían con respecto al evento al que se enfrentan y las características que posee esta Nación.
Se podrán recopilar datos sobre los cambios territoriales, el desarrollo, la población y las características de las Naciones y con estos analizar la influencia de las características de una Nación ya sean geográficas, políticas o económicas en el desarrollo que esta sea capaz de alcanzar.



<h2> DSL </h2>

Para facilitar la creación de escenarios para la simulación se implementó un Lenguaje de Dominio Específico que además de permitir la creación de forma sencilla de una simulación desde cero, creando cada uno de sus objetos y procesos, tiene la característica de que es Turing-Completo, por lo que cualquier programa es implementable con código del DSL.

<h4> Arquitectura del compilador y gramática</h4>


Para la lexemización, tokenización y parser se utilizaron los tokens definidos en lexer.py y la biblioteca de python SLY. Esta es una biblioteca para escribir analizadores y compiladores. Se basa libremente en las herramientas tradicionales de construcción de compiladores lex(tokenizar) y yacc (yet another compiler-compiler).

Para la obtención del AST se utilizó el algoritmo de análisis sintáctico (parser) LALR(1) implementado en SLY. Un analizador LALR (Look-Ahead LR)  es una versión simplificada de un analizador LR canónico, para analizar un texto de acuerdo con un conjunto de reglas de producción especificadas por una gramática formal para un lenguaje.

SLY utiliza una técnica de análisis conocida como análisis LR o análisis shift-reduce. El análisis LR es una técnica de abajo hacia arriba que intenta reconocer el lado derecho de varias reglas gramaticales. Cada vez que se encuentra un lado derecho válido en la entrada, se activa el método de acción apropiado y los símbolos gramaticales del lado derecho se reemplazan por el símbolo gramatical del lado izquierdo.

Al igual que con otros tipos de gramáticas LR, un analizador o gramática LALR es bastante eficiente para encontrar el único análisis de abajo hacia arriba correcto en un solo escaneo de izquierda a derecha sobre el flujo de entrada, porque no necesita usar el retroceso. El analizador siempre utiliza una búsqueda anticipada, representando LALR(1) una búsqueda anticipada de un token. Este parser presenta el inconveniente de que, como consecuencia de la técnica shift-reduce, no puede garantizar el análisis correcto en gramáticas ambiguas, siendo LR más poderoso en este aspecto.

Las producciones se encuentran en parser.py y las acciones que se realizan para cada producción se encuentran en execution.py.

Todos los detalles acerca de las reglas de gramática utilizada se puede ver en parser.out, además de visualizar cada uno de los estados de la ejecución actual.


<h4> Diseño del Lenguaje</h4>

<h5> Tipos </h5>

- `element`: elementos que se usarán en la simulación, y se encuentran presentes en el mapa: `nation`, `province`, `sea`, `neutral`, `trait`, `decision`, `distribution`, `category`, `event`.
- `interger`: número entero.
- `decimal`: número flotante.
- `boolean`: buleano, puede ser `true` o `false`.
- `string`: cadena de texto.
- `list`: lista de elementos.
- `time`: tiempo el cual puede ser en años, meses o días(y, m, d respectivamente), se usa para definir los tiempos en la simulación.


<h5> Sintaxis </h5>

- Sintaxsis similar a Python en cuanto a las funcionalidades y dinamismo.
- Instrucciones separadas por `;`.
- Los bloques de código de los lops, condicionales y eventos se encierran en `{}`.
- Para el caso de los argumentos de las funciones o eventos se usa `()`.
- Mientras que los parametros se encierran en `<< >>`.
- Parametros y argumentos separados por `,`.
- Admite aritméticas como `+`, `-`, `/`, `//`, `*`, `**`, `%`.
- Uso de operadores `==`, `!=`, `>=`, `>`, `<=`, `<`.
- Uso de operadores lógicos `not`, `and`, `or`, `xor`.
- Para asignar las variables o hacer cambios en los valores de los `elements` se usa `=`.
- Para acceder a los valores de los elementos se usa `->`.
- Se puede asignar el tipo de los argumentos o el nombre de los parámetros usando  `:`.


<h5> Loops </h5>

- `repeat`: ciclo for desde unicio hasta un final, ambos indicados.
- `foreach`: ciclo for iterando en una lista.
- `while`: ciclo while


<h5> Condicionales </h5>

- Clásicos `if` y `else`.



<h5> Ejemplos de código</h5>

```
category socialism();
category capitalism();

province Havana(100, 10, 10345, []);
province Mayabeque(236, 10, 204, []);
province New_York(2056, 20, 103856, []);
province California(341, 30, 402175, []);

nation Cuba([Havana, Mayabeque], [socialism]);
nation USA([New_York, California], [capitalism]);

distribution pg(expon, scale: 4);

show(pos(Cuba->provinces, 0)->extension);
pos(Cuba->provinces, 0) -> extension= 200;
show(pos(Cuba->provinces, 0)->extension);

event population_growth(pg, socialism, true, []){
    foreach <<prov>> (map->provinces){
        prov->population= irvs(expon, loc: prov->population);
    }
}

event population_mortality(pg, socialism, true, []){
    foreach <<prov>> (map->provinces){
        prov->population= prov->population - irvs(expon, loc: 0);
    }
}

simulate( 100d );
```

<h4> Ejecución del programa</h4>

Para ejecutar el código, primero debe instalar las dependencias de Python que se encuentran en los requirements.txt con `pip install -r requirements.txt`. Luego ejecuta `streamlit run main.py` con el terminal en la dirección de la carpeta src, en caso de estar en otra dirección debes incluir la dirección en el comando `streamlit run <dirección>main.py`, luego la interfaz visual se muestra en el navegador predeterminado.




