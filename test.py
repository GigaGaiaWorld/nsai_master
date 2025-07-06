model = """
digit(img_1,1).
digit(img_2,2).
digit(img_3,3).
digit(img_4,4).
digit(img_5,5).
digit(img_6,6).
langda(LLM:"digit 7, it as a probability of 0.8", FUP:"false").
digit(img_8,8).
digit(img_9,9).
digit(img_0,0).

number([],Result,Result).
number([H|T],Acc,Result) :- digit(H,Nr), Acc2 is Nr+10*Acc,number(T,Acc2,Result).
number(X,Y) :- number(X,0,Y).

0.8::langda(LLM:"define multi_addition(X,Y,Z), it's logic is: number(X,X2), number(Y,Y2), Z is X2+Y2.",FUP:"false").

query(multi_addition([img_7,img_9],[img_3,img_1,img_2],Z)).
"""

from langda import langda_solve
model_langda = langda_solve('double_dc',model)

from problog.program import PrologString
from problog import get_evaluatable
evaluatable = get_evaluatable().create_from(PrologString(model_langda))
results = evaluatable