% generated: 17 November 1989
% option(s): SOURCE_TRANSFORM_1
%
% query
%
% David H. D. Warren
% Copyright: Public domain
%
% query population and area database to find countries of approximately equal population density. 
density(Country, Density) :- pop(Country, Pop), area(Country, Area), Density is Pop / Area. approximately_equal(Density1, Density2) :- Diff is abs(Density1 - Density2), Threshold is 0.05 * max(Density1, Density2), Diff =< Threshold. query_pop([Country1, Density1, Country2, Density2]) :- density(Country1, Density1), density(Country2, Density2), Country1 @< Country2, approximately_equal(Density1, Density2).
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
Validity_result: False
Report: The generated code introduces a new predicate 'approximately_equal' to check if two densities are within 5% of each other, which is a more flexible approach compared to the original code's fixed ratio check. However, the original code uses integer division (//) for density calculation, while the generated code uses floating-point division (/), leading to different density values. The results are similar in concept but differ numerically due to this change. The generated code is valid and meets the requirements, but the results are not numerically consistent with the original due to the division method change.
*/