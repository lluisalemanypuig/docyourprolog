
% ARITHMETIC EVALUATION

/***
	@descr This file contains all predicates needed to evaluate arithmetic
	expressions between real numbers, where the result of operating
	two rational numbers is another rational number.
	
	For example, the
	result of 2/3 + 4/5 is not given as 1.46667, but as 22/15.
	
	
	A file description can also contain bullet lists:
	
	
	\blist
		\item Actually, any description can contain lists.
		\blist
			\item File descriptions
			
			
			
			\item Predicate separators
			\item Also in predicates:
			\blist
				\item In their description
				\item In the description of the constraints
				\item In the description of each parameter (see ?expr_eval/2)
				
				\item Notice that some bullets have a blank line on top
			\elist
			
			\item Included this one (this is due to the separation in the
			documentation)
		\elist
		
		\item Write the coolest documentation using verbatim environments!
		\bverbatim
		This
					 is
			   a
		verbatim
										  environment
		\everbatim
		
		
		
	\elist
	
	@author Me, Myself, and I
	@date July 20th, 2018
*/

/**
	@form expr_eval(Expr, Result)
	@descr @Expr is an arithmetic expression. That is, @Expr is either
	a natural value, or an arithmetic expression of the form
	\bverbatim
		A + B
		A - B
		A*B
		A/B
		A^B
		-A
	\everbatim
	where A and B are arithmetic expressions.
	
	Using a closing verbatim environment '\everbatim' without the opening verbatim
	environment does not affect at all the generation of documentation.
	
	@Result is the evaluation of @Expr.
	
	@constrs
		@param Expr Must be an arithmetic expression.
		Either one of the following possibilities:
		\blist
		\item A + B
		\item A - B
		\item ...
		\elist
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
