async def on_ready(self):
    print(f"Logged in as {self.user}")

    games = mlb.get_todays_games()
    print("Connected to MLB API!")
    print(games)

    if CHANNEL_ID:
        ch = self.get_channel(int(CHANNEL_ID))
        if ch:
            await ch.send("✅ DingerHQ bot is online.")

    await mlb.start(self)
