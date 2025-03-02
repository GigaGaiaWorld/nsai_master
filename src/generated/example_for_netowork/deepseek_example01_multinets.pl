event_temperature_exceed(Sensor) :- 
    sensor_data(Sensor, temperature, _, _, _, Mean, _, _, _, _), Mean > 26.

event_cpu_high_utilization(Sensor) :- 
    sensor_data(Sensor, cpuload, _, _, _, Mean, _, _, _, _), Mean > 0.75.

event_temperature_low(Sensor) :- 
    sensor_data(Sensor, temperature, _, _, _, Mean, _, _, _, _), Mean < 24.

event_humidity_high(Sensor) :- 
    sensor_data(Sensor, humidity, _, _, _, Mean, _, _, _, _), Mean > 0.85.

event_temperature_difference_large(Sensor1, Sensor3) :- 
    sensor_data(Sensor1, temperature, _, _, _, Mean1, _, _, _, _),
    sensor_data(Sensor3, temperature, _, _, _, Mean3, _, _, _, _), 
    Diff is abs(Mean1 - Mean3), Diff > 2.0.


nn(overheat_net, [event_temperature_exceed, event_cpu_high_utilization], Overheat, [yes, no]) :: anomaly(overheat_risk, Overheat) :- 
    event_temperature_exceed(sensor_KMS1),
    event_cpu_high_utilization(sensor_cpu).

nn(conden_net, [event_temperature_low, event_humidity_high], Condensation, [yes, no]) :: anomaly(condensation_risk, Condensation) :- 
    event_temperature_low(sensor_KMS1),
    event_humidity_high(sensor_weather).

nn(high_pow_net, [event_temperature_difference_large], HighPower, [yes, no]) :: anomaly(high_power_consumption, HighPower) :- 
    event_temperature_difference_large(sensor_KMS1, sensor_weather).

