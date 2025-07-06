0.8::weather_yesterday(sunny); 0.2::weather_yesterday(rainy).
0.9::cleaner_fired.
% Causation: Analyzing cause and effect based on above all informations
ground_wet :- weather_yesterday(rainy).
query(ground_wet).
/* %%% Result %%% 
% Problog Inference Result：
ground_wet = 0.2000
*/