
DROP DATABASE if exists utaka;
create database utaka;
use utaka;

CREATE TABLE user (
	userid SERIAL PRIMARY KEY,
	username VARCHAR(64) NOT NULL UNIQUE,
	accesskey VARCHAR(40) UNIQUE,
	secretkey VARCHAR(40) UNIQUE
) ENGINE=InnoDB;

insert into user(username, accesskey, secretkey) values('UTAKA_ALL_USERS', '', '');
insert into user(username, accesskey, secretkey) values('UTAKA_AUTHENTICATED_USERS', null, null);
insert into user(username, accesskey, secretkey) values('andrew', 'access', 'secret');

CREATE TABLE bucket (
	userid BIGINT UNSIGNED NOT NULL,
	bucket VARCHAR(32) PRIMARY KEY NOT NULL,
	bucket_creation_time DATETIME,
	FOREIGN KEY (userid) REFERENCES user(userid)
) ENGINE=InnoDB;

CREATE TABLE object (
	userid BIGINT UNSIGNED NOT NULL,
	object VARCHAR(64) NOT NULL,
	bucket VARCHAR(32) NOT NULL,
	hashfield blob,
	object_create_time DATETIME,
	eTag VARCHAR(32),
	object_mod_time DATETIME,
	content_type VARCHAR(32) DEFAULT 'binary/octet-stream',
	content_disposition VARCHAR(64),
	content_encoding VARCHAR(32),
	size INT UNSIGNED,
	PRIMARY KEY(object, bucket),
	FOREIGN KEY(userid) REFERENCES user(userid),
	FOREIGN KEY(bucket) REFERENCES bucket(bucket)
) ENGINE=InnoDB;

CREATE TABLE bucket_permission (
	userid BIGINT UNSIGNED NOT NULL,
	bucket VARCHAR(32) NOT NULL,
	permission ENUM('read', 'write', 'read_acp', 'write_acp') NOT NULL,
	PRIMARY KEY(userid, bucket, permission),
	FOREIGN KEY(userid) REFERENCES user(userid),
	FOREIGN KEY(bucket) REFERENCES bucket(bucket)
) ENGINE=InnoDB;

#CREATE INDEX bucketPermIndex ON bucket_permission(userid, bucket);

CREATE TABLE object_permission (
	userid BIGINT UNSIGNED NOT NULL,
	bucket VARCHAR(32) NOT NULL,
	object VARCHAR(64) NOT NULL,
	permission ENUM('read', 'read_acp', 'write_acp') NOT NULL,
	PRIMARY KEY(userid, bucket, object, permission),
	FOREIGN KEY(userid) REFERENCES user(userid),
	FOREIGN KEY(bucket) REFERENCES bucket(bucket),
	FOREIGN KEY(object) REFERENCES object(object)
) ENGINE=InnoDB;

#CREATE INDEX objectPermIndex ON object_permission(userid, bucket, object);

CREATE TABLE object_metadata (
	bucket VARCHAR(32) NOT NULL,
	object VARCHAR(64) NOT NULL,
	type VARCHAR(64) NOT NULL,
	value VARCHAR(64) NOT NULL,
	PRIMARY KEY(bucket, object, type, value),
	FOREIGN KEY(bucket) REFERENCES bucket(bucket),
	FOREIGN KEY(object) REFERENCES object(object)
) ENGINE=InnoDB;

#CREATE INDEX objectDataIndex ON object_metadata(bucket, object);
