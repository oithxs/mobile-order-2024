
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
  `reservationTime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `store_status` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `is_open` BOOLEAN NOT NULL DEFAULT TRUE , PRIMARY KEY (`id`)
)ENGINE = InnoDB;

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


INSERT INTO `nickname` (`name`, `status`) VALUES('ハンバーグ田中',1),('フィッシュアンドチップス山田',1),('ペンネ中西',1),('ドリアン佐藤',1),('ストロガノフ松本',1),('サラダ鈴木',1),('ラーメン伊藤',1),('カレー山本',1),('コーヒー中村',1),('パスタ小林',1),('ピザ加藤',1),('ビール吉田',1),('チーズ井上',1),('バナナ木村',1),('サンド林',1),('ヨーグルト石田',1),('ハンバーグ近藤',1),('オムレツ川口',1),('そば本田',1),('うどん岡田',1),('かに影山',1),('たこ鷲見',1),('いか変口',1),('サケ真田',1),('フライ大野',1),('キムチ小川',1),('ナッツ山崎',1),('サバ直井',1),('マグロ佐々木',1),('トースト冨田',1),('ケーキ小野',1),('クッキー野口',1),('シチュー田辺',1),('ソース安田',1),('スープ後藤',1),('ピクルス福田',1),('リゾット笠原',1),('ミルク秋山',1),('バター白井',1),('バジル森',1),('アーモンド宮崎',1),('メロン牧野',1),('スシ日野',1),('シラス藤原',1),('カキ小松',1),('タルト江口',1),('イクラ中川',1),('クリーム横山',1),('モッツァ坂本',1);















