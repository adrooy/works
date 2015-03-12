CREATE TABLE `uninstall_caller_log` (
  `caller` VARCHAR(256) DEFAULT NULL,
  `callee` VARCHAR(256) DEFAULT NULL,
  `cnt` INT(11) DEFAULT NULL,
  UNIQUE KEY `both_index` (`caller`,`callee`(64)),
  KEY `caller_index` (`caller`(64)),
  KEY `callee_index` (`callee`(64))
) ENGINE=MYISAM DEFAULT CHARSET=utf8


SELECT COUNT(*) FROM uninstall_caller_log

SELECT SUM(cnt) FROM uninstall_caller_log

DELETE FROM uninstall_caller_log WHERE caller = 'unknown'

SELECT caller, SUM(cnt) AS totalcnt FROM uninstall_caller_log GROUP BY caller ORDER BY totalcnt DESC

SELECT callee, SUM(cnt) AS totalcnt FROM uninstall_caller_log GROUP BY callee ORDER BY totalcnt DESC

