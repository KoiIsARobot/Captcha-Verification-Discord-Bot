import os
import disnake
from disnake.ext import commands
from captcha.image import ImageCaptcha
import random
from disnake.enums import ButtonStyle
bot = commands.Bot(command_prefix = '.', test_guilds = [1069982958859067542], intents = disnake.Intents.all())       #REPLACE HERE WITH THE ID OF YOUR SERVER



global guild, id_verification_role, id_verification_channel 
suc_pattern = ""
pattern = ""

drop_list_text_option = []
drop_list_role_option = []

def load_role_channel():												# UPLOADING CHANNELS AND ROLES. WORKS WHEN THE BOT IS INSTALLED, AND WHEN THE COMMAND /reload
	global drop_list_text_option
	for channel in guild.channels:
		if channel.type != disnake.ChannelType.category:
			if channel.type == disnake.ChannelType.text:
				drop_list_text_option.append(
					disnake.SelectOption(
					label = str(channel),
					value = str(channel.id)
					)
					)
	for r in guild.roles:
		if r.name != "@everyone":
			drop_list_role_option.append(
					disnake.SelectOption(
					label = str(r.name),
					value = str(r.id)
					)
					)


@bot.event
async def on_ready():													# SLASH COMMANDS
	global guild
	print("Bot connected")
	guild = bot.get_guild(1069982958859067542)                #REPLACE HERE WITH THE ID OF YOUR SERVER
	load_role_channel()

@bot.slash_command(description = "Setting the channel and role for verification")
@commands.default_member_permissions(administrator=True)
async def verification_channel(inter: disnake.ApplicationCommandInteraction):
	await inter.response.send_message(view = DropViewChannel(), ephemeral=True)


@bot.slash_command(description = "Updates drop-down lists of roles and channels")
@commands.default_member_permissions(administrator=True)
async def reload(ctx):
	load_role_channel()


@bot.listen("on_button_click")
async def help_listener(inter: disnake.MessageInteraction):							#PROCESSING THE "VERIFY" BUTTON
	global suc_pattern
	pattern = ""
	if inter.component.custom_id not in ["ver"]:
		return
	if inter.component.custom_id == "ver":
		for a in range(6):
			pattern += str(random.randint(0,9))
		if os.path.isdir(str(inter.author)) == False:
			os.mkdir(str(inter.author))
		image_captcha = ImageCaptcha(width = 440, height = 140, fonts = ['BRADHI.ttf', 'LuckiestGuy-Regular.ttf', 'earwig.ttf'], font_sizes = [128])
		image_captcha.write(pattern, "captcha.png")
		os.replace("captcha.png", f"{inter.author}/captcha.png")
		suc = ""
		with open(f"{inter.author}/patterns.txt", "w+") as f:
			f.write(f"{suc}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = "``` ```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.send_message(embed = embed, view = RowButtons() ,ephemeral=True)


class DropRole(disnake.ui.StringSelect):									# DROP-DOWN LISTS OF TEXT CHANNELS AND ROLES
	def __init__(self):
		options = drop_list_role_option
		super().__init__(placeholder = "Choose verified role", min_values = 1, max_values = 1,options = options)
	
	async def callback(self, inter: disnake.MessageInteraction):
		global id_verification_role
		id_verification_role = self.values[0]
		embed = disnake.Embed(title="Captcha Verification",
		description="Press button Verify below",
		color=disnake.Colour.red(),
		)
		await bot.get_channel(int(id_verification_channel)).send(embed = embed,
		components=[
			disnake.ui.Button(label="Verify", style=disnake.ButtonStyle.success, custom_id="ver"),
			],
			)



class DropViewRole(disnake.ui.View):
	def __init__(self):
		super().__init__()
		self.add_item(DropRole())


class DropChannel(disnake.ui.StringSelect):
	def __init__(self):
		options = drop_list_text_option
		super().__init__(placeholder = "Choose a channel for verification", min_values = 1, max_values = 1,options = options)

	async def callback(self, inter: disnake.MessageInteraction):
		global id_verification_channel
		id_verification_channel = self.values[0]
		await inter.response.edit_message(view = DropViewRole())


class DropViewChannel(disnake.ui.View):
	def __init__(self):
		super().__init__()
		self.add_item(DropChannel())


class RowButtons(disnake.ui.View):														# BUTTONS FOR VERIFICATION AND CLICK EVENTS
	def __init__(self):
		super().__init__(timeout=None)

	@disnake.ui.button(label="1", style=ButtonStyle.blurple)
	async def first_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-1] + "1"
		with open(f"{inter.author}/patterns.txt", "w") as f:
			f.write(f"{suc_pattern}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = f"```{suc_pattern}```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.edit_message(embed = embed)

	@disnake.ui.button(label="2", style=ButtonStyle.blurple)
	async def second_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-1] + "2"
		with open(f"{inter.author}/patterns.txt", "w") as f:
			f.write(f"{suc_pattern}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = f"```{suc_pattern}```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.edit_message(embed = embed)

	@disnake.ui.button(label="3", style=ButtonStyle.blurple)
	async def third_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-1] + "3"
		with open(f"{inter.author}/patterns.txt", "w") as f:
			f.write(f"{suc_pattern}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = f"```{suc_pattern}```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.edit_message(embed = embed)

	@disnake.ui.button(label="4", style=ButtonStyle.blurple, row=1)
	async def fourth_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-1] + "4"
		with open(f"{inter.author}/patterns.txt", "w") as f:
			f.write(f"{suc_pattern}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = f"```{suc_pattern}```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.edit_message(embed = embed)

	@disnake.ui.button(label="5", style=ButtonStyle.blurple, row=1)
	async def fifth_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-1] + "5"
		with open(f"{inter.author}/patterns.txt", "w") as f:
			f.write(f"{suc_pattern}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = f"```{suc_pattern}```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.edit_message(embed = embed)

	@disnake.ui.button(label="6", style=ButtonStyle.blurple, row=1)
	async def six_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-1] + "6"
		with open(f"{inter.author}/patterns.txt", "w") as f:
			f.write(f"{suc_pattern}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = f"```{suc_pattern}```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.edit_message(embed = embed)

	@disnake.ui.button(label="7", style=ButtonStyle.blurple, row=2)
	async def seven_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-1] + "7"
		with open(f"{inter.author}/patterns.txt", "w") as f:
			f.write(f"{suc_pattern}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = f"```{suc_pattern}```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.edit_message(embed = embed)

	@disnake.ui.button(label="8", style=ButtonStyle.blurple, row=2)
	async def eight_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-1] + "8"
		with open(f"{inter.author}/patterns.txt", "w") as f:
			f.write(f"{suc_pattern}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = f"```{suc_pattern}```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.edit_message(embed = embed)

	@disnake.ui.button(label="9", style=ButtonStyle.blurple, row=2)
	async def nine_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-1] + "9"
		with open(f"{inter.author}/patterns.txt", "w") as f:
			f.write(f"{suc_pattern}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = f"```{suc_pattern}```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.edit_message(embed = embed)

	@disnake.ui.button(label="❌", style=ButtonStyle.blurple, row=3)
	async def return_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-2]
		with open(f"{inter.author}/patterns.txt", "w") as f:
			f.write(f"{suc_pattern}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = f"```{suc_pattern}```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.edit_message(embed = embed)

	@disnake.ui.button(label="0", style=ButtonStyle.blurple, row=3)
	async def zero_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-1] + "0"
		with open(f"{inter.author}/patterns.txt", "w") as f:
			f.write(f"{suc_pattern}\n{pattern}")
		embed = disnake.Embed(title = "Your input", description = f"```{suc_pattern}```", color = disnake.Colour.red())
		embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
		await inter.response.edit_message(embed = embed)

	@disnake.ui.button(label="✅", style=ButtonStyle.blurple, row=3)
	async def sucsess_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
		with open(f"{inter.author}/patterns.txt", "r") as f:
			suc_pattern = f.readline()
			pattern = f.readline()
		suc_pattern = suc_pattern[:-1]
		print (suc_pattern == pattern)
		if suc_pattern == pattern:
			role = inter.guild.get_role(int(id_verification_role))
			if role not in inter.author.roles:
				await inter.author.add_roles(role)
			newembed = disnake.Embed(title = "You have successfully completed verification", color = disnake.Colour.green())
			newembed.set_image(file=disnake.File("None.png"))
			os.remove(f"{inter.author}/captcha.png")
			os.remove(f"{inter.author}/patterns.txt")
			os.rmdir(f"{inter.author}")
			await inter.response.edit_message(embed = newembed, view = None)
		else:
			suc_pattern = ""
			pattern = ""
			for a in range(6):
				pattern += str(random.randint(0,9))
			os.remove(f"{inter.author}/captcha.png")
			image_captcha = ImageCaptcha(width = 440, height = 140, fonts = ['BRADHI.ttf', 'LuckiestGuy-Regular.ttf', 'earwig.ttf'], font_sizes = [128])
			image_captcha.write(pattern, 'captcha.png')
			os.replace("captcha.png", f"{inter.author}/captcha.png")
			with open(f"{inter.author}/patterns.txt", "w") as f:
				f.write(f"{suc_pattern}\n{pattern}")
			embed = disnake.Embed(title = "Your input", description = "```Captcha was entered incorrectly```", color = disnake.Colour.red())
			embed.set_image(file=disnake.File(f"{inter.author}/captcha.png"))
			await inter.response.edit_message(embed = embed)




bot.run("...")      # BOT TOKEN