-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               10.3.13-MariaDB-log - mariadb.org binary distribution
-- Операционная система:         Win64
-- HeidiSQL Версия:              10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Дамп структуры базы данных anime_norm_maria
CREATE DATABASE IF NOT EXISTS `anime_norm_maria` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `anime_norm_maria`;

-- Дамп структуры для таблица anime_norm_maria.anime
CREATE TABLE IF NOT EXISTS `anime` (
  `anime_id` int(11) unsigned NOT NULL,
  `title` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title_english` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title_japanese` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title_synonyms` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image_url` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `source` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `episodes` int(10) unsigned DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `airing` tinyint(1) DEFAULT NULL,
  `start_date` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `finish_date` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `duration` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rating` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `premiered_year` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `premiered_season` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `broadcast_day` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `broadcast_time` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `opening_theme` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ending_theme` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `url_mal` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `url_shiki` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`anime_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.animelists_cleaned_full
CREATE TABLE IF NOT EXISTS `animelists_cleaned_full` (
  `username` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `anime_id` int(11) unsigned NOT NULL,
  `my_watched_episodes` int(11) DEFAULT NULL,
  `my_start_date` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `my_finish_date` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `my_score` int(11) DEFAULT NULL,
  `my_status` int(11) DEFAULT NULL,
  `my_rewatching` tinyint(4) DEFAULT NULL,
  `my_rewatching_ep` int(11) DEFAULT NULL,
  `my_last_updated` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `my_tags` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `broadcast_day` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `broadcast_time` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.anime_filtered_full
CREATE TABLE IF NOT EXISTS `anime_filtered_full` (
  `anime_id` int(11) unsigned NOT NULL,
  `title` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title_english` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title_japanese` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title_synonyms` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image_url` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `source` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `episodes` int(11) DEFAULT NULL,
  `status` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `airing` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `aired_string` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `aired` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `duration` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rating` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `score` double DEFAULT NULL,
  `scored_by` int(11) DEFAULT NULL,
  `rank` double DEFAULT NULL,
  `popularity` int(11) DEFAULT NULL,
  `members` int(11) DEFAULT NULL,
  `favorites` int(11) DEFAULT NULL,
  `background` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `premiered` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `broadcast` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `related` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `producer` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `licensor` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `studio` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `genre` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `opening_theme` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ending_theme` text COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.anime_genre
CREATE TABLE IF NOT EXISTS `anime_genre` (
  `id_anime` bigint(20) DEFAULT NULL,
  `id_genre` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.anime_licensor
CREATE TABLE IF NOT EXISTS `anime_licensor` (
  `id_anime` bigint(20) DEFAULT NULL,
  `id_licensor` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.anime_producer
CREATE TABLE IF NOT EXISTS `anime_producer` (
  `id_anime` bigint(20) DEFAULT NULL,
  `id_producer` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.anime_studio
CREATE TABLE IF NOT EXISTS `anime_studio` (
  `id_anime` bigint(20) DEFAULT NULL,
  `id_studio` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.genre
CREATE TABLE IF NOT EXISTS `genre` (
  `id_genre` int(11) DEFAULT NULL,
  `title_genre` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.licensor
CREATE TABLE IF NOT EXISTS `licensor` (
  `id_licensor` int(11) DEFAULT NULL,
  `title_licensor` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.producer
CREATE TABLE IF NOT EXISTS `producer` (
  `id_producer` int(11) DEFAULT NULL,
  `title_producer` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.relation
CREATE TABLE IF NOT EXISTS `relation` (
  `id_anime_object` int(11) unsigned NOT NULL,
  `id_relation` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `id_anime_subject` int(11) unsigned NOT NULL,
  KEY `FK_anime_related_anime` (`id_anime_object`),
  KEY `FK_anime_related_anime_2` (`id_anime_subject`),
  CONSTRAINT `FK_anime_related_anime` FOREIGN KEY (`id_anime_object`) REFERENCES `anime` (`anime_id`),
  CONSTRAINT `FK_anime_related_anime_2` FOREIGN KEY (`id_anime_subject`) REFERENCES `anime` (`anime_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.studio
CREATE TABLE IF NOT EXISTS `studio` (
  `id_studio` int(11) DEFAULT NULL,
  `title_studio` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.user
CREATE TABLE IF NOT EXISTS `user` (
  `id_user` int(10) unsigned NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` enum('Male','Female','Non-Binary') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birth_date` date NOT NULL,
  `join_date` date NOT NULL,
  `location_user` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.user_anime
CREATE TABLE IF NOT EXISTS `user_anime` (
  `id_user` int(10) unsigned NOT NULL,
  `id_anime` int(10) unsigned NOT NULL,
  `watched_ep` int(10) unsigned NOT NULL,
  `my_status` int(1) unsigned NOT NULL,
  `my_start_date` date NOT NULL,
  `my_finish_date` date NOT NULL,
  `my_score` int(2) unsigned NOT NULL,
  `my_rewatching` int(10) unsigned NOT NULL,
  `my_rewatching_ep` int(10) unsigned NOT NULL,
  `my_tags` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_user`,`id_anime`),
  KEY `FK_user-anime_anime` (`id_anime`),
  KEY `FK_user-anime_user` (`id_user`),
  CONSTRAINT `FK_user-anime_anime` FOREIGN KEY (`id_anime`) REFERENCES `anime` (`anime_id`),
  CONSTRAINT `FK_user-anime_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

-- Дамп структуры для таблица anime_norm_maria.user_filtered
CREATE TABLE IF NOT EXISTS `user_filtered` (
  `username` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `user_watching` int(11) DEFAULT NULL,
  `user_completed` int(11) DEFAULT NULL,
  `user_onhold` int(11) DEFAULT NULL,
  `user_dropped` int(11) DEFAULT NULL,
  `user_plantowatch` int(11) DEFAULT NULL,
  `user_days_spent_watching` double DEFAULT NULL,
  `gender` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `location` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birth_date` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `access_rank` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `join_date` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_online` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stats_mean_score` double DEFAULT NULL,
  `stats_rewatched` double DEFAULT NULL,
  `stats_episodes` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Экспортируемые данные не выделены.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
