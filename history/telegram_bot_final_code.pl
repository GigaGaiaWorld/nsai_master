% Earth constant: R * π / 180 -> 111194.93 meters/degree
user_location(49.87500, 8.65639).
special_zone_location(49.877248, 8.65639).
relative_offset(NorthOffset, EastOffset) :-
 user_location(UserLat, UserLon), special_zone_location(ZoneLat, ZoneLon), NorthOffset is (ZoneLat - UserLat) * 111194.93, EastOffset is (ZoneLon - UserLon) * 111194.93 * cos(UserLat * pi / 180).
query(user_location(_,_)).
query(relative_offset(_,_)).
/* %%% Result %%% 
% Problog Inference Result：
user_location(49.875,8.65639) = 1.0000
relative_offset(249.9662026401759,0.0) = 1.0000
*/