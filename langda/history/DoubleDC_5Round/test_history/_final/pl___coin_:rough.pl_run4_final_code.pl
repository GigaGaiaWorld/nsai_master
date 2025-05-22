PH::make_coin(C,PH).
coin(C) :- make_coin(C,0.8).
coins_r(SC,SC,0).
coins_r(SC,S,CNT) :-
 CNT > 0,
 
 (coin(CNT), NSC is SC + 1 ; \+ coin(CNT), NSC is SC), NCNT is CNT - 1, coins_r(NSC, S, NCNT).
total(S) :- coins_r(0,S,4).
query(total(_)).

*** Result:*** 
% Problog Inference Result：
total(4) = 0.4096
total(3) = 0.4096
total(2) = 0.1536
total(1) = 0.0256
total(0) = 0.0016 

***Report:***
Validity_form:True\Validity_result:True
The generated code is correct and consistent with the original code. The logic remains the same, with only minor syntactic differences such as variable renaming (SC2 to NSC, CNT2 to NCNT) and formatting changes. The generated code produces identical results to the original code, demonstrating equivalent functionality.