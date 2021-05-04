import discord
from discord.ext import commands

class Tag_management(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.config = bot.config
		self.db = bot.db
		self.functions = bot.functions

	async def create_tag(self, ctx, name, content):
		try:
			await self.db.tags.insert_one({"name" : name, "content" : content})
		except:
			return await self.functions.handle_error(ctx, f"Unknown error creating tag {name}")

	async def update_tag(self, ctx, name, new_content):
		try:
			target = await self.db.tags.find_one({"name" : name})
			await self.db.tags.update_one(target, {"$set": {"content" : new_content}})
		except:
			return await self.functions.handle_error(ctx, f"Unknown error updating tag {name}")

	async def delete_tag(self, ctx, name):
		try:
			await self.db.tags.delete_one({"name" : name})
		except:
			return await self.functions.handle_error(ctx, f"Unknow error deleting tag {name}")

	@commands.command()
	@commands.guild_only()
	async def create(self, ctx, name, *, content):
		# Checks if user has permission to run command
		permission = await self.functions.require_manage_tag_role(ctx, ctx.message.author)
		if not permission:
			return
		# Checks for duplicate
		dupe = await self.db.tags.find_one({"name" : name})
		if dupe:
			return await self.functions.handle_error(ctx, "A tag with that name already exists", "You can edit the existing tag with //edit")
		await self.create_tag(ctx, name, content)
		return await self.functions.confirm_action(ctx, f"Tag `{name}` created")
	
	@commands.command()
	@commands.guild_only()
	async def update(self, ctx, name, *, new_content):
		# Checks if user has permission to run command
		permission = await self.functions.require_manage_tag_role(ctx, ctx.message.author)
		if not permission:
			return
		# Checks if tag exists
		target = await self.db.tags.find_one({"name" : name})
		if not target:
			return await self.functions.handle_error(ctx, f"No tag with the name `{name}` exists")
		await self.update_tag(ctx, name, new_content)
		return await self.functions.confirm_action(ctx, f"Tag `{name}` updated")
	
	@commands.command()
	@commands.guild_only()
	async def delete(self, ctx, *, name):
		# Checks if user has permission to run command
		permission = await self.functions.require_manage_tag_role(ctx, ctx.message.author)
		if not permission:
			return
		# Checks if tag exists
		target = await self.db.tags.find_one({"name" : name})
		if not target:
			return await self.functions.handle_error(ctx, f"No tag with the name `{name}` exists")
		await self.delete_tag(ctx, name)
		return await self.functions.confirm_action(ctx, f"Tag `{name}` deleted")
	

def setup(bot):
	bot.add_cog(Tag_management(bot))