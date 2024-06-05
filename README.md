## Opis

Projekt języka programowania “Parasite”. Napisany w języku Python.

Język Parasite umożliwia zaimplementowanie paradygmatu programowania aspektowego do języka. Poza charakterystyczną opcją definiowania aspektów do funkcji, język umożliwia inicjalizację i przypisywanie zmiennych, obsługę pętli while oraz instrukcji warunkowych, definiowanie funkcji z argumentami wywołania, funkcje rekurencyjne, operacje arytmetyczne, konwersja typów, konkatenacje typów string.

Implementacja wszystkich elementów projeku napisana w języku Python.

## Standardowe operacje

- inicjalizacja i przypisanie zmiennej
- obsługa operacji arytmetycznych ( o różnym priorytecie wykonania)
- konkatenacja typu string
- instrukcje warunkowe (if, elif, else)
- instrukcja pętli (while)
- definiowanie funkcji
- wywołania funkcji (zwykłe i rekurencyjne)
- konwersja typów (operator ->)

## Charakterystyczne operacje języka

- obsługa aspektów (funkcji, które mają za zadanie wywołać się przed lub po wybranej funkcji)
    - definiowanie aspektów (słowo kluczowe “aspect”)
    - funkcja aspektowa ma składać się z:
        - “before” (działanie wykonywane przed funkcją powiązaną z aspektem) i
        - “after”(działanie wykonywane po funkcji powiązanej z aspektem)
        - before lub after są opcjonalne, tzn. można wywołać tylko before lub tylko after albo oba, jednak zawsze w aspekcie musi znaleźć się przynajmniej jedno z nich
- Przykłady definicji i wywołań poniżej

## Założenia języka (koncepcja)

- statycznie typowany
- typowanie silne
- zmienne mutowalne (tylko do typu zmiennej)
- argumenty przekazywane przez wartość
- program musi posiadać funkcję main()
- zmienna zdefiniowana lokalnie (w bloku funkcji czy pętli) przykrywa zmienną zewnętrzną
- przeciążanie funkcji NIE jest dozwolone
- Obsługiwane typy danych
    - integer (int)
    - float (float)
    - string (str)
    - boolean (bool)
- głębokość rekurencji = 200
- maksymalna długość string = 200

## Przykłady wykorzystania języka

inicjalizacja i przypisanie wartości

```jsx
int a = 5
str b = "hi"

a = 3
a = "hello" // niedozwolone
```

---

operacje artymetyczne

```jsx
int a = 6
a = a + 10 * (5-2) // a == 36
```

---

komentarze

```jsx
// this is a comment
```

---

instrukcje warunkowe

```jsx
int a = 6
if a > 3 {
	print("a is greater than 3")
} elif a < 3 {
	print("a is smaller than 3")
} else {
	print("a is equal to 3")
}
// output:
// a is greater than 3
```

---

instrukcja pętli

```jsx
int i = 0
while i < 10 {
	print(i)
	i = i + 1
}
```

---

przykrywanie zmiennych

```jsx
main(){
	int a = 10
	int b = 12
	if b > 10 {
		int a = 15
		print(a)
	}
}
//output
// 15
```

---

Funkcja z argumentem (przez wartość)

```jsx
square(x: int) int {
	return x*x
}

int x = 5
int a = square(x) // a == 25, x == 5
```

---

funkcja z argumentem

```jsx
triangleArea(a: int, h: int) float {
	return 0.5 * a * h
}

int a = 3
int h = 7
float result = triangleArea(a, h) // result == 10.5
```

---

funkcja rekurencyjna

```jsx
fibonacci(n: int) int {
	if n <= 1 {
		return n
	} else {
		return fibonacci(n-1) + fibonacci(n - 2)
	}
}

int result = fibonacci(5)
```

---

aspekty

```jsx
// askept z wylistowaniem argumentów funkcji, do której został podczepiony

doSomething(){
        print("hello world")
}

aspect logFunctionCall(doSomething){
        int coutner = 0;
        before{
		        for arg in function.args {
			        print(arg.value)
			        print(arg.name)
			        print(arg.type)
			        if arg.type is int {
				        print("argument " + arg.value + "jest typu int")
			        }
		        }
            print("starting function " function.name)
        }
        after{
            print("ending function with result " + function.result)
            print("aspect called: " + counter + "times")
        }
}
doSomething()

//output:
// starting function
// hello world
// ending function
```

```jsx
sayHello(x: string) {
	print("hello " + x)
}

aspect prepareSay(sayHello){
	 before{
        print("Will call function " + function.name + " with arguments: ");
        for arg in function.args {
            print(arg.value)
        }
    }
}

sayHello("Alice")
//output:
// Will call function sayHello with arguments: Alice
// hello Alice
```

---

---

EBNF

