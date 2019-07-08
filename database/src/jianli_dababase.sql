USE jianlila;

CREATE TABLE users (
	id   			int(10)      UNSIGNED NOT NULL AUTO_INCREMENT ,
	username 		varchar(40)  NOT NULL ,
	password 		varchar(128) NOT NULL ,
	email   		varchar(255) NOT NULL ,
	first_name   	varchar(40)  NOT NULL ,
	last_name   	varchar(40)  NOT NULL ,
	isadmin 		tinyint(1)   NOT NULL ,
	PRIMARY KEY (id) ,
	UNIQUE KEY username (username, email)
) ENGINE = MYISAM DEFAULT CHARSET = utf8;

CREATE TABLE educations (
	id 				int(10)		 UNSIGNED NOT NULL AUTO_INCREMENT ,
	user_id 		int(10)		 UNSIGNED NOT NULL ,
	school 			varchar(40)  NOT NULL ,
	degree 			varchar(40)  NOT NULL ,
	Study           varchar(128) NOT NULL ,	
	in_date         date         NOT NULL ,
	out_date        date         NOT NULL ,
	description     text 		 DEFAULT NULL ,
	PRIMARY KEY (id) 
) ENGINE = MYISAM DEFAULT CHARSET = utf8;

CREATE TABLE books (
	id 				int(10)		 UNSIGNED NOT NULL AUTO_INCREMENT ,
	user_id 		int(10)		 UNSIGNED NOT NULL ,
	bookname        varchar(40)  NOT NULL ,
	pubdate			date         NOT NULL ,
	description     text 		 DEFAULT NULL ,
	PRIMARY KEY (id) 
) ENGINE = MYISAM DEFAULT CHARSET = utf8;

CREATE TABLE experiences (
	id 				int(10)		 UNSIGNED NOT NULL AUTO_INCREMENT ,
	user_id 		int(10)		 UNSIGNED NOT NULL ,
	company 		varchar(128) NOT NULL ,
	title 			varchar(128) NOT NULL ,
	in_date         date         NOT NULL ,
	out_date        date         NOT NULL ,
	description     text 		 DEFAULT NULL ,
	PRIMARY KEY (id) 

) ENGINE = MYISAM DEFAULT CHARSET = utf8;

CREATE TABLE skills (
	id 				int(10)		 UNSIGNED NOT NULL AUTO_INCREMENT ,
	user_id 		int(10)		 UNSIGNED NOT NULL ,
	skillname       varchar(40)  NOT NULL ,
	level           varchar(40)  NOT NULL ,
	PRIMARY KEY (id) 
) ENGINE = MYISAM DEFAULT CHARSET = utf8;

CREATE TABLE resumes (
	id 				int(10)		 UNSIGNED NOT NULL AUTO_INCREMENT ,
	user_id 		int(10)		 UNSIGNED NOT NULL ,
	resume_name     varchar(128) NOT NULL ,
	email   		varchar(255) NOT NULL ,
	first_name   	varchar(40)  NOT NULL ,
	last_name   	varchar(40)  NOT NULL ,
	educations      varchar(255) DEFAULT NULL ,
	experiences     varchar(255) DEFAULT NULL ,
	skills          varchar(255) DEFAULT NULL ,
	books           varchar(255) DEFAULT NULL ,
	objective		varchar(128) NOT NULL ,
	ispublic 		tinyint(1)   NOT NULL ,
	description     text 		 DEFAULT NULL ,	
	PRIMARY KEY (id) 
) ENGINE = MYISAM DEFAULT CHARSET = utf8;
