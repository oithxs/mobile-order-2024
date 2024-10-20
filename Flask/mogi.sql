--
-- データベース: `mogi.db`
--
CREATE DATABASE mogi;
-- --------------------------------------------------------
USE mogi;

-- --------------------------------------------------------

--
-- テーブルの構造 `Nickname`
--

CREATE TABLE `nickname` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- テーブルの構造 `Received`
--

CREATE TABLE `received` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- テーブルの構造 `Reservation`
--

CREATE TABLE `reservation` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `number` int(11) NOT NULL,
  `ketchup` tinyint(1) NOT NULL,
  `mustard` tinyint(1) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `Nickname`
--
ALTER TABLE `nickname`
  ADD PRIMARY KEY (`id`);

--
-- テーブルのインデックス `Received`
--
ALTER TABLE `received`
  ADD PRIMARY KEY (`id`);

--
-- テーブルのインデックス `Reservation`
--
ALTER TABLE `reservation`
  ADD PRIMARY KEY (`id`);

--
-- ダンプしたテーブルのAUTO_INCREMENT
--

--
-- テーブルのAUTO_INCREMENT `Nickname`
--
ALTER TABLE `nickname`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルのAUTO_INCREMENT `Received`
--
ALTER TABLE `received`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルのAUTO_INCREMENT `Reservation`
--
ALTER TABLE `reservation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;
