CREATE TABLE IF NOT EXISTS guilds (
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