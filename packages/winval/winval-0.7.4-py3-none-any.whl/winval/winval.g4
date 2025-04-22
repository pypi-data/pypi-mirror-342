grammar winval;

// parsing rules

constraint: expr EOF ;

expr:
    atom=INT                                   # IntExpr
    | atom=FLOAT                               # FloatExpr
    | atom=STRING                              # StringExpr
    | atom=BOOL                                # BoolExpr
    | atom=EMPTY_SET                           # EmptySetExpr
    | variable                                 # VariableExpr
    | struct=variable '[' key=expr ']'         # AccessExpr
    | '[' elements ']'                         # ListExpr
    | '{' elements '}'                         # SetExpr
    | '(' expr ')'                             # ParenExpr
    | op=('defined'|'len'|'prefix'|'suffix'|'basename'|'splitext'|'not') operand=expr # PrefixExpr
    | left=expr op=('+'|'-'|'*'|'/'|'**'|'%') right=expr     # InfixExpr
    | left=expr op='in' right=expr                           # InfixExpr
    | left=expr op=('|'|'&') right=expr                      # InfixExpr
    | left=expr op=('>'|'>='|'=='|'<='|'<'|'!=') right=expr  # InfixExpr
    | left=expr op=('or'|'and') right=expr                   # InfixExpr
    | left=expr op=('->'|'<->') right=expr                   # InfixExpr
;

variable: VARIABLE # VariableExpr2;

elements:
      (INT) ( ',' (INT) )*
      | (FLOAT) ( ',' (FLOAT) )*
      | (STRING) ( ',' (STRING) )*
      | (VARIABLE) ( ',' (VARIABLE) )*
      ;

// lexing rules
BOOL: 'True'|'False' ;
VARIABLE  : ('a'..'z' | 'A'..'Z' | '_' )+('a'..'z' | 'A'..'Z' | '0'..'9' | '_' )* ;
INT: '-'? [0-9]+ ;
FLOAT: '-'? [0-9]+ '.' [0-9]+ ;
EMPTY_SET: '{}' | 'set()' ;
STRING: '"' (~('"' | '\\' | '\r' | '\n'))* '"'
      | '\'' (~('\\' | '\r' | '\n' | '\''))* '\'';
WS   : [ \t]+ -> skip ;