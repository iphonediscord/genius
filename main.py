from aiohttp import ClientSession
import asyncio
from config import Config
from datetime import datetime
import discord
from discord.ext import commands
from functions import Functions
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os
import pymongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import sys

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1")

cogs = ['cogs.admin','cogs.tag_management','cogs.tag_use']

class Genius(commands.Bot):

	def __init__(self):
		super().__init__(
			command_prefix = "//",
			description = ""
		)

		self.config = Config()
		self.db: AsyncIOMotorDatabase
		self.functions = Functions()

	async def on_ready(self):
		print(f"{self.user.name} ({self.user.id}) is online")
		print("______________")
		# Sets playing status to "watching your questions"
		await self.change_presence(activity = discord.Activity(name = "you", type = 3))
		# Attempts to load extensions
		print("Loading extensions...")
		for cog in cogs:
			  self.load_extension(cog)
		print("Loaded extensions")
		print("______________")

	async def init_http(self):
		self.session = ClientSession()

	async def init_mongo(self) -> None:
		self.mongo = AsyncIOMotorClient(MONGO_URI)
		await self.mongo.admin.command("ismaster")
		self.db = self.mongo.genius
		print("Connected to database")
		print("______________")

	async def close(self):
		await super().close()
		await self.session.close()
		self.mongo.close()


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	bot = Genius()

	loop.run_until_complete(bot.init_http())

	try:
		loop.run_until_complete(bot.init_mongo())
	except ServerSelectionTimeoutError:
		print("Could not connect to mongo, timed out\nExiting.")
		sys.exit(0)

	bot.run(DISCORD_TOKEN)