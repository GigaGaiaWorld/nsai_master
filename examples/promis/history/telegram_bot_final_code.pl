% Your model here
% Earth constant
meter_per_degree(111194.93).
 % R * π / 180 ≈ 111194.93 meters/degree
user_location(49.87500, 8.65639).
special_zone_location(49.87495, 8.65941).
relative_offset(NorthOffset, EastOffset) :-
 user_location(UserLat, UserLon), special_zone_location(ZoneLat, ZoneLon), NorthOffset is (ZoneLat - UserLat) * 111194.93, LatRad is UserLat * pi / 180, EastOffset is (ZoneLon - UserLon) * 111194.93 * cos(LatRad).
query(relative_offset(NorthOffset, EastOffset)).
query(user_location(North, East)).
/* %%% Result %%% 
% Problog Inference Result：
relative_offset(-5.559746500184565,216.41437029481477) = 1.0000
user_location(49.875,8.65639) = 1.0000
*/