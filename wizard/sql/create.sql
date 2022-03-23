use dnd;
create table summons (id int not null, creature_type tinytext, health int not null, hit_modifier int not null, damage_modifier int not null, permanent boolean not null);