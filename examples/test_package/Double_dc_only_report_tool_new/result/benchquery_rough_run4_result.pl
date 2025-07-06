% generated: 17 November 1989
% option(s): SOURCE_TRANSFORM_1
%
% query
%
% David H. D. Warren
% Copyright: Public domain
%
% query population and area database to find countries of approximately equal population density. 
density(Country, Density) :- pop(Country, Pop), area(Country, Area), Area > 0, Density is Pop / Area. similar_density(D1, D2) :- Ratio is D1 / D2, Ratio >= 0.95, Ratio =< 1.05. query_pop([Country1, Density1, Country2, Density2]) :- density(Country1, Density1), density(Country2, Density2), Country1 \= Country2, similar_density(Density1, Density2).
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
Report: The generated code introduces a new approach to finding countries with similar population densities by using a ratio-based comparison (within 5% difference) instead of the original fixed multiplication factors. While the logic is different, it still achieves the goal of finding countries with approximately equal population densities. The generated code is valid and meets the requirements, but the results differ slightly due to the different comparison methods. The original code uses integer division and fixed multipliers, while the generated code uses floating-point division and a ratio range.
*/