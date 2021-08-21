create table if not exists Employee (
	ID serial primary key,
	Name varchar(40) not null,
	Department varchar(80),
	Chief_ID integer references Employee(ID) not null,
	check(Chief_ID != ID)
);