import discord
from discord import app_commands
import json

class EmbedGenerator(discord.ui.View):
	def __init__(self, msg: discord.Message):
		from .menus import EditarFieldMenus, RemoverFieldMenus, LinguagemSelect
		from .buttons import EditButton, FooterButton, AddFieldButton, SendButton
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

class EmbedModelCommands(app_commands.Group):
	def __init__(self, bot: discord.Client):
		super().__init__(name="embed", description="Comandos padrões de embeds.")
		self.bot = bot

	@app_commands.command(name="create", description="Cria um embed")
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
	
	@app_commands.command(name="json", description="Ajuda com o modelo JSON dos embeds")
	async def json_help(self, interaction: discord.Interaction):
		embed = discord.Embed(
			title="📖 Como usar os modelos JSON de embeds",
			description="Aqui está um exemplo de como montar um template JSON para o comando `/embed create`:",
			colour=discord.Color.blurple()
		)

		exemplo_json = """```json
{
	"title": "Título do Embed",
	"description": "Descrição do Embed",
	"color": "#5865F2",
	"content": "Mensagem fora do embed",
	"author": {
		"name": "Autor",
		"url": "https://example.com",
		"icon_url": "https://link-da-imagem.com/icon.png"
	},
	"thumbnail": {
		"url": "https://link-da-imagem.com/thumb.png"
	},
	"image": {
		"url": "https://link-da-imagem.com/image.png"
	},
	"footer": {
		"text": "Rodapé",
		"icon_url": "https://link-da-imagem.com/footer.png"
	},
	"fields": [
		{
		"name": "Campo 1",
		"value": "Valor do campo 1",
		"inline": true
		},
		{
		"name": "Campo 2",
		"value": "Valor do campo 2",
		"inline": false
		}
	]
}
	```"""

		embed.add_field(name="📝 Exemplo de JSON", value=exemplo_json, inline=False)
		embed.add_field(
			name="ℹ️ Observações",
			value="• Os campos `author`, `thumbnail`, `image`, `footer` e `fields` são opcionais.\n"
				"• A cor deve estar em formato hexadecimal (`#RRGGBB`).\n"
				"• Você também pode usar o link de uma mensagem como template no comando `/embed create`.",
			inline=False
		)

		await interaction.response.send_message(embed=embed, ephemeral=True)
