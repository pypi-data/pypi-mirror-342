%{
#include <stdio.h>
%}

%%
"int"       { printf("Keyword: int\n"); }
"float"     { printf("Keyword: float\n"); }
"if"        { printf("Keyword: if\n"); }
"else"      { printf("Keyword: else\n"); }

[0-9]+      { printf("Literal: %s\n", yytext); }
[a-zA-Z_][a-zA-Z0-9_]*    { printf("Identifier: %s\n", yytext); }

"+"         { printf("Operator: +\n"); }
"-"         { printf("Operator: -\n"); }
"="         { printf("Operator: =\n"); }
";"         { printf("Punctuation: ;\n"); }
[ \t\n]+    { /* Skip whitespace */ }
.           { printf("Unknown character: %s\n", yytext); }
%%

int main() {
    yylex();  // Start lexical analysis
    return 0;
}


# int x = 5;
# float total = x + 10;


# to run 
# lex tokenizer.l
# gcc lex.yy.c -o lexer
# ./lexer


%{
#include <stdio.h>
%}

%%
"int"                       { printf("Keyword: int\n"); }
"float"                     { printf("Keyword: float\n"); }
"if"                        { printf("Keyword: if\n"); }
"else"                      { printf("Keyword: else\n"); }

[0-9]+                      { printf("Literal: %s\n", yytext); }
[a-zA-Z_][a-zA-Z0-9_]*      { printf("Identifier: %s\n", yytext); }

"=="                        { printf("Operator: ==\n"); }
"="                         { printf("Operator: =\n"); }
"!="                        { printf("Operator: !=\n"); }
"<="                        { printf("Operator: <=\n"); }
">="                        { printf("Operator: >=\n"); }
"<"                         { printf("Operator: <\n"); }
">"                         { printf("Operator: >\n"); }

"+"                         { printf("Operator: +\n"); }
"-"                         { printf("Operator: -\n"); }
"*"                         { printf("Operator: *\n"); }
"/"                         { printf("Operator: /\n"); }

";"                         { printf("Punctuation: ;\n"); }
","                         { printf("Punctuation: ,\n"); }
"("                         { printf("Punctuation: (\n"); }
")"                         { printf("Punctuation: )\n"); }

[ \t\r\n]+                  { /* Skip whitespace */ }
.                           { printf("Unknown character: %s\n", yytext); }
%%

int main() {
    printf("Enter input:\n");
    yylex();  // Start lexical analysis
    return 0;
}

int yywrap() {
    return 1;
}
