import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration
MEMBER_ROLE_NAME = "MEMBER"
VERIFICATION_EMOJI = "✅"
RULES_MESSAGE_ID = None
RULES_CHANNEL_ID = None

# Embed des règles
def create_rules_embed():
    embed = discord.Embed(
        title="📋 Règles du Serveur",
        description="Bienvenue sur notre serveur Discord ! Avant d'accéder aux autres salons, tu dois accepter les règles.",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="1️⃣ Respect",
        value="Sois respectueux avec tous les membres. Pas d'insultes, de discrimination ou de harcèlement.",
        inline=False
    )
    embed.add_field(
        name="2️⃣ Pas de Spam",
        value="Ne spam pas les messages, les mentions ou les émojis.",
        inline=False
    )
    embed.add_field(
        name="3️⃣ Pas de Contenu Illégal",
        value="Aucun contenu illégal, NSFW excessif ou dangereux.",
        inline=False
    )
    embed.add_field(
        name="4️⃣ Publicité Interdite",
        value="Pas de publicité pour d'autres serveurs ou produits sans permission.",
        inline=False
    )
    embed.add_field(
        name="5️⃣ Suivre les Modérateurs",
        value="Respecte les décisions des modérateurs et administrateurs.",
        inline=False
    )
    embed.add_field(
        name="✅ Pour Continuer",
        value=f"Clique sur l'emoji {VERIFICATION_EMOJI} ci-dessous pour accepter et accéder au serveur !",
        inline=False
    )

    embed.set_footer(text="Merci de respecter ces règles !")
    return embed

@bot.event
async def on_ready():
    print(f'✅ Bot connecté en tant que {bot.user}')
    try:
        await bot.tree.sync()
        print("✅ Commandes synchronisées")
    except Exception as e:
        print(f"❌ Erreur sync: {e}")

# Commande pour poster l'embed des règles
@bot.command(name="setup_rules")
@commands.has_permissions(administrator=True)
async def setup_rules(ctx):
    """Poste l'embed des règles dans le salon actuel"""
    try:
        global RULES_MESSAGE_ID, RULES_CHANNEL_ID

        embed = create_rules_embed()
        message = await ctx.send(embed=embed)

        # Ajoute la réaction
        await message.add_reaction(VERIFICATION_EMOJI)

        # Sauvegarde les IDs
        RULES_MESSAGE_ID = message.id
        RULES_CHANNEL_ID = ctx.channel.id

        await ctx.send(f"✅ Embed des règles posté ! Les utilisateurs peuvent maintenant cliquer sur {VERIFICATION_EMOJI}")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {e}")

# Système de réaction automatique
@bot.event
async def on_raw_reaction_add(payload):
    """Quand quelqu'un ajoute une réaction"""
    # Ignore les réactions du bot
    if payload.user_id == bot.user.id:
        return

    # Vérifie si c'est la bonne réaction sur le bon message
    if payload.emoji.name != VERIFICATION_EMOJI:
        return

    if payload.message_id == RULES_MESSAGE_ID and payload.channel_id == RULES_CHANNEL_ID:
        try:
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            # Trouve ou crée le rôle MEMBER
            role = discord.utils.get(guild.roles, name=MEMBER_ROLE_NAME)
            if not role:
                role = await guild.create_role(name=MEMBER_ROLE_NAME, color=discord.Color.green())
                print(f"✅ Rôle {MEMBER_ROLE_NAME} créé")

            # Ajoute le rôle au membre
            await member.add_roles(role)
            print(f"✅ {member.name} a accepté les règles et reçu le rôle {MEMBER_ROLE_NAME}")

            # Message de confirmation en DM (optionnel)
            try:
                await member.send(f"✅ Bienvenue ! Tu as été vérifié et as accès à tous les salons du serveur !")
            except:
                pass

        except Exception as e:
            print(f"❌ Erreur lors de l'ajout du rôle: {e}")

@bot.event
async def on_raw_reaction_remove(payload):
    """Quand quelqu'un retire une réaction"""
    if payload.user_id == bot.user.id:
        return

    if payload.emoji.name != VERIFICATION_EMOJI:
        return

    if payload.message_id == RULES_MESSAGE_ID and payload.channel_id == RULES_CHANNEL_ID:
        try:
            guild = bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            role = discord.utils.get(guild.roles, name=MEMBER_ROLE_NAME)
            if role:
                await member.remove_roles(role)
                print(f"❌ {member.name} a retiré le rôle {MEMBER_ROLE_NAME}")
        except Exception as e:
            print(f"❌ Erreur lors du retrait du rôle: {e}")

# Lance le bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ ERREUR: DISCORD_TOKEN non trouvé! Ajoute-le à tes variables d'environnement.")
