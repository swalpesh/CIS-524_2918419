# CIS 524 -- Spring 2026

## Programming Assignment

**Student Name:** Swalpesh Kotalwar\
**CSU ID:** 2918419

------------------------------------------------------------------------

# Project Overview

This project implements a top-down recursive descent interpreter in
Python for a simple programming language defined in the CIS 524 project
specification.

The interpreter:

-   Reads a `.tiny` input file from the command line
-   Performs lexical analysis (tokenization)
-   Parses according to the given grammar
-   Evaluates expressions during parsing
-   Prints the result of each valid `let-in-end` block
-   Prints `Error` for invalid blocks
-   Continues execution even after encountering errors

------------------------------------------------------------------------

# Program Structure

## Lexer

The Lexer class:

-   Converts input text into tokens
-   Recognizes keywords: let, in, end, int, real, if, then, else
-   Recognizes identifiers and numeric literals
-   Recognizes arithmetic and comparison operators
-   Ignores whitespace
-   Appends EOF token at the end

## Parser

The Parser class implements recursive descent parsing.

Each grammar rule corresponds to a function:

-   let_in_end()
-   decl_list()
-   decl()
-   type_rule()
-   expr()
-   term()
-   factor()
-   cond()
-   if_expr()

Expressions are evaluated during parsing.

------------------------------------------------------------------------

# Type Handling

The language supports:

-   int
-   real

Features implemented:

-   Explicit casting: int(x), real(x)
-   Proper type conversion during assignment
-   Correct return type for each block

------------------------------------------------------------------------

# Symbol Table

A dictionary is used to store variables:

variable_name -\> (type, value)

The symbol table resets for every new let block, ensuring proper
scoping.

------------------------------------------------------------------------

# Error Handling

The interpreter prints:

Error

when:

-   Syntax errors occur
-   Undeclared variables are used
-   Type mismatches occur
-   Grammar rules are violated

If one block fails, execution continues to the next block.

------------------------------------------------------------------------

# How to Run

From terminal:

python3 parser_2918419.py sample2.tiny

Example output:

20 
314.16 
0.25

Example with error:

48.0 
Error

------------------------------------------------------------------------

# Features Implemented

-   Top-down recursive descent parsing
-   Lexical analysis using regular expressions
-   Symbol table with scoped variables
-   Integer and real types
-   Explicit type casting
-   Arithmetic operations with correct precedence
-   Conditional expressions (if-then-else)
-   Comparison operators
-   Multiple let blocks
-   Robust error handling

------------------------------------------------------------------------

# Conclusion

This project demonstrates the implementation of a complete recursive descent interpreter in Python. The interpreter strictly follows the given grammar, evaluates expressions correctly with proper precedence, handles scoped symbol tables, and provides robust error handling while continuing execution across multiple blocks.

All project requirements have been successfully implemented.
