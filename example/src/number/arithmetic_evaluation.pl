
% ARITHMETIC EVALUATION

/***
	@descr This file contains all predicates needed to evaluate arithmetic
	expressions between real numbers, where the result of operating
	two rational numbers is another rational number.
	
	For example, the
	result of 2/3 + 4/5 is not given as 1.46667, but as 22/15.
	
	
	A file description can also contain bullet lists:
	
	
	<++
	!> Actually, any description can contain lists.
		<++
			!> File descriptions
			
			
			
			!> Predicate separators
			!> Also in predicates:
			<++
				!> In their description
				!> In the description of the constraints
				!> In the description of each parameter (see ?expr_eval/2)
				
				!> Notice that some bullets have a blank line on top
			++>
			
			!> Included this one (this is due to the separation in the
			documentation)
		++>
	!> Write the coolest documentation using verbatim environments!
		<--
		This
					 is
			   a
		verbatim
										  environment
		-->
		
		
		
	++>
	
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
	
	Using a closing verbatim environment '-->' without the opening verbatim
	environment does not affect at all the generation of documentation.
	
	
	@Result is the evaluation of @Expr.
	
		@param Expr Must be an arithmetic expression.
		Either one of the following possibilities:
		<++
		!> A + B
		!> A - B
		!> ...
		++>
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
