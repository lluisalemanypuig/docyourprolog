
% ARITHMETIC EVALUATION

/***
	@descr This file contains all predicates needed to evaluate arithmetic
	expressions between real numbers, where the result of operating
	two rational numbers is another rational number. For example, the
	result of 2/3 + 4/5 is not given as 1.46667, but as 22/15.
	
	@author Me, Myself, and I
	@date July 20th, 2018
*/

/**
	@form expr_eval(Expr, Result)
	@constrs @Expr is an arithmetic expression. That is, @Expr is either
	a natural value, or an arithmetic expression of the form
	<--
		A + B
		A - B
		A*B
		A/B
		A^B
		-A
	-->
	where A and B are arithmetic expressions.
	
	@Result is the evaluation of @Expr.
*/
expr_eval(A + B, C):- expr_eval(A, AA), expr_eval(B, BB), C is AA + BB, !.
expr_eval(A - B, C):- expr_eval(A, AA), expr_eval(B, BB), C is AA - BB, !.
expr_eval(A*B, C):- expr_eval(A, AA), expr_eval(B, BB), C is AA*BB, !.
expr_eval(A/B, C):- expr_eval(A, AA), expr_eval(B, BB), C is AA/BB, !.
expr_eval(A^B, C):- expr_eval(A, AA), expr_eval(B, BB),C is AA^BB, !.
expr_eval(-A, C):- expr_eval(A, AA), C is -AA, !.
expr_eval(A, A).

/**
	@form factorial_(Num, F)
	@descr @F is the factorial of natural number @Num.
	@constrs
		@param Num A natural number.
*/
factorial_(0, 1):- !.
factorial_(N, F):- N1 is N - 1, factorial_(N1, F1), F is N*F1.
/**
	@form factorial(Expr, F)
	@descr @F is the factorial of the result of evaluating the arithmetic
	expression @Expr. Uses predicate ?factorial/2.
	@constrs
		@param Expr An arithmetic expression.
*/
factorial(E, F):- expr(E), expr_eval(E, N), natural(N), factorial_(N, F), !.
factorial(N, F):- natural(N), factorial_(N, F).
