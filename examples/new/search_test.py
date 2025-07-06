from langda import langda_solve

model3 = """
langda(LLM:"What was the weather yesterday in Darmstadt? rainy or sunny?", LOT:"search").

0.7::ground_wet_by_the_cleaner :- 
  langda(LLM:"According to the message from 
  cleaner: '/* Cleaner */', choose to be true or false.").
0.2::watering_splashed.

% Causation: Analyzing cause and effect based on above all informations
langda(LLM:"Figure out if the ground is wet or not", FUP:"false").

query(ground_wet).
"""
# result = langda_solve('double_dc',model3,'deepseek-chat',langda_ext={"Cleaner":"I wasn't there yesterday."}, query_ext="")
result = langda_solve('double_dc',model3,'deepseek-chat',langda_ext={"Cleaner":"I mopped the floor yesterday"}, query_ext="")

print(result)


"""
0.8::weather_yesterday(rainy).
0.2::weather_yesterday(sunny).
0.7::ground_wet_by_the_cleaner :- 
 true.
0.2::watering_splashed.
ground_wet :-
 weather_yesterday(rainy).
ground_wet :-
 ground_wet_by_the_cleaner.
ground_wet :-
 watering_splashed.
query(ground_wet).
"""