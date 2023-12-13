from abc import ABC, abstractmethod
import discord



class BaseDiscordActionService(ABC):
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction
        self.discord_id = interaction.user.id

    async def add_reactions(self, message, slice: int=None):
        for emoji in self.emoji_list(slice=slice):
            await message.add_reaction(emoji)

    @staticmethod
    def emoji_map(emoji):
        emoji_num_dict = {
            '1️⃣': '1', '2️⃣': '2', '3️⃣': '3', '4️⃣': '4', '5️⃣': '5',
            '6️⃣': '6', '7️⃣': '7', '8️⃣': '8', '9️⃣': '9', '🔟': '10'
        }
        return emoji_num_dict.get(emoji, 'хуй пизда')

    @staticmethod
    def emoji_list(slice: int= None):
        emoji_list = [
            '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣',
            '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'
        ]
        if slice:
            return emoji_list[:slice]
        else:
            return emoji_list