/***
	@descr This file contains a number of high-order predicates for
	list manipulation, such as map, foldl, foldr, zip, ...
	@author Me, Myself and I
	@date 19th July 2018
*/

/**
	@form map(Function, List, NewList)
	@descr @NewList is the result of applying @Function to every element
	of List.
	
	In Haskell notation: map :: (a -> b) -> [a] -> [b]
*/
map(_, [], []):- !.
map(F, [X|L], [E|R]):- call(F, X, E), map(F, L, R), !.

/**
	@form zip(List1, List2, NewList)
	@constrs @List1 and @List2 must have the same length.
	@descr @NewList is the result of an element-wise pairing of the
	elements in @List1 and @List2. Each element of @NewList is a pair,
	where the left element is an element from @List1 and the right element
	is an element from @List2.
*/
zip([], [], []).
zip([A|L], [B|R], [(A, B)|S]):- zip(L, R, S).

/**
	@form zip(Function, List1, List2, NewList)
	@descr @NewList is the result of applying @Function to the
	i-th element of both @List1 and @List2.
	
	In Haskell notation: zip_with :: (a -> b -> c) -> [a] -> [b] -> [c]
	@constrs List1 and List2 must have the same length.
*/
zip_with(_,  [],  [],  []):- !.
zip_with(F, [A], [B], [X]):- call(F, A, B, X), !.
zip_with(F, [A|L], [B|R], [C|S]):- call(F, A, B, C), zip_with(F, L, R, S).
