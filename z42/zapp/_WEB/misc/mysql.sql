CREATE TABLE `Ob` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `ico` bigint(20) unsigned NOT NULL DEFAULT '0',
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=100000021 DEFAULT CHARSET=utf8 ;
