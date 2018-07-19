/***
	@descr This file contains a number of simple list-related simple
	predicates. Finding the minimum and maximum values in a list, sorting
	a list, dropping certain elements from a list, ...
*/

/**
	@form min(List, Min)
	@descr @Min is the smallest value, according to '@>', in @List.
	@constrs
		@param List Must have at least one element.
*/
min([X], X):- !.
min([X|L], M):- min(L, N), X @> N, !, M is N.
min([X|_], X).

/**
	@form max(List, Max)
	@descr @Max is the smallest value, according to '@<', in @List.
	@constrs
		@param List Must have at least one element.
*/
max([X], X):- !.
max([X|L], M):- max(L, N), X @< N, !, M is N.
max([X|_], X).

/**
	@form first(List, First, Rest)
	@descr @First is the head of @List and @Rest are the other elements
	of @List.
	@constrs
		@param List Must have at least one element.
*/
first([X], X, []):- !.
first([X|L], X, L).

/**
	@form last(List, Rest, Last)
	@descr @Last is the last element of @List. @Rest are the elements
	from the first to the second to last.
	@constrs
		@param List Cannot be empty.
*/
last([X], [], X):- !.
last([X|R], [X|K], L):- last(R, K, L).
