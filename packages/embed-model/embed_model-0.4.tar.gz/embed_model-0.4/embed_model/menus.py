import discord
from . import EmbedGenerator
from .modals import EditFieldModal

class RemoverFieldMenus(discord.ui.Select):
	def __init__(self, message: discord.Message):
		if not message.embeds or not message.embeds[0].fields:
			raise ValueError("A mensagem não contém embeds ou campos para remover.")

		embed = message.embeds[0]
		fields = embed.fields

		options = [
			discord.SelectOption(label=field.name, value=str(i)) for i, field in enumerate(fields)
		]

		super().__init__(placeholder="Selecione um Field para remover", options=options)

		self.message = message

	async def callback(self, interaction: discord.Interaction):
		field_index = int(self.values[0])
		embed = self.message.embeds[0]

		embed.remove_field(field_index)

		await self.message.edit(embed=embed, view=EmbedGenerator(self.message))

class EditarFieldMenus(discord.ui.Select):
	def __init__(self, message: discord.Message):
		if not message.embeds or not message.embeds[0].fields:
			raise ValueError("A mensagem não contém embeds ou campos para editar.")

		embed = message.embeds[0]
		fields = embed.fields

		options = [
			discord.SelectOption(label=field.name, value=str(i)) for i, field in enumerate(fields)
		]

		super().__init__(placeholder="Selecione um Field para editar", options=options)

		self.message = message

	async def callback(self, interaction: discord.Interaction):
		field_index = int(self.values[0])
		embed = self.message.embeds[0]
		field = embed.fields[field_index]

		modal = EditFieldModal(self.message, field_index, field.name, field.value, str(field.inline))
		await interaction.response.send_modal(modal)

class LinguagemSelect(discord.ui.Select):
	def __init__(self):
		options = [
			discord.SelectOption(label="Python", description="Gerar código em Python", emoji="🐍"),
			discord.SelectOption(label="JSON", description="Gerar código em JSON", emoji="📄"),
			discord.SelectOption(label="JavaScript", description="Gerar código em JavaScript", emoji="🛠️"),
		]
		super().__init__(placeholder="Escolha uma linguagem", options=options)

	async def callback(self, interaction: discord.Interaction):
		embed = interaction.message.embeds[0]

		descricao = embed.description.replace('\n', '\\n')
		python_code = f"discord.Embed(title=\"{embed.title}\", description=\"{descricao}\", timestamp={embed.timestamp}"
		python_code += f", colour=discord.Color.from_str({'"#{:06X}"'.format(embed.colour)}))" if embed.colour else ")"
		if embed.author:
			python_code += f"\nembed.set_author(name=\"{embed.author.name}\""
			if embed.author.url:
				python_code += f", url=\"{embed.author.url}\""
			if embed.author.icon_url:
				python_code += f", icon_url=\"{embed.author.icon_url}\""
			python_code += ")"
		if embed.image:
			python_code += f"\nembed.set_image(url=\"{embed.image.url}\")"
		if embed.thumbnail:
			python_code += f"\nembed.set_thumbnail(url=\"{embed.thumbnail.url}\")"
		if embed.footer:
			python_code += f"\nembed.set_footer(text=\"{embed.footer.text}\""
			if embed.footer.icon_url:
				python_code += f", icon_url=\"{embed.footer.icon_url}\""
			python_code += ")"
		for field in embed.fields:
			python_code += f"\nembed.add_field(name=\"{field.name}\", value=\"{field.value}\", inline={field.inline})"

		# Gerar código em JSON
		json_code = "{\n"
		json_code += f'	"title": "{embed.title}",\n'
		json_code += f'	"description": "{descricao}",\n'
		json_code += f'	"color": {'"#{:06X}"'.format(embed.colour.value) if embed.colour else None},\n'
		json_code += f'	"timestamp": "{embed.timestamp.isoformat()}"' if embed.timestamp else ""
		if embed.author:
			json_code += f',\n	"author": {{\n		"name": "{embed.author.name}"'
			if embed.author.url:
				json_code += f',\n		"url": "{embed.author.url}"'
			if embed.author.icon_url:
				json_code += f',\n		"icon_url": "{embed.author.icon_url}"'
			json_code += "\n	}"
		if embed.image:
			json_code += f',\n	"image": {{\n		"url": "{embed.image.url}"\n	}}'
		if embed.thumbnail:
			json_code += f',\n	"thumbnail": {{\n		"url": "{embed.thumbnail.url}"\n	}}'
		if embed.footer:
			json_code += f',\n	"footer": {{\n		"text": "{embed.footer.text}"'
			if embed.footer.icon_url:
				json_code += f',\n		"icon_url": "{embed.footer.icon_url}"'
			json_code += "\n	}"
		if embed.fields:
			json_code += ',\n	"fields": ['
			for field in embed.fields:
				json_code += f'\n		{{\n			"name": "{field.name}",\n			"value": "{field.value}",\n			"inline": "{str(field.inline).lower()}"\n		}},'
			json_code = json_code.rstrip(",") + "\n	]"
		json_code += "\n}"

		# Gerar código em JavaScript
		js_code = "const embed = {\n"
		js_code += f'	title: "{embed.title}",\n'
		js_code += f'	description: "{descricao}",\n'
		js_code += f'	color: {'"#{:06X}"'.format(embed.colour.value) if embed.colour else 'null'},\n'
		js_code += f'	timestamp: "{embed.timestamp.isoformat()}"' if embed.timestamp else ""
		if embed.author:
			js_code += f',\n	author: {{\n		name: "{embed.author.name}"'
			if embed.author.url:
				js_code += f',\n		url: "{embed.author.url}"'
			if embed.author.icon_url:
				js_code += f',\n		icon_url: "{embed.author.icon_url}"'
			js_code += "\n	}"
		if embed.image:
			js_code += f',\n	image: {{\n		url: "{embed.image.url}"\n	}}'
		if embed.thumbnail:
			js_code += f',\n	thumbnail: {{\n		url: "{embed.thumbnail.url}"\n	}}'
		if embed.footer:
			js_code += f',\n	footer: {{\n		text: "{embed.footer.text}"'
			if embed.footer.icon_url:
				js_code += f',\n		icon_url: "{embed.footer.icon_url}"'
			js_code += "\n	}"
		if embed.fields:
			js_code += ',\n	fields: ['
			for field in embed.fields:
				js_code += f'\n		{{\n			name: "{field.name}",\n			value: "{field.value}",\n			inline: {str(field.inline).lower()}\n		}},'
			js_code = js_code.rstrip(",") + "\n	]"
		js_code += "\n};"

		# Determinar o código com base na linguagem selecionada
		if self.values[0] == "Python":
			code = f"```python\n{python_code}```"
		elif self.values[0] == "JSON":
			code = f"```json\n{json_code}```"
		elif self.values[0] == "JavaScript":
			code = f"```javascript\n{js_code}```"

		# Responder com o código correspondente
		await interaction.response.send_message(code, ephemeral=True)