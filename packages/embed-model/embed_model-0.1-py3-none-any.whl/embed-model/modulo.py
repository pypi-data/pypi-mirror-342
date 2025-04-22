import discord
import json
from discord import app_commands

class EmbedTextModal(discord.ui.Modal, title="Editar Embed (Textos)"):
	def __init__(self, message: discord.Message):
		super().__init__()
		self.message = message
		self.embed = message.embeds[0]

		self.msg_content.default = message.content
		self.embed_title.default = self.embed.title
		self.embed_description.default = self.embed.description
		self.embed_color.default = f"#{self.embed.colour.value:06x}" if self.embed.colour else "#FFFFFF"

	msg_content = discord.ui.TextInput(label="Conteúdo", style=discord.TextStyle.short, required=False)
	embed_title = discord.ui.TextInput(label="Embed Title", style=discord.TextStyle.short)
	embed_description = discord.ui.TextInput(label="Embed Description", style=discord.TextStyle.long)
	embed_color = discord.ui.TextInput(label="Embed Color (e.g., #FFFFFF)", style=discord.TextStyle.short, required=False)

	async def on_submit(self, interaction: discord.Interaction):
		try:
			embed = self.message.embeds[0]
			embed.title = self.embed_title.value
			embed.description = self.embed_description.value

			if self.embed_color.value:
				embed.colour = discord.Color.from_str(self.embed_color.value)

			self.message = await self.message.edit(content=self.msg_content.value, embed=embed, view=EmbedGenerator(self.message))
			await self.message.edit(content=self.msg_content.value, embed=embed, view=EmbedGenerator(self.message))
			await interaction.response.send_message("Texto do Embed atualizado com sucesso!", ephemeral=True)
		except ValueError:
			await interaction.response.send_message(
				content="A cor fornecida é inválida! Use um formato como `#RRGGBB`.",
				ephemeral=True,
			)

class EmbedImageModal(discord.ui.Modal, title="Editar Embed (Imagens e Timestamp)"):
	def __init__(self, message: discord.Message):
		super().__init__()
		self.message = message
		self.embed = message.embeds[0]

		self.embed_thumbnail.default = self.embed.thumbnail.url if self.embed.thumbnail else ""
		self.embed_image.default = self.embed.image.url if self.embed.image else ""
		self.embed_timestamp.default = "True" if self.embed.timestamp else "False"

	embed_thumbnail = discord.ui.TextInput(label="Thumbnail URL", style=discord.TextStyle.short, required=False)
	embed_image = discord.ui.TextInput(label="Imagem URL", style=discord.TextStyle.short, required=False)
	embed_timestamp = discord.ui.TextInput(label="Timestamp (True/False)", style=discord.TextStyle.short)

	async def on_submit(self, interaction: discord.Interaction):
		embed = self.message.embeds[0]

		# Verifica se uma thumbnail foi fornecida e adiciona
		if self.embed_thumbnail.value:
			embed.set_thumbnail(url=self.embed_thumbnail.value)
		
		# Verifica se uma imagem foi fornecida e adiciona
		if self.embed_image.value:
			embed.set_image(url=self.embed_image.value)
		
		# Verifica o valor de timestamp
		if self.embed_timestamp.value.lower() == "true":
			embed.timestamp = discord.utils.utcnow()
		elif self.embed_timestamp.value.lower() == "false":
			embed.timestamp = None

		await self.message.edit(embed=embed, view=EmbedGenerator(self.message))
		await interaction.response.send_message("Imagem e Timestamp do Embed atualizados com sucesso!", ephemeral=True)

class EditButton(discord.ui.Button):
	def __init__(self, message: discord.Message, tipo: int):
		tipos = ["textos", "imagens"]
		self.tipo = tipo
		super().__init__(label="Editar " + tipos[tipo], style=discord.ButtonStyle.blurple, emoji="📝")
		self.message = message

	async def callback(self, interaction: discord.Interaction):
		if self.tipo == 0:
			modal = EmbedTextModal(message=self.message)
		else:
			modal = EmbedImageModal(message=self.message)
		await interaction.response.send_modal(modal)

class FooterModal(discord.ui.Modal, title="Editar Footer do Embed"):
	def __init__(self, message: discord.Message):
		super().__init__()
		self.message = message
		self.embed = message.embeds[0]
		self.embed_footer_text.default = self.embed.footer.text if self.embed.footer else ""
		self.embed_footer_image.default = self.embed.footer.icon_url if self.embed.footer and self.embed.footer.icon_url else ""
	
	embed_footer_text = discord.ui.TextInput(label="Footer Text", style=discord.TextStyle.short, required=False)
	embed_footer_image = discord.ui.TextInput(label="Footer Image URL", style=discord.TextStyle.short, required=False)

	async def on_submit(self, interaction: discord.Interaction):
		try:
			embed = self.message.embeds[0]
			footer_text = self.embed_footer_text.value
			footer_image_url = self.embed_footer_image.value

			# Se o texto e a imagem forem fornecidos, define ambos
			if footer_text and footer_image_url:
				embed.set_footer(text=footer_text, icon_url=footer_image_url)
			elif footer_text:
				embed.set_footer(text=footer_text)
			elif footer_image_url:
				embed.set_footer(icon_url=footer_image_url)

			await self.message.edit(embed=embed)
			await interaction.response.send_message("Footer atualizado com sucesso!", ephemeral=True)
		except Exception as e:
			await interaction.response.send_message(
				content=f"Ocorreu um erro ao tentar atualizar o footer: {str(e)}",
				ephemeral=True,
			)

class FooterButton(discord.ui.Button):
	def __init__(self, message: discord.Message):
		super().__init__(label="Footer", style=discord.ButtonStyle.blurple, emoji="🦶")
		self.message = message

	async def callback(self, interaction: discord.Interaction):
		modal = FooterModal(message=self.message)
		await interaction.response.send_modal(modal)

class FieldModal(discord.ui.Modal, title="Adicionar Field"):
	field_name = discord.ui.TextInput(label="Field Name", style=discord.TextStyle.short)
	field_value = discord.ui.TextInput(label="Field Value", style=discord.TextStyle.long)
	field_inline = discord.ui.TextInput(label="Inline (True/False)", style=discord.TextStyle.short)

	def __init__(self, message: discord.Message):
		super().__init__()
		self.message = message

	async def on_submit(self, interaction: discord.Interaction):
		try:
			inline = self.field_inline.value.lower() == "true"

			embed = self.message.embeds[0]
			embed.add_field(name=self.field_name.value, value=self.field_value.value, inline=inline)

			await self.message.edit(embed=embed, view=EmbedGenerator(self.message))
			await interaction.response.send_message("Field adicionado com sucesso!", ephemeral=True)
		except IndexError:
			await interaction.response.send_message(
				content="Erro: Nenhum embed foi encontrado na mensagem!",
				ephemeral=True,
			)

class SendButton(discord.ui.Button):
	def __init__(self, msg: discord.Message):
		super().__init__(label="Enviar", style=discord.ButtonStyle.green, emoji="✅")
		self.msg = msg

	async def callback(self, interaction: discord.Interaction):
		await self.msg.channel.send(content=self.msg.content, embed=self.msg.embeds[0])
		await interaction.response.send_message("Embed enviado com sucesso!", ephemeral=True)

class CancelButton(discord.ui.Button):
	def __init__(self, msg: discord.Message):
		super().__init__(label="Cancelar", style=discord.ButtonStyle.red, emoji="❌")
		self.msg = msg

	async def callback(self, interaction: discord.Interaction):
		await self.msg.delete()

class AddFieldButton(discord.ui.Button):
	def __init__(self, message: discord.Message):
		super().__init__(label="Adicionar Field", style=discord.ButtonStyle.gray, emoji="➕")
		self.message = message

	async def callback(self, interaction: discord.Interaction):
		modal = FieldModal(message=self.message)
		await interaction.response.send_modal(modal)

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

