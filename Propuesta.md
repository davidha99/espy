
![](https://i.imgur.com/HthnYwP.png)

<div style="text-align:center;">
    <h1>ESPY</h1>
    <h3>Diseño de compiladores</h3>
    <br>
	<h3>Omar David Hernández Aguirre | A01383543</h3>
    <h3>Bernardo García Zermeño | A01383543</h3>
	<br>
	<h3>Profesor: M.C. Elda G. Quiroga, Dr. Héctor Ceballos, PhD</h3>
	<br>
	<h4>Monterrey, Nuevo León</h4>
	<h4>01 de octubre de 2022</h4>
	<br>
</div>

---

## Objetivo principal y categoría (área)

**ESPY** es un lenguaje de paradigma funcional implementado en Python. El paradigma funcional es muy popular por su gran expresividad gracias al concepto de funciones puras. Las funciones puras ayudan a que el software sea fácil de entender porque las funciones individuales son independientes y pueden ser escritas, entendidas y probadas de forma independiente.


## Requerimientos

A continuación se presentan los elementos básicos del lenguaje ESPY.

### Elementos básicos


#### Palabras reservadas:

```
main       if       do           or
define     cond     quote        not
set        else     and          display     
```


#### Tokens

```
ID
LPAREN   -> (
RPAREN   -> )
EQUALS   -> =
SQUOTE   -> '
LBRACK   -> [
RBRACK   -> ]
GT       -> >
LT       -> <
PLUS     -> +
MINUS    -> -
TIMES    -> *
DIVIDE   -> /
CTEINT
CTEFLOAT
BANNER
```


### Diagramas de sintaxis


|    Nombre   |               Diagrama                |
| :---------: | :-----------------------------------: |
| Program     | ![](https://i.imgur.com/XLchsLX.png)  |
| Main        | ![](https://i.imgur.com/AAoK9mF.png)  |
| Form        | ![](https://i.imgur.com/7zYxKJT.png)  |
| Variable Definition | ![](https://i.imgur.com/GGejknG.png)  |
| Variable    | ![](https://i.imgur.com/nq7UNj1.png)  |
| Body        | ![](https://i.imgur.com/3fpjx8S.png)  |
| Keyword     | ![](https://i.imgur.com/KWAcA5K.png)  |
| Expression  | ![](https://i.imgur.com/pvgbyeb.png)  |
| Constant    | ![](https://i.imgur.com/9eCgUcr.png)  |
| Application | ![](https://i.imgur.com/ki7W0vs.png)  |
| Derived Expresssion | ![](https://i.imgur.com/D7Nunos.png)  |
| Identifier  | ![](https://i.imgur.com/JSB7xwP.png)  |
| Subsequent  | ![](https://i.imgur.com/M57xnQ4.png)  |
| Letter      | ![](https://i.imgur.com/muHSzcG.png)  |
| Digit       | ![](https://i.imgur.com/rxQ0z8k.png)  |
| Datum       | ![](https://i.imgur.com/uSA1cAS.png)  |
| Boolean     | ![](https://i.imgur.com/zn68YK2.png)  |
| Number      | ![](https://i.imgur.com/Z2D8n75.png)  |
| Character   | ![](https://i.imgur.com/OOK03Dd.png)  |
| String      | ![](https://i.imgur.com/dqIw2eQ.png)  |
| String Character    | ![](https://i.imgur.com/t0X6Qit.png)  |
| List        | ![](https://i.imgur.com/XLchsLX.png)  |
| Num10       | ![](https://i.imgur.com/NjBo8nu.png)  |
| Int         | ![](https://i.imgur.com/XChkX4i.png)  |
| Float       | ![](https://i.imgur.com/fYVx17g.png)  |

### EBNF

A continuación, se muestra la especificación de ESPY en la forma EBNF (*Extended Back-Naur Form*).[^1]

```
/* PROGRAMS */
Program   ::= Main
Main      ::= '(' 'main' Form+ ')'
Form      ::= VariableDefinition | Expression

/* DEFINITIONS */

VariableDefinition
          ::= '(' 'define' Variable Expression ')'
          | '(' 'define' '(' Variable Variable* ')' Body ')'
Variable  ::= Identifier
Body      ::= Definition* Expression+
Keyword   ::= Identifier


/* EXPRESSSIONS */

Expression
          ::= Constant
          | Variable
          | '(' 'quote' Datum ')' 
          | "'" Datum
          | '(' 'if' Expression Expression Expression ')' 
          | '(' 'if' Expression Expression ')'
          | '(' 'set' Variable Expression ')'
          | Application
          | DerivedExpression

Constant  ::= Boolean | Number | Character | String

Application
          ::= '(' Expression Expression* ')'

DerivedExpression
          ::= 'cond' | 'and' | 'or' | 'do'

/* Esto se puede usar para las lambdas
Formals   ::= Variable  | '(' Variable* ')' | '(' Variable+ '.' Variable ')'
Application
          ::= '(' Expression Expression* ')'
*/

/* IDENTIFIERS */

Identifier
          ::= Letter Subsequent*
Subsequent
          ::= Letter | Digit | '_'
Letter    ::= [a-zA-Z]
Digit     ::= [0-9]

/* DATA */
Datum     ::= Boolean | Number | Character | String | List
Boolean   ::= 'true' | 'false'
Number    ::= Num10
Character ::= '#' '\' AnyCharacter | '#' '\' 'newline' | '#' '\' 'space'
String    ::= '"' StringCharacter '"'
StringCharacter
          ::= '\' '"' | '\' '\' | AnyCharacterExceptDoubleQuotesAndBackSlash
List      ::= '(' Datum* ')'

/* NUMBERS */
Num10     ::= Int
          |   Float
Int       ::= Digit+
          |   '-' Digit+
Float     ::= Digit+ '.' Digit+
          |   '-' Digit+ '.' Digit+
```


### Características semánticas principales

* Las variables declaradas tendrán en todo momento un alcance estático
* Los objetos dentro de la programación con ESPY tienen extensión indefinida
* Los procedimientos dictados dentro de la programación con ESPY serán manejados como objetos
* Los argumentos en las funciones son pasados por valor (*passed by value*)
* La recursividad aplicada será de modo PTC (*Proper Tail Recursion*)


#### Tabla de compatibilidad de datos

|L. O. |R.O.  |=+    |-     |*     |/     |=     |>     |&lt;     |>=    |&lt;=    |and   |or    |not   |exp   |max   |min   |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
|int   |int   |int   |int   |int   |int   |bool  |bool  |bool  |bool  |bool  |error |error |error |int   |int   |int   |
|int   |float |float |float |float |float |error |bool  |bool  |bool  |bool  |error |error |error |float |float |float |
|int   |char  |error |error |error |error |error |error |error |error |error |error |error |error |error |error |error |
|int   |bool  |error |error |error |error |error |error |error |error |error |error |error |error |error |error |error |
|float |float |float |float |float |float |bool  |bool  |bool  |bool  |bool  |error |error |error |float |float |float |
|float |int   |float |float |float |float |error |bool  |bool  |bool  |bool  |error |error |error |float |float |float |
|float |char  |error |error |error |error |error |error |error |error |error |error |error |error |error |error |error |
|float |bool  |error |error |error |error |error |error |error |error |error |error |error |error |error |error |error |
|char  |char  |char  |error |error |error |bool  |bool  |bool  |bool  |bool  |error |error |error |error |error |error |
|char  |bool  |error |error |error |error |error |error |error |error |error |error |error |error |error |error |error |
|char  |int   |error |error |error |error |error |error |error |error |error |error |error |error |error |error |error |
|char  |float |error |error |error |error |error |error |error |error |error |error |error |error |error |error |error |
|bool  |bool  |error |error |error |error |bool  |error |error |error |error |bool  |bool  |bool  |bool  |bool  |bool  |
|bool  |int   |error |error |error |error |error |error |error |error |error |error |error |error |error |error |error |
|bool  |float |error |error |error |error |error |error |error |error |error |error |error |error |error |error |error |
|bool  |char  |error |error |error |error |error |error |error |error |error |error |error |error |error |error |error |


### Descripción de funciones especiales

- Expresiones **_lambda_**:

```scheme
(lambda <formals> <body>)
```


- ESPY contará con los siguientes *procedures* primitivos:
    - `+`: suma de operandos
    - `-`: resta de operandos
    - `*`: multiplicación de operandos
    - `/`: división de operandos
    - `head`: regresa el *head* de una lista
    - `tail`: regresa el *tail* de una lista
    - `display`: despliega un mensaje en pantalla


### Tipos de datos

ESPY contará con los siguientes tipos de datos:
- Enteros
- Flotantes
- Caracter
- Boolean
- Letreros
- Listas

## Desarrollo

Se utilizará Python para la implementación de ESPY, y los sistemas operativos que se usarán para el desarrollo serán MacOS, y Windows.

## Ejemplo de un programa en ESPY

````scheme
; Procedure principal
(main
    ; Asignación de variables
    (define x 2)                ;  x -> 2
    (+ x 1)                     ;  3
    (set x 4)                   ;  x -> 4
    (+ x 1)                     ;  5
    
    ; Creación de funciones (procedures) sin parámetros
    (define (foo1)
        (+ 2 2))
    
    ; Creación de funciones (procedures) con parámetros
    (define (foo2 x y)
        (* x y))
    
    ; Condicionales
    (if (> 3 2) 'si 'no)       ; si
    (if (> 2 3) 'si 'no)       ; no
    (if (> 3 2)
        (- 3 2)
        (+ 3 2))
    
    ; sin else
    (cond ((> 3 2) 'mayor)
          ((< 3 2) 'menor))    ; mayor
    
    ; con else
    (cond ((> 3 3) 'mayor)
          ((< 3 3) 'menor)
          (else 'equal))       ; equal
)

````
[^1]: En caso de querer interactuar con los diagramas, ingresa el [código en la forma EBNF](#EBNF) en este [sitio](https://bottlecaps.de/rr/ui#_Production).

## Bibliografía

* Scheme - Table of Contents. Cmu.edu. Published 2022. Accessed October 1, 2022. https://www.cs.cmu.edu/Groups/AI/html/r4rs/r4rs_toc.html
* An Introduction to Scheme and its Implementation - Table of Contents. Rpi.edu. Published 2022. Accessed October 1, 2022. http://cs.rpi.edu/academics/courses/fall00/ai/scheme/reference/schintro-v14/schintro_toc.html
