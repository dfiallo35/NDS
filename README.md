<h1> Evolución de Naciones</h1>

<h2> Simulación</h2>
Se quiere simular el desarrollo de ciertas Naciones en un tiempo definido y en una zona geográfica generada. Estas Naciones van a contener ciertas Provincias de las que se proporciona su desarrollo y su población, mientras que de las naciones se proporcionarán los rasgos distintivos de estas. Además, pueden existir zonas neutrales o mares, los cuales representan áreas vacías. Se tomará como base principal para la simulación a los Eventos (a los cuales se les atribuye una distribución específica y un período de tiempo), todo suceso en la simulación será un Evento; estos pueden provocar una toma de decisiones por parte de una Nación, las cuales varían con respecto al evento al que se enfrentan y las características que posee esta Nación.
Se podrán recopilar datos sobre los cambios territoriales, el desarrollo, la población y las características de las Naciones y con estos analizar la influencia de las características de una Nación ya sean geográficas, políticas o económicas en el desarrollo que esta sea capaz de alcanzar.



<h2> DSL </h2>

Para facilitar la creación de Eventos, Mapas y otros elementos fundamentales de la simulación se implementó un Lenguaje de Dominio Específico que además de permitir la creación de forma sencilla de una simulación desde cero, creando cada uno de sus objetos y procesos, tiene la característica de que es Turing-Completo, por lo que cualquier programa es implementable con código del DSL.

<h4> Arquitectura del compilador </h4>




<h4> Parser y Gramática</h4>

Para la obtención del AST se utilizó el parser LALR(1) implementado en la biblioteca de python SLY.  Esta es una biblioteca para escribir analizadores y compiladores. Se basa libremente en las herramientas tradicionales de construcción de compiladores lex y yacc (yet another compiler-compiler) e implementa el mismo algoritmo de análisis sintáctico LALR(1).
Un analizador LALR (Look-Ahead LR)  es una versión simplificada de un analizador LR canónico, para analizar un texto de acuerdo con un conjunto de reglas de producción especificadas por una gramática formal para un lenguaje.

Al igual que con otros tipos de analizadores LR, un analizador LALR es bastante eficiente para encontrar el único análisis de abajo hacia arriba correcto en un solo escaneo de izquierda a derecha sobre el flujo de entrada, porque no necesita usar el retroceso. Al ser un analizador de búsqueda anticipada por definición, siempre utiliza una búsqueda anticipada, siendo LALR(1) el caso más común, lo que representa una búsqueda anticipada de un token.

El analizador LALR(1) es menos poderoso que el analizador LR(1) y más poderoso que el analizador SLR(1), aunque todos usan las mismas reglas de producción. La simplificación que introduce el analizador LALR consiste en fusionar reglas que tienen conjuntos de elementos del núcleo idénticos, porque durante el proceso de construcción del estado LR(0) no se conocen las búsquedas anticipadas. Esto reduce el poder del analizador porque no conocer los símbolos de anticipación puede confundir al analizador en cuanto a qué regla gramatical elegir a continuación, lo que genera conflictos de reducción/reducción. Todos los conflictos que surgen al aplicar un analizador LALR(1) a una gramática LR(1) inequívoca son conflictos de reducción/reducción. El analizador SLR(1) realiza más fusiones, lo que introduce conflictos adicionales.

Todos los detalles acerca de la gramática utilizada se puede ver en parser.out, además de 

<h4> Generación de código</h4>


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


<h5> CONDITIONALS </h5>

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







