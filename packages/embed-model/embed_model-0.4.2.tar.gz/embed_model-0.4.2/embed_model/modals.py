import discord
from .menus import EmbedGenerator

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