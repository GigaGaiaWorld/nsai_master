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

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is correct and consistent with the original code. Both codes implement the insertion sort algorithm in Prolog, with identical logic and structure. The only differences are in variable naming (e.g., 'H' vs 'Head', 'T' vs 'Tail', 'insert_element' vs 'insert'), which do not affect functionality. The running results of both codes are identical, producing the same sorted list.
*/