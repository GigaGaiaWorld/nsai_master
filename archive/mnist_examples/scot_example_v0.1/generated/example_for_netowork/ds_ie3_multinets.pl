% nn predicates remain unchanged:
nn(temp_net, [Mean_value], Output_Prob)::sensor_data(sensor_KMS1, temperature, Mean_value, Output_Prob).
nn(cpul_net, [Mean_value], Output_Prob)::sensor_data(sensor_cpu, cpu_load, Mean_value, Output_Prob).
nn(humi_net, [Mean_value], Output_Prob)::sensor_data(sensor_weather, humidity, Mean_value, Output_Prob).

event_temperature_exceed(Temp, Output_Prob) :- 
    sensor_data(_, temperature, Temp, Output_Prob), Temp > 26.

event_temperature_low(Temp, Output_Prob) :- 
    sensor_data(_, temperature, Temp, Output_Prob), Temp < 24.

event_cpu_high_utilization(CPU, Output_Prob) :- 
    sensor_data(_, cpu_load, CPU, Output_Prob), CPU > 0.75.

event_humidity_high(Humi, Output_Prob) :- 
    sensor_data(_, humidity, Humi, Output_Prob), Humi > 0.85.

anomaly_heat(Temp, CPU, Output_Prob) :- 
    event_temperature_exceed(Temp, Output_Prob1),
    event_cpu_high_utilization(CPU, Output_Prob2),
    Output_Prob is 1 - (1 - Output_Prob1) * (1 - Output_Prob2).

anomaly_cond(Temp, Humi, Output_Prob) :- 
    event_temperature_low(Temp, Output_Prob1),
    event_humidity_high(Humi, Output_Prob2),
    Output_Prob is 1 - (1 - Output_Prob1) * (1 - Output_Prob2).

anomaly(Temp, CPU, Humi, Prob_final) :-
    anomaly_heat(Temp, CPU, Output_Prob1),
    anomaly_cond(Temp, Humi, Output_Prob2),
    Prob_final is 1 - (1 - Output_Prob1) * (1 - Output_Prob2).
