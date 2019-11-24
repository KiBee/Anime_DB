-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Ноя 24 2019 г., 17:09
-- Версия сервера: 10.3.13-MariaDB-log
-- Версия PHP: 5.6.40

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `anime_norm_maria`
--
CREATE DATABASE IF NOT EXISTS `anime_norm_maria` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `anime_norm_maria`;

-- --------------------------------------------------------

--
-- Структура таблицы `anime`
--

CREATE TABLE `anime` (
  `anime_id` int(11) UNSIGNED NOT NULL,
  `title` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title_english` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title_japanese` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title_synonyms` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image_url` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `source` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `episodes` int(10) UNSIGNED DEFAULT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `airing` enum('Y','N') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `finish_date` date DEFAULT NULL,
  `duration` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rating` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `opening_theme` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ending_theme` text COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `premiered_year` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `premiered_season` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `broadcast_day` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `broadcast_time` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anime_genre`
--

CREATE TABLE `anime_genre` (
  `id_genre` int(11) UNSIGNED NOT NULL,
  `id_anime` int(11) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anime_licensor`
--

CREATE TABLE `anime_licensor` (
  `id_licensor` int(10) UNSIGNED NOT NULL,
  `id_anime` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anime_producer`
--

CREATE TABLE `anime_producer` (
  `id_producer` int(10) UNSIGNED NOT NULL,
  `id_anime` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `anime_studio`
--

CREATE TABLE `anime_studio` (
  `id_studio` int(10) UNSIGNED NOT NULL,
  `id_anime` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `genre`
--

CREATE TABLE `genre` (
  `id_genre` int(11) UNSIGNED NOT NULL,
  `title_genre` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `licensor`
--

CREATE TABLE `licensor` (
  `id_licensor` int(10) UNSIGNED NOT NULL,
  `title_licensor` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `producer`
--

CREATE TABLE `producer` (
  `id_producer` int(10) UNSIGNED NOT NULL,
  `title_producer` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `relation`
--

CREATE TABLE `relation` (
  `id_anime_object` int(11) UNSIGNED NOT NULL,
  `id_relation` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `id_anime_subject` int(11) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `studio`
--

CREATE TABLE `studio` (
  `id_studio` int(10) UNSIGNED NOT NULL,
  `title_studio` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `user`
--

CREATE TABLE `user` (
  `id_user` int(10) UNSIGNED NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gender` enum('Male','Female','Non-Binary') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `birth_date` date NOT NULL,
  `join_date` date NOT NULL,
  `location_user` text COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `user_anime`
--

CREATE TABLE `user_anime` (
  `id_user` int(10) UNSIGNED NOT NULL,
  `id_anime` int(10) UNSIGNED NOT NULL,
  `watched_ep` int(10) UNSIGNED NOT NULL,
  `my_status` int(1) UNSIGNED NOT NULL,
  `my_start_date` date NOT NULL,
  `my_finish_date` date NOT NULL,
  `my_score` int(2) UNSIGNED NOT NULL,
  `my_rewatching` int(10) UNSIGNED NOT NULL,
  `my_rewatching_ep` int(10) UNSIGNED NOT NULL,
  `my_tags` text COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `anime`
--
ALTER TABLE `anime`
  ADD PRIMARY KEY (`anime_id`);

--
-- Индексы таблицы `anime_genre`
--
ALTER TABLE `anime_genre`
  ADD KEY `FK_anime-genre_genre` (`id_genre`),
  ADD KEY `FK_anime-genre_anime` (`id_anime`);

--
-- Индексы таблицы `anime_licensor`
--
ALTER TABLE `anime_licensor`
  ADD KEY `FK_anime_licensor_licensor` (`id_licensor`),
  ADD KEY `FK_anime_licensor_anime` (`id_anime`);

--
-- Индексы таблицы `anime_producer`
--
ALTER TABLE `anime_producer`
  ADD KEY `FK_anime_producer_producer` (`id_producer`),
  ADD KEY `FK_anime_producer_anime` (`id_anime`);

--
-- Индексы таблицы `anime_studio`
--
ALTER TABLE `anime_studio`
  ADD KEY `FK_studio_anime_anime` (`id_anime`),
  ADD KEY `FK_studio_anime_studio` (`id_studio`);

--
-- Индексы таблицы `genre`
--
ALTER TABLE `genre`
  ADD PRIMARY KEY (`id_genre`);

--
-- Индексы таблицы `licensor`
--
ALTER TABLE `licensor`
  ADD PRIMARY KEY (`id_licensor`);

--
-- Индексы таблицы `producer`
--
ALTER TABLE `producer`
  ADD PRIMARY KEY (`id_producer`);

--
-- Индексы таблицы `relation`
--
ALTER TABLE `relation`
  ADD KEY `FK_anime_related_anime` (`id_anime_object`),
  ADD KEY `FK_anime_related_anime_2` (`id_anime_subject`);

--
-- Индексы таблицы `studio`
--
ALTER TABLE `studio`
  ADD PRIMARY KEY (`id_studio`);

--
-- Индексы таблицы `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`);

--
-- Индексы таблицы `user_anime`
--
ALTER TABLE `user_anime`
  ADD PRIMARY KEY (`id_user`,`id_anime`),
  ADD KEY `FK_user-anime_anime` (`id_anime`),
  ADD KEY `FK_user-anime_user` (`id_user`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `genre`
--
ALTER TABLE `genre`
  MODIFY `id_genre` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `licensor`
--
ALTER TABLE `licensor`
  MODIFY `id_licensor` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `producer`
--
ALTER TABLE `producer`
  MODIFY `id_producer` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `studio`
--
ALTER TABLE `studio`
  MODIFY `id_studio` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `anime_genre`
--
ALTER TABLE `anime_genre`
  ADD CONSTRAINT `FK_anime-genre_anime` FOREIGN KEY (`id_anime`) REFERENCES `anime` (`anime_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_anime-genre_genre` FOREIGN KEY (`id_genre`) REFERENCES `genre` (`id_genre`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `anime_licensor`
--
ALTER TABLE `anime_licensor`
  ADD CONSTRAINT `FK_anime_licensor_anime` FOREIGN KEY (`id_anime`) REFERENCES `anime` (`anime_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_anime_licensor_licensor` FOREIGN KEY (`id_licensor`) REFERENCES `licensor` (`id_licensor`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `anime_producer`
--
ALTER TABLE `anime_producer`
  ADD CONSTRAINT `FK_anime_producer_anime` FOREIGN KEY (`id_anime`) REFERENCES `anime` (`anime_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_anime_producer_producer` FOREIGN KEY (`id_producer`) REFERENCES `producer` (`id_producer`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `anime_studio`
--
ALTER TABLE `anime_studio`
  ADD CONSTRAINT `FK_studio_anime_anime` FOREIGN KEY (`id_anime`) REFERENCES `anime` (`anime_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `FK_studio_anime_studio` FOREIGN KEY (`id_studio`) REFERENCES `studio` (`id_studio`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `relation`
--
ALTER TABLE `relation`
  ADD CONSTRAINT `FK_anime_related_anime` FOREIGN KEY (`id_anime_object`) REFERENCES `anime` (`anime_id`),
  ADD CONSTRAINT `FK_anime_related_anime_2` FOREIGN KEY (`id_anime_subject`) REFERENCES `anime` (`anime_id`);

--
-- Ограничения внешнего ключа таблицы `user_anime`
--
ALTER TABLE `user_anime`
  ADD CONSTRAINT `FK_user-anime_anime` FOREIGN KEY (`id_anime`) REFERENCES `anime` (`anime_id`),
  ADD CONSTRAINT `FK_user-anime_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
