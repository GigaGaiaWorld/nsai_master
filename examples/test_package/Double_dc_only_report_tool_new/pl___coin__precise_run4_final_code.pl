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
/* %%% Result %%% 
Error evaluating Problog model:
    return self.collapse(string, tokens)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/zhenzhili/miniforge3/envs/langda/lib/python3.11/site-packages/problog/parser.py", line 1282, in collapse
    raise UnmatchedCharacter(string, expr_stack[-1].start.location)
problog.parser.UnmatchedCharacter: Unmatched character '(' at 7:3.
*/