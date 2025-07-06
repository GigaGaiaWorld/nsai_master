% Your model here
% Earth constant
meter_per_degree(111194.93).
 % R * π / 180 ≈ 111194.93 meters/degree
user_location(49.87500, 8.65639).
special_zone_location(49.873094, 8.658995).
relative_offset(NorthOffset, EastOffset) :-
 user_location(UserLat, UserLon), special_zone_location(ZoneLat, ZoneLon), meter_per_degree(MetersPerDegree), NorthOffset is (ZoneLat - UserLat) * MetersPerDegree, EastOffset is (ZoneLon - UserLon) * MetersPerDegree * cos(UserLat * pi / 180).
query(relative_offset(NorthOffset, EastOffset)).
query(user_location(North, East)).
/* %%% Result %%% 
% Problog Inference Result：
relative_offset(-211.93753657979838,186.67530947625767) = 1.0000
user_location(49.875,8.65639) = 1.0000
*/