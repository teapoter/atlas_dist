DROP TABLE IF EXISTS `script_info`;
CREATE TABLE IF NOT EXISTS `script_info` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `scriptName` varchar(256) NOT NULL COMMENT '脚本名称',
  `description` varchar(256) NOT NULL COMMENT '脚本描述',
  `content` VARCHAR(64) NOT NULL COMMENT '脚本内容',
  `createTime` datetime NOT NULL COMMENT '创建时间',
  `updateTime` datetime NOT NULL COMMENT '更新时间',
  `creator` varchar(32) NOT NULL COMMENT '创建人',
  `flag` tinyint(2) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='存储脚本信息' AUTO_INCREMENT=1 ;