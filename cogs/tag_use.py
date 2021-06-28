import discord
from discord.ext import commands

class Tag_use(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.config = bot.config
		self.db = bot.db

	@commands.Cog.listener()
	async def on_message(self, message):
		ctx: commands.Context = await self.bot.get_context(message)
		if ctx.message.author.bot:
			return
		if ctx.message.content.startswith("/"):
			tag_name = ctx. message.content.replace(f"/","")
			try:
				tag = await self.db.tags.find_one({"name" : tag_name})
			except:
				return
			if not tag:
				return
			await ctx.send(tag["content"])

def setup(bot):
	bot.add_cog(Tag_use(bot))