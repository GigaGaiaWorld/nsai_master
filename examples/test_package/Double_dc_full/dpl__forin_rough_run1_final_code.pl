insertion_sort([], []).
insertion_sort([Head|Tail], Sorted) :-
    insertion_sort(Tail, SortedTail),
    insert(Head, SortedTail, Sorted).
insert(Element, [], [Element]).
insert(Element, [Head|Tail], [Element, Head|Tail]) :-
    Element =< Head.
insert(Element, [Head|Tail], [Head|SortedTail]) :-
    Element > Head,
    insert(Element, Tail, SortedTail).
 
query(insertion_sort([3,1,2,5,7,12],X)).
/* %%% Result %%% 
% Problog Inference Result：
insertion_sort([3, 1, 2, 5, 7, 12],[1, 2, 3, 5, 7, 12]) = 1.0000
*/