#Random bot configs
from discord.enums import ActivityType

# Bot token - keep private!
TOKEN = ""

# Owner and Dev user ID(s)
OWNER = 408372847652634624  # vito#1072 as of 04-11-2021
DEVS = [408372847652634624,261232036625252352]

# Activity settings
ACTIVITY_NAME = "Prisma Illya"
ACTIVITY_TYPE = ActivityType.watching

# Extensions to load
EXTENSIONS = ['cogs.disable',
              'cogs.music']

# Link to the repo for the !about command.
REPO_LINK = "https://github.com/vitobru/kurobot"

# Default embed color
EMBED_COLOR = 0x451d93