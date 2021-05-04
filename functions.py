import discord
from discord.ext import commands
from config import Config
import os

class Functions:

    async def handle_error(self, ctx, description : str, troubleshooting : str = None):
        embed = discord.Embed(
            description = description,
            color = 0xf34141
            )
        embed.set_author(name = "Error")
        if troubleshooting:
            embed.set_footer(text = troubleshooting)
        await ctx.send(embed = embed)
    
    async def confirm_action(self, ctx, description : str, additional_info: str = None):
        embed = discord.Embed(
            description = description,
            color = 0x43e286
        )
        embed.set_author(name = "Success")
        if additional_info:
            embed.set_footer(text = additional_info)
        await ctx.send(embed = embed)

    async def require_manage_tag_role(self, ctx, user: discord.User):
        for role in Config.manage_tag_roles:
            role = discord.utils.get(ctx.guild.roles, id = role)
            if role in ctx.message.author.roles:
                return True
        await self.handle_error(ctx, "You do not have permission to run this command")
        return False