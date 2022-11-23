# ESPY

Lenguaje funcional. Proyecto final del curso de Diseño de Compiladores del Tecnológico de Monterrey.

- [Requisitos](#requisitos)
- [Instalación](#instalación)
    - [Primeros ajustes](#primeros-ajustes) 
- [Manual de usuario](#manual-de-usuario)
    - [Ejecución de una programa ESPY](#ejecución-de-una-programa-espy)
    - [Librería](#librería)
    - [Palabras reservadas](#palabras-reservadas)
    - [Tipos de datos](#tipos-de-datos)
        - [Literales](#literales)
            - [Números](#números)
            - [Booleanos](#booleanos)
            - [Caracteres](#caracteres)
            - [Nulos](#nulos)
        - [Estructurados](#estructurados)
            - [Listas](#listas)
    - [Declaraciones](#declaraciones)
        - [Variables](#variables)
            - [Globales](#globales)
            - [Locales](#locales)
        - [Funciones](#funciones)
    - [Expresiones](#expresiones)
        - [Condicionales](#condicionales)
        - [Aritméticas](#aritméticas)
        - [Relaciones](#relacionales)
        - [Booleanas](#booleanas)

## Requisitos

Para poder correr ESPY es necesario tener instalado:

- [Docker](https://docs.docker.com/get-docker/)

## Instalación

1. Clonar el repositorio

```bash
git clone https://github.com/davidha99/espy.git
```

2. Instalar la imagen del proyecto

Dentro de la raíz del proyecto, ejecutar el siguiente comando de Docker para crear la imagen:

```bash
docker build -t espy:latest .
```

(Nota el `.` al final del comando, es importante)

3. Crear el contenedor

```bash
docker run -it espy:latest bash
```

Este comando creará por primera vez el contender, y entrará a la línea de comandos dentro contenedor. Para salir, presionar `CTRL-D`.

4. Listo! Ahora cada vez que se quiera ejecutar el contenedor con ESPY, ejecutar:

```bash
docker start -i espy
```

### Primeros ajustes

Antes de comenzar a ejecutar ESPY es necesario hacer unos ajustes dentro del ambiente del contenedor.

1. Si todavía no has entrado al contenedor, ejecutar:

```bash
docker start -i espy
```

2. Hacer ejecutable el archivo `espy.py` con el siguiente comando:

```bash
chmod u+x espy.py
```

3. Listo! Ahora puedes correr cualquier archivo de ESPY con el siguiente comando:

```bash
./espy.py <ruta/al/archivo.espy>
```

En caso de marcar algún error, realizar los siguientes pasos:

1. Abrir el archivo `espy.py` con VIM

```bash
vim espy.py
```

2. Ejecutar el siguiente comando VIM para cambiar el formato del archivo

```vim
:set --file-format=unix
```

## Manual de usuario

Antes de comenzar, es importante leer los [primeros ajustes](#primeros-ajustes) para ser capaz de ejecutar ESPY dentro del contenedor.

### Ejecución de una programa ESPY

Para compilar programas en ESPY, basta con ejecutar ESPY con el archivo `.espy` de la siguiente manera:

```bash
./espy.py <ruta/archivo.espy>
```

### Ejecución del interpretador ESPY

Para mostrar las funcionalidades de ESPY y su sintaxis utilizaremos el interpretador de ESPY, ya que consideramos que la mejor forma de aprender un nuevo lenguaje de programación es con la práctica.

Para abrir el interpretador de ESPY, solamente hay que ejecutar:

```bash
./espy.py
```

Este comando ejecutará el interpretador y estará listo para recibir instrucciones.

```bash
espy> 
```

### Librería

ESPY cuenta con una librería de funciones auxiliares para el desarrollador, estas funciones son:

- `add1`: Recibe de parámetro un número, y regresa el número sumado con 1
- `sub1`: Recibe de parámetro un número, y regresa el número restado con 1
- `char->num`: Recibe de parámetro un caracter y regresa su valor en ASCII
- `num->char`: Recibe de parámetro un número y regresa su caracter ASCII
- `num?`: Recibe de parámetro un número, y regresa un booleano dependiendo de si el parámetro es un número o no.
- `boolean?`: Recibe de parámetro un número, y regresa un booleano dependiendo de si el parámetro es un booleano o no.
- `char?`: Recibe de parámetro un número, y regresa un booleano dependiendo de si el parámetro es un caracter o no.
- `null?`: Recibe de parámetro un número, y regresa un booleano dependiendo de si el parámetro es nulo o no.

Algunos de los ejemplos utilizarán estas funciones auxiliares de ESPY.

### Palabras reservadas

ESPY cuenta con las siguientes palabras reservadas:

```
not         let         def
and         if          lambda
or          var         list
```

### Tipos de datos

ESPY soporta los siguientes tipos de datos:

- [Literales](#literales)
    - [Números](#números)
    - [Booleanos](#booleanos)
    - [Caracteres](#caracteres)
    - [Nulos](#nulos)
- [Estructurados](#estructurados)
    - [Listas](#listas)

#### Literales

##### Números

El rango de números que soporta ESPY es de `(-2^29)` a `(2^29 - 1)`, por lo tanto es número más pequeño es `-536870912` y el más grande es `536870911`.

```
espy> 10
10

espy> -536870912
-536870912

espy> 536870911
536870911
```

##### Booleanos

Los booleanos en ESPY son representados de la siguiente manera:

- `#t` para booleano verdadero
- `#f` para booleano falso

```
espy> #t
#t

espy> #f
#f
```

##### Caracteres

Los caracteres en ESPY se representan con `\#` antes del caracter, por ejemplo, `\#A` es el caracter `A`.

```
espy> \#A
\#A

espy> \#z
\#z

espy> (char? \#A)
#t

espy> (char? A)
#f
```

##### Nulos

ESPY también reconoce valores nulos y estos son representados como `()`.

```
espy> ()
()
```

#### Estructurados

Por el momento, ESPY solamente soporta listas como elemento estructurado

##### Listas

### Declaraciones

ESPY soporta declaraciones para variables y funciones.

#### Variables

Dentro de las declaraciones de variables, ESPY cuenta con 2 tipos:

1. [Globales](#globales)
2. [Locales](#locales)

##### Globales

Se utiliza la instrucción `var` para declarar una variable global, y la sintaxis es la siguiente:

```
(var ([<nombre_var> <expr>]))
```

Para demostrar el uso de variables globales, se tiene el siguiente ejemplo:

```
espy> (var [x 10])
10

espy> x
10

espy> (var [y (+ 1 2 3)])
6

espy> (var [z (if (char? 1) (+ 1 2) (- 10 2))])
8

espy> (+ x y z)
24
```

##### Locales

Para las variables locales, se tiene la instrucción `let`. Todas las variables dejan de existir una vez que se termine de ejecutar la instrucción `let`.

La sintaxis básica es la siguiente:

```
(let ([<nombre_var1> <expr1>] [<nombre_var2> <expr2>] ...) <expr_let>)
```

El siguiente ejemplo demuestra el uso de `let`:

```
espy> (var [x 10])
10

espy> (let ([x 20] (+ x x))
40

espy> (+ x x)
20
```

#### Funciones

Para declarar funciones ESPY utiliza las instrucción `def`. La sintaxis de declaración de funciones se explicará por partes.

```
(def <función> <expr>)
```
donde:

- `<función>`: es la definición de la función
- `<expr>`: puede ser cualquier expresión, también se puede realizar la llamada a la función con parámetros (si es que se definió una función con parámetros).

Ahora, para la definición de `<función>` se tiene la siguiente sintaxis:

```
[<nombre_func> (lambda (<param1> <param2> ...) <expr_func>] ...)
```

donde:

- `<nombre_func>`: es el nombre de la función
- `<param1> <param2> ...`: es una lista de parámetros de la función
- `<expr_func>`: es el cuerpo de la función, puede ser cualquier expresión

##### Fibonacci

Para dejar más clara la sintaxis de funciones, se tiene el siguiente programa que calcula el fibonacci de un número utilizando funciones en ESPY.

```
; fib.espy

(def ([fib (lambda (x) 
            (if (<= x 2) 
            1 
            (+ (fib (- n 1))(fib (- n 2)))))])
    (fib 6))

$ ./espy fib.espy
8
```

##### Sumatoria

Otro ejemplo que utiliza funciones, se tiene el siguiente programa que define una función `sum` que recibe de 2 parámetros `n` y `acc`, y calcula la sumatoria del rango.

```
; sum.espy

(def ([sum (lambda (n acc)
                (if (== n 0)
                ac
                (sum (sub1 n) (+ n ac))))])
    (sum 10 0))

$ ./espy sum.espy
55
```

##### Factorial

Como último ejemplo, se define una función `fact` que recibe de parámetro un número `n` y calcula su factorial.

```
; fact.espy

(def ([fact (lambda (n) 
            (if (= n 0) 
            1 
            (* n (fact (- n 1)))))]) 
    (fact 3))

$ ./espy fact.espy
6
```


### Expresiones

ESPY cuenta con los siguientes tipos de expresiones:

- [Condicionales](#condicionales)
- [Expresiones aritméticas](#aritméticas)
- [Expresiones relacionales](#relacionales)
- [Expresiones booleanas](#booleanas)

#### Condicionales

ESPY soporta el condicional `if` para el control de ejecución de código. La sintaxis es la siguiente:

```
(if <expr_bool> <expr_consecuente> <expr_alternativa>)
```

- `<expr_bool>`: es cualquier expresión que evalúe a un booleano.
- `<expr_consecuente`: es la expresión que se ejecutará en caso de que `<expr_bool>` evalúe a `#t`.
- `<expr_alternativa>`: es la expresión que se ejcutarña en caso de que `<expr_bool>` evalúe a `#f`.

Algunos ejemplos son:

```
espy> (if #t (+ 6 6) (+ 2 2))
12

espy> (if #f 12 (if #f 13 4))
4

espy> (if (not (boolean? #t)) 15 (boolean? #f))
#t

espy> (if (not (if (if (not 1) (not 2) (not 3)) 4 5)) 6 7)
7
```

#### Aritméticas

Para las operaciones aritméticas se tienen los siguientes operadores:

- `+`
- `-`
- `*`
- `/`

La sintaxis para las operaciones aritméticas es la siguiente

```
( <operador> <expr1> <expr2> <expr3> ... <expr_n>)
```

Algunos ejemplos son:

```
espy> (+ 1 2 3 4 5)
15

espy> (+ 1 2 (- 13 10) 40 (* 1 2 3))
52

espy> (/ 50 10)
5

espy> (+ (if #f 2 10) 10 10)
30
```

#### Relacionales

Para las operaciones relaciones se tienen los siguientes operadores:

- `<=`
- `>=`
- `==`
- `<`
- `>`

Las operaciones relaciones sólo aceptan dos expresiones:

```
( <operador> <expr1> <expr2>)
```

Algunos ejemplos son:

```
espy> (< 10 20)
#t

espy> (let ([n 0]) (if (== n 0) 10 20))
10
```

#### Booleanas

Para las operaciones booleans se tienen los siguientes operadores:

- `and`
- `or`
- `not`

La sintaxis básica de las expresiones booleanas es la siguiente:

```
(and <expr1> <expr2> <expr3> ... <expr_n>)
(or <expr1> <expr2> <expr3> ... <expr_n>)
(not <expr1>)
```

Todas las expresiones deben evaluar a valores booleanos. Un ejemplos es:

```
espy> (and (== 10 10) #t (char? \#A) (if (num? 10) #t #f))
#t

espy> (or (== 10 0) #f (char? 10) (if (not #f) #t #f))
#t

espy> (not (if (and (char? 10) (num? \#A)) #f #t))
#f
```