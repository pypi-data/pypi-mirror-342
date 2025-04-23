import discord
from .modals import FieldModal, FooterModal, EmbedTextModal, EmbedImageModal

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

class FooterButton(discord.ui.Button):
	def __init__(self, message: discord.Message):
		super().__init__(label="Footer", style=discord.ButtonStyle.blurple, emoji="🦶")
		self.message = message

	async def callback(self, interaction: discord.Interaction):
		modal = FooterModal(message=self.message)
		await interaction.response.send_modal(modal)

class SendButton(discord.ui.Button):
	def __init__(self, msg: discord.Message):
		super().__init__(label="Enviar", style=discord.ButtonStyle.green, emoji="✅")
		self.msg = msg

	async def callback(self, interaction: discord.Interaction):
		embed = self.msg.embeds[0]
		embed.timestamp = discord.utils.utcnow() if embed.timestamp else None
		await self.msg.channel.send(content=self.msg.content, embed=embed)
		await interaction.response.send_message("Embed enviado com sucesso!", ephemeral=True)

class AddFieldButton(discord.ui.Button):
	def __init__(self, message: discord.Message):
		super().__init__(label="Adicionar Field", style=discord.ButtonStyle.gray, emoji="➕")
		self.message = message

	async def callback(self, interaction: discord.Interaction):
		modal = FieldModal(message=self.message)
		await interaction.response.send_modal(modal)
