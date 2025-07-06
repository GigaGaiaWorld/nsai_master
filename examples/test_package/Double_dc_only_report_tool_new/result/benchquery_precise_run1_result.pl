% generated: 17 November 1989
% option(s): SOURCE_TRANSFORM_1
%
% query
%
% David H. D. Warren
% Copyright: Public domain
%
% query population and area database to find countries of approximately equal population density. 
query_pop([C1,D1,C2,D2]) :-
 
 
    density(C1,D1),
    density(C2,D2),
    C1 @< C2,
    20*D1 < 21*D2,
    20*D2 < 21*D1.
density(C,D) :-
 
 
    pop(C,P),
    area(C,A),
    D is (P*100) // A.
% populations in 100000's
pop(china,	8250).
pop(india,	5863).
pop(usa,	2119).
pop(indonesia,	1276).
pop(japan,	1097).
pop(brazil,	1042).
pop(bangladesh,	 750).
pop(pakistan,	 682).
pop(nigeria,	 613).
pop(mexico,	 581).
pop(uk,		 559).
pop(italy,	 554).
pop(france,	 525).
pop(philippines, 415).
pop(thailand,	 410).
pop(turkey,	 383).
pop(egypt,	 364).
pop(spain,	 352).
pop(poland,	 337).
pop(s_korea,	 335).
pop(iran,	 320).
pop(ethiopia,	 272).
pop(argentina,	 251).
% areas in 1000's of square miles
area(china, 3380).
area(india, 1139).
area(usa, 3609).
area(indonesia, 570).
area(japan, 148).
area(brazil, 3288).
area(bangladesh, 55).
area(pakistan, 311).
area(nigeria, 373).
area(mexico, 764).
area(uk, 86).
area(italy, 116).
area(france, 213).
area(philippines, 90).
area(thailand, 200).
area(turkey, 296).
area(egypt, 386).
area(spain, 190).
area(poland, 121).
area(s_korea, 37).
area(iran, 628).
area(ethiopia, 350).
area(argentina, 1080).
query(query_pop(_)).

/* Result Report:
Validity_form: True
Validity_result: True
Report: The generated code is mostly correct and consistent with the original code. It correctly implements the logic to find countries with approximately equal population density. The main differences are: 1) The generated code uses 'C1 @< C2' to avoid duplicate pairs, which is an improvement over the original. 2) The generated code simplifies the comparison logic by directly using '20*D1 < 21*D2' and '20*D2 < 21*D1' instead of calculating temporary variables. The running results are consistent, showing the same pairs of countries with similar densities, though the order of some pairs is reversed (e.g., [china, 244, france, 246] vs [france, 246, china, 244]).
*/