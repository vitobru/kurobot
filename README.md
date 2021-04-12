# Kuro Bot v.0.7.3-indev

###### A Discord bot created by Vitobru and Alatar

**Info:** This is a small Discord bot written sitting on top of the discord.py library. Still in its alpha stages of development, it can perform some basic tasks such as latency, uptime, and playing uploaded mp3 files in VC, all prefaced by the $ parameter (eventually customisable). You can also disable commands on a per-server basis as those transactions will be stored in a SQL DB file.

**Prerequisites:** You're gonna need `discord.py`, aiosqlite, PyNaCl, redis, and youtube_dl for this; all of which you can easily install through the terminal, using:
```
pip install -U discord.py
pip install -U aiosqlite
pip install -U youtube_dl
pip install -U PyNaCl
pip install -U redis
```

Then, you'll need to install ffmpeg and redis however you can.
On Arch Linux, it's:
```
pacman -S ffmpeg
pacman -S redis
```

Please note that Windows is not fully supported yet, you will need to fix the issues yourself.

**Team:**

Lead Programmers - vito and alatartheblue42

**Contact:** [Click here](mailto:lillieerinhp@gmail.com) if you wanna email me about the progress. Otherwise, just tweet me [@lillieerinw](https://twitter.com/lillieerinw/).
