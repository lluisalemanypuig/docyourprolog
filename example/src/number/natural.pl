/***
	@descr This file contains the basic definitions for what a natural
	number is, two constants (zero and one), 
*/

/**
	@form zero(Z)
	@descr Predicate fails if @Z is not 0.
*/
zero(0).
/**
	@form one(O)
	@descr Predicate fails if @O is not 1.
*/
one(1).

/**
	@form natural(N)
	@descr Predicates fails on any non-integer value, or negative
	integer value for parameter @N.
*/
natural(N):- integer(N), N >= 0.

/**
	@form next_natural(N)
	@descr Predicate used to generate all natural numbers.
	
	Example of usage: next_natural(N), write(N), nl, fail.
	@constrs
		@param N Natural value.
*/
next_natural(0).
next_natural(N):- next_natural(M), N is M + 1.

/**
	@form parity(Num, Par)
	@descr Obtains the parity of natural number @Num.
	
	\blist
	\item If @Num is even then @Par is "even".
	\item If @Num is odd then @Par is "odd".
	\elist
*/
parity(N, "even"):- 0 is N mod 2, !.
parity(_, "odd").