```jsx
program              = { function_definition | aspect_definition } ;

function_definition  = identifier, "(", [ parameters ], ")", [ type ], block ;

parameters           = identifier, ":", type, { ",", identifier, ":", type } ;

type                 = "int"
                     | "float"
                     | "str"
                     | "bool";
                     
block                = "{", {statement}, "}" ;

statement            = variable_declaration
                     | if_statement
                     | loop_statement
                     | for_each_statement
                     | assign_or_call
                     | return_statement ;

variable_declaration = type, identifier, "=", expression ;

assign_or_call       = identifier, ( "(", arguments, ")"  |  "=", expression ) ;

if_statement         = "if", expression, block, { "elif", expression, block }, ["else", block] ;

loop_statement       = "while", expression, block ;

for_each_statement   = "for", idientifier, "in", expression, block ;

return_statement     = "return", [ expression ] ;

arguments            = [ expression, {",", expression } ] ;

expression           = conjunction, { "||", conjunction } ;

conjunction          = relation_term, { "&&", relation_term } ;

relation_term        = additive_term, [ relation_operator, additive_term ] ; 

relation_operator    = ">="
                     | ">"
                     | "<="
                     | "<"
                     | "=="
                     | "is"
                     | "!=" ;
                     
additive_term        = multiplicative_term, { ("+" | "-"), multiplicative_term } ;

multiplicative_term  = unary_application, { ("*" | "/"), unary_application } ; 

unary_application    = [ ("-" | "!") ], casting ;

casting              = term, [ "->", type ] ;

term                 = integer
                     | float
                     | bool
                     | string
                     | object_access
                     | "(" , expression , ")" ;
                                          
object_access = identifier_or_call, {".", identifier_or_call}

identifier_or_call   = identifier, ["(", arguments, ")"]
                                          
aspect_definition    = "aspect", identifier, "(", (identifier | string) {"," (identifier | string), ")", aspect_block;

aspect_block         = "{", { variable_declaration }, aspect_member "}" ;

aspect_members       = ( before_statement, [ after_statement ] ) |  after_statement) ;

before_statement     = "before", block ;

before_statement     = "after", block ;

identifier           = letter , { letter | digit | "_" } ;

float                = integer , "." , digit , { digit } ;

integer              = "0" | positive_digit , { digit } ;

string               = '"' , { literal } , "\n" '"' ;

comment              = "//", { literal | '"' } ;

literal              = letter
                     | digit
                     | symbols ;
                     
*letter              = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;
*positive_digit      = "1" | "2" | ... | "9" ;
*digit               = "0" | "1" | ... | "9" ;
*bool                = "true" | "false" ;
*symbols             = "`" 
                     | "~" 
                     | "!" 
                     | "@" 
                     | "#" 
                     | "$" 
                     | "%" 
                     | "^" 
                     | "&" 
                     | "*" 
                     | "(" 
                     | ")" 
                     | "_" 
                     | "-" 
                     | "+" 
                     | "=" 
                     | "{"
                     | "}" 
                     | "[" 
                     | "]" 
                     | ";" 
                     | ":" 
                     | "'" 
                     | "," 
                     | "." 
                     | "?" 
                     | "/" 
                     | "|" 
                     | "\" 
                     ;

```

## Dane wejściowe strumienie/pliki

Program napisany w Parasite może zostać uruchomiony ze strumienia oraz z pliku.

Uruchomienie programy ze strumienia danych obsługuje wszystkie bajty jako program do interpretacji, aż do wystąpienia znaku ETX.

Język dostarcza narzędzia do przesyłania danych na standardowe wyjście - funkcja print().

Co oznacza, że interpreter posiada dostęp do standardowego wejścia i wyjścia.

## Obsługa błędów

```jsx
// format błędów
<Severity>: <message>; [<line>:<column>]
```

```jsx
// przykład niezdefiniowana zmienna

main(){
	print("hi" + a)
}
```


Error: Couldn't find [a] in scope, declare it first; [2:15]
```

---

```jsx
// przykład niepoprawnego przypisania do zmiennej

main(){
	int a = 10
	a = "hi"
}
```

```jsx
Error: Cannot assign to variable of type [int]; [3:2]
```

---

```jsx
// przykład próby dodania wartości o różnych typach
main() {
  int a = 10 + "5"
}
```

```jsx
Error: Couldn't create [AddExpresion] expression, expression should be of type [int, float]; [2:14]
```

---


```jsx
// przykład zdefiniowania aspektu, bez podanych argumentów

aspect logSomething(){
	before{
		print("before")
	}
} 
```

```jsx

Warning: Aspect not attached to any function; [5:21]
```

---

```jsx
// przykład zdefiniowania aspektu bez before lub after

aspect logSomething(someFunction){
	int counter = 0
}
```

```jsx
Error: Aspect must have at least 'before' or 'after' declaration; [7:1]
```

```jsx
// przykład dwa razy zdefiniowanej funkcji main

main(){
	print("hi")
}

main(){
	print("hello")
}
```

