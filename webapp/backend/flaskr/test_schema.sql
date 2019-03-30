set FOREIGN_KEY_CHECKS=0;
drop table if exists user;
drop table if exists books;
drop table if exists reviews;
set FOREIGN_KEY_CHECKS=1;

create table user (
  id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username TEXT NOT NULL,
  password TEXT not null
);

create table books (
 id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
 title text not null,
 author TEXT NOT NULL,
 isbn TEXT NOT NULL,
 cover TEXT NOT NULL,
 description TEXT NOT NULL,
 average_review FLOAT NOT NULL,
 purchase_link TEXT NOT NULL,
 date_published DATE
);

create table reviews (
  id integer not null auto_increment primary key,
  book_id int(10) not null,
  foreign key(book_id) references books(id),
  critic boolean default false,
  rating integer default 0,
  text text,
  date_published date
);

load data local infile 'tests/seedbookdata.csv' into table books fields terminated by ',' lines terminated by '\n';