class EditFieldModal(discord.ui.Modal, title="Editar Field"):
	def __init__(self, message: discord.Message, field_index: int, field_name: str, field_value: str, field_inline: str):
		super().__init__()

		self.message = message
		self.field_index = field_index

		self.field_name = discord.ui.TextInput(label="Nome do Field", default=field_name)
		self.field_value = discord.ui.TextInput(label="Valor do Field", default=field_value, style=discord.TextStyle.paragraph)
		
		self.field_inline = discord.ui.TextInput(label="Inline do Field", default=field_inline, style=discord.TextStyle.paragraph)

		self.add_item(self.field_name)
		self.add_item(self.field_value)
		self.add_item(self.field_inline)

	async def on_submit(self, interaction: discord.Interaction):
		embed = self.message.embeds[0]
		inline = True if self.field_inline.value.lower() == "True" else False 
		embed.set_field_at(self.field_index, name=self.field_name.value, value=self.field_value.value, inline=inline)

		await self.message.edit(embed=embed, view=EmbedGenerator(self.message))
		await interaction.response.send_message("Field atualizado com sucesso!", ephemeral=True)

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
		js_code += f'	color: {embed.colour.value if embed.colour else "null"},\n'
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

class EmbedGenerator(discord.ui.View):
	def __init__(self, msg: discord.Message):
		super().__init__(timeout=None)
		self.add_item(EditButton(msg, 0))
		self.add_item(EditButton(msg, 1))
		self.add_item(FooterButton(msg))
		self.add_item(AddFieldButton(msg))
		self.add_item(SendButton(msg))
		if msg.embeds[0].fields:
			self.add_item(RemoverFieldMenus(msg))
			self.add_item(EditarFieldMenus(msg))
		self.add_item(LinguagemSelect())

class EmbedModelCommands(app_commands.AppCommandGroup):
	def __init__(self, bot: discord.Client):
		super().__init__()
		self.bot = bot

	@app_commands.command(name="embed", description="Cria um embed")
	@app_commands.checks.has_permissions(manage_webhooks=True)
	@app_commands.describe(
		template="Um template do embed que será editado"
	)
	async def embedcmd(self, interaction: discord.Interaction, template: str = None):
		content = "Conteúdo"
		embed = discord.Embed(title="Título", description="Descrição")
		embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
		embed.set_thumbnail(url=interaction.guild.icon.url)
		embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)

		if template:
			try:
				if template.startswith("{") and template.endswith("}"):
					data: dict = json.loads(template)

					embed = discord.Embed(
						title=data.get("title", "Título"),
						description=data.get("description", "Descrição"),
						color=int(data.get("color", "#ffffff").lstrip("#"), 16)
					)
					
					content=data.get("content")

					if "author" in data:
						author = data["author"]
						embed.set_author(
							name=author.get("name", ""),
							url=author.get("url", ""),
							icon_url=author.get("icon_url", "")
						)

					if "thumbnail" in data:
						embed.set_thumbnail(url=data["thumbnail"].get("url", ""))
					
					if "image" in data:
						embed.set_image(url=data["image"].get("url", ""))

					if "footer" in data:
						footer = data["footer"]
						embed.set_footer(
							text=footer.get("text", ""),
							icon_url=footer.get("icon_url", "")
						)

					for field in data.get("fields", []):
						embed.add_field(
							name=field.get("name", "Sem Nome"),
							value=field.get("value", "Sem Valor"),
							inline=field.get("inline", True)
						)
				else:
					template = template.split("/")
					canal = self.bot.get_channel(int(template[-2])) if len(template) > 1 else interaction.channel
					msg = await canal.fetch_message(int(template[-1]))
					embed = msg.embeds[0]
					content = msg.content
			except json.JSONDecodeError:
				return await interaction.response.send_message("O JSON fornecido não é válido. Verifique a formatação.", ephemeral=True)
			except ValueError:
				return await interaction.response.send_message("O template fornecido não é válido. Certifique-se de que contém IDs numéricos ou um JSON correto.", ephemeral=True)
			except discord.NotFound:
				return await interaction.response.send_message("A mensagem ou o canal especificado não foi encontrado.", ephemeral=True)
			except discord.Forbidden:
				return await interaction.response.send_message("O bot não tem permissão para acessar o canal ou a mensagem.", ephemeral=True)
			except Exception as e:
				return await interaction.response.send_message(f"Ocorreu um erro inesperado: {str(e)}", ephemeral=True)
		await interaction.response.defer(ephemeral=True)
		await interaction.followup.send(content=content, embed=embed, ephemeral=True)
		msg = await interaction.original_response()
		await msg.edit(view=EmbedGenerator(msg))