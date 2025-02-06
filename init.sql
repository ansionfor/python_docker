drop database if exists docker_demo;
create database docker_demo;

use docker_demo;

create table user_docker_list(
	`id` Int AUTO_INCREMENT COMMENT 'id',
	`user_id` BIGINT not null comment '用户id',
	`docker_id` char(12) not null comment 'docker id',
	`docker_type` tinyint not null default 1 comment 'docker 类型, mysql 1, redis 2',
	`db_info` json not null comment '数据库信息，host,user,pwd',
	`db_port` int not null comment '端口',
	`create_time` INT(11)      NOT NULL COMMENT '创建时间',
	`update_time` INT(11)      NOT NULL COMMENT '更新时间',
	`deleted`     TINYINT(4)   NOT NULL DEFAULT 0 COMMENT '是否删除 0未删除 1已删除',
	primary key (`id`),
	KEY `k_user_id` (`user_id`)
) engine = INNODB charset = utf8mb4 COLLATE utf8_general_ci COMMENT = '用户docker表';

create table config(
	`id` Int AUTO_INCREMENT COMMENT 'id',
	`name` varchar(30) not null comment '配置名称',
	`jsonval` json not null comment 'json',
	`intval` int not null comment '整型值',
	primary key (`id`),
	unique key `name` (`name`)
) engine = INNODB charset = utf8mb4 COLLATE utf8_general_ci COMMENT = '配置表';

insert into config values (null, 'max_used_port', '{}', 2000);