```jsx
Error: Function redefinition, function name: [main]; [5:1]
```

---

## Uruchomienie

Uruchomienie programu z pliku (wyjście standardowe)

```jsx
python main.py nazwapliku
Hello world!
```

Uruchomienie programu ze strumienia (wyjście standardowe)
```jsx
// jeszcze nie udalo sie zrobić
```

## Tokeny

Operatory relacyjne:

- EQUALS (==)
- NOT_EQUALS (!=)
- GREATER (>)
- GREATER_EQUAL (>=)
- LESS (<)
- LESS_EQUAL (<=)

Operatory arytmetyczne:

- PLUS (+)
- MINUS (-)
- MULTIPLY (*)
- DIVIDE (/)

Operatory logiczne:

- AND (and)
- OR (or)
- NEGATE(!)
- IS (is)

Parantheses:

- PAREN_OPEN (()
- PAREN_CLOSE ())
- BRACE_OPEN ({)
- BRACE_CLOSE (})

Słowa kluczowe:

- WHILE
- FOR_EACH
- IN
- IF
- ELSE
- ASPECT
- BEFORE
- AFTER
- RETURN

Komenatrz:

- COMMENT

Identyfikatory (zmiennych/funkcji/aspektu):

- IDENTIFIER

Typy danych:

- INTEGER
- FLOAT
- STRING
- BOOL
- TYPE (nie jestem pewien)

Symbole specjalne:

- COMMA (,)
- COLON (:)
- ASSIGNMENT (=)
- CAST (→)
- EXT

## **Konwersja typów w tabelce i jaka kombinacja typów jest akceptowalna dla operatorów
wieloargumentowych i funkcji wbudowanych**

| Z/DO | INTEGER | FLOAT | STRING | BOOLEAN |
| --- | --- | --- | --- | --- |
| INTEGER | - | Explicit | Explicit | Explicit |
| FLOAT | Explicit | - | Explicit | Explicit |
| STRING | - | - | - | Explicit |
| BOOLEAN | Explicit | Explicit | Explicit | - |

```jsx
// przykład konwersji typu int -> float
int a = 3
float b = a -> float
print(b)
print(a -> float)

// output:
// 3.0
// 3.0
```

W przypadkach konwersji na boolean:

- pusty string “” oznacza `false`
- niepusty string oznacza `true`
- int/float 0 oznacza `false`
- inny int/float oznacza `true`


## Opis realizacji modułów

1. Analizator leksykalny

Jako wejście analizator leksykalny przyjmuje kod źródłowy programu a następnie go przetwarza, na wynikające z gramatyki tokeny. 

Tokeny powiązane są z wartościami.

Tokeny przechowują także informacje o swoim położeniu w kodzie źródłowym - w postaci (nr linii, nr kolumny).

W przypadku gdy lekser natrafi na niemożliwy do zdekodowania ciąg znaków analizator skanuje go aż do natrafienia na biały znak i przerywa działanie.

1. Analizator składniowy 

Parser jako wejście przyjmuje strumień tokenów zwracany przez lekser. Lekser jest obiektem analizatora leksykalnego. 

Parser produkuje drzewo rozbioru składniowego programu `AST`.

Na podstawie podanych tokenów, oczekuje na tokeny określonego typu.

W przypadku natrafienia na nieścisłość, analizator, rzuca wyjątkiem, który zawiera informacje o położeniu niepoprawnego kawałka kodu.

2. Analizator semantyczny

Analizator semantyczny operuje na drzewie AST zwracanym przez parser. 

Kontroluje “poprawność” (sens) analizowanego kodu.



Sprawdza: 

- czy program zawiera wymaganą funkcję `main`
- wszystkie odwołania do zmiennych (czy istnieją i zostały poprawnie użyte - sprawdzenie typu)
- kontrola typów

W przypadku natrafienia na nieścisłość analizator rzuca wyjątkiem, który zawiera informacje o położeniu niepoprawnego kawałku kodu, jeśli trzeba wypisuje też odpowiedni identyfikator.

1. Interpreter

Interpreter również działa na drzewie AST, działa dopiero gdy analiza semantyczna zakończy się powodzeniem. 

Interpreter odwiedza elementy drzewa składniowego, ewaluując ich zawartość. Nadaje wartości zmiennym, sprawdza zgodność typów, zgodność podawanych do wywołań argumentów, uruchamia wywoływane funkcje i aspekty.

Wykonuje operacje arytmetyczne, obsługuje instrukcje warunkowe, pętle, wywołania funkcji oraz inne konstrukcje językowe.

Dba o to aby wywołania rekurencyjnie nie przekroczyly zdefiowanego limitu (implementacja za pomocą CallStack).

## Testy

Testy sprawdzają poprawność działania różnych komponentów systemu, takich jak skaner, analizator leksykalny, parser i interpreter.
Każdy z modułów zawiera testy jednostkowe oraz bardziej złożone


