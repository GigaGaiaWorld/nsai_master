PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
if(coin(CNT),
        (NewSC is SC + 1,
         NewCNT is CNT - 1,
         coins_r(NewSC,S,NewCNT)),
        (NewCNT is CNT - 1,
         coins_r(SC,S,NewCNT))
.
total(S) :- coins_r(0,S,4).
query(total(_)).

/* Result Report:
Validity_form: False
Validity_result: False
Report: The generated code is not valid due to a syntax error. The 'if' construct is incorrectly used and lacks proper parentheses, causing a parsing error. The original code uses a disjunction (;) for conditional branching, which is correct in Prolog. The generated code fails to maintain this logic and introduces invalid syntax. Both the form and result validity are false because the code cannot run and thus cannot produce results consistent with the original.
*/