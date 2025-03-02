% nn predicates that convert features into probabilities:
nn(temp_net, [Start_timestamp, End_timestamp, Mean_value], Output_Prob)::sensor_data(sensor_KMS1, temperature, Start_timestamp, End_timestamp, Mean_value, Output_Prob).

nn(cpul_net, [Start_timestamp, End_timestamp, Mean_value], Output_Prob)::sensor_data(sensor_cpu, cpu_load, Start_timestamp, End_timestamp, Mean_value, Output_Prob).

nn(humi_net, [Start_timestamp, End_timestamp, Mean_value], Output_Prob)::sensor_data(sensor_weather, humidity, Start_timestamp, End_timestamp, Mean_value, Output_Prob).


event_temperature_exceed(Start_timestamp, End_timestamp, Temp, Output_Prob) :- 
    sensor_data(Sensor, temperature, Start_timestamp, End_timestamp, Temp, Output_Prob), Temp > 26.

event_temperature_low(Start_timestamp, End_timestamp, Temp, Output_Prob) :- 
    sensor_data(Sensor, temperature, Start_timestamp, End_timestamp, Temp, Output_Prob), Temp < 24.

event_cpu_high_utilization(Start_timestamp, End_timestamp, CPU, Output_Prob) :- 
    sensor_data(Sensor, cpu_load, Start_timestamp, End_timestamp, CPU, Output_Prob), CPU > 0.75.

event_humidity_high(Start_timestamp, End_timestamp, Humi, Output_Prob) :- 
    sensor_data(Sensor, humidity, Start_timestamp, End_timestamp, Humi, Output_Prob), Humi > 0.85.


anomaly_heat(Start_timestamp, End_timestamp, Temp, CPU, Output_Prob) :- 
    event_temperature_exceed(Start_timestamp, End_timestamp, Temp, Output_Prob),
    event_cpu_high_utilization(Start_timestamp, End_timestamp, CPU, Output_Prob).

anomaly_cond(Start_timestamp, End_timestamp, Temp, Humi, Output_Prob) :- 
    event_temperature_low(Start_timestamp, End_timestamp, Temp, Output_Prob),
    event_humidity_high(Start_timestamp, End_timestamp, Humi, Output_Prob).

anomaly(Start_timestamp, End_timestamp, Temp, CPU, Humi, Result):-
    anomaly_heat(Start_timestamp, End_timestamp, Temp, CPU, Output_Prob1),
    anomaly_cond(Start_timestamp, End_timestamp, Temp, Humi, Output_Prob2),
    Prob_final is 1 - (1 - Output_Prob1) * (1 - Output_Prob2),
    (Prob_final > 0.5 -> Result = 1 ; Result = 0).
