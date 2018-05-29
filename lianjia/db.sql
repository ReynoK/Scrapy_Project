create database lianjia;
create table lianjia.renting_information(
	`id` bigint(20) PRIMARY KEY NOT NULL auto_increment comment '主键',
	`name` varchar(1024) NOT NULL DEFAULT '' COMMENT '租房名称',
	`area` varchar(1024) NOT NULL DEFAULT '' COMMENT '区域',
	`house_type` varchar(1024) NOT NULL DEFAULT '' COMMENT '房屋类型',
	`layer` varchar(1024) NOT NULL DEFAULT '' COMMENT '楼层',
	`subway` varchar(1024) NOT NULL DEFAULT '' COMMENT '地铁',
	`position` varchar(1024) NOT NULL DEFAULT '' COMMENT '位置',
	`manager` varchar(1024) NOT NULL DEFAULT '' COMMENT '中介',
	`price` varchar(1024) NOT NULL DEFAULT '' COMMENT '价格'
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='链家租房信息';
