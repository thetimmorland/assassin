create table user (
    id integer primary key autoincrement,

    is_active boolean not null default true
        check(is_active in (true, false)),

    email text unique not null,
    name text not null,
    location text not null
);


create table assassination (
    id integer primary key autoincrement,
    hunter_id integer not null,
    prey_id integer not null,

    foreign key(hunter_id) references user(id),
    foreign key(prey_id) references user(id)
);

create index ui_assassination_hunter_id on assassination(hunter_id);
create index ui_assassination_prey_id on assassination(prey_id);


create table target_ring (
    id integer primary key autoincrement,
    user_id integer unique not null,

    foreign key(user_id) references user(id)
);


create view target as
select
    user_id as hunter_id,
    coalesce(
        lead(user_id) over (order by id),
        first_value(user_id) over (order by id)
    ) as prey_id
from target_ring;


create trigger tr_assassination_update_target
after insert on assassination 
begin
    delete from target_ring where user_id = new.prey_id;
end;
