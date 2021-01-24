CREATE TABLE IF NOT EXISTS Prefixes (
	GuildID integer PRIMARY KEY,
	Prefix text DEFAULT "-"
);


CREATE TABLE IF NOT EXISTS balance (
	GuildID integer,
	GuildName text,
	MemberID integer,
	MemberName text,
	Money integer DEFAULT 0
);


CREATE TABLE IF NOT EXISTS welchannel (
	ChannelID integer DEFAULT 0,
	GuildID integer,
	Message text DEFAULT "приветствуем тебя на нашем сервере!"
);

CREATE TABLE IF NOT EXISTS exitchannel (
	ChannelID integer DEFAULT 0,
	GuildID integer,
	Message text DEFAULT "покинул ряды нашего сервера!"
);