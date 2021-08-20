psql -U postgres
create database netology_music;
create user netology_dj with password 'xxxxx';
alter database netology_music owner to netology_dj;
\l
\q
psql -U netology_dj -d netology_music
create table if not exists Genre (
	ID serial primary key,
	Name varchar(40) not null
);
create table if not exists Artist (
	ID serial primary key,
	Name varchar(40) not null,
	Genre_ID integer references Genre(ID) not null
);
create table if not exists Album (
	ID serial primary key,
	Name varchar(40) not null,
	Release_year integer
);
create table if not exists Track (
	ID serial primary key,
	Name varchar(40) not null,
	Duration numeric(3,2),
	Album_ID integer references Album(ID)
);
\d+ Artist
alter table Artist drop column Genre_ID;
\d+ Album
alter table Album drop column Artist_ID;

create table if not exists Collection (
	ID serial primary key,
	Name varchar(40) not null,
	Release_year integer
);
\dt
create table if not exists ArtistGenre (
	Artist_ID integer references Artist(ID) not null,
	Genre_ID integer references Genre(ID) not null,
	constraint pk1 primary key (Artist_ID, Genre_ID)
);
create table if not exists ArtistAlbum (
	Artist_ID integer references Artist(ID) not null,
	Album_ID integer references Album(ID) not null,
	constraint pk2 primary key (Artist_ID, Album_ID)
);
Create table if not exists TrackCollection (
	Track_ID integer references Track(ID) not null,
	Collection_ID integer references Collection(ID) not null,
	constraint pk3 primary key (Track_ID, Collection_ID)
);