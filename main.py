async def on_ready(self):
    print(f"Logged in as {self.user}", flush=True)

    ch = None

    if CHANNEL_ID:
        try:
            ch = await self.fetch_channel(int(CHANNEL_ID))
            print(f"Channel: {ch}", flush=True)

            await ch.send("✅ DingerHQ bot is online!")

        except Exception as e:
            print(f"Failed to fetch channel: {e}", flush=True)

    print("🚨 THIS IS THE NEW MAIN.PY", flush=True)

    if ch:
        await alerts.watch_home_runs(self, ch)
    else:
        print("No valid channel found.", flush=True)