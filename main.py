import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# ---------- Configuration ----------
MEMBER_ROLE_NAME = "MEMBER"
VERIFICATION_EMOJI = "✅"
RULES_TITLE = "📋 Règles du Serveur"   # sert de "signature" pour reconnaître le message
# -----------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


def create_rules_embed():
    embed = discord.Embed(
        title=RULES_TITLE,
        description="Bienvenue sur RICHNESS ! Avant d'accéder aux autres salons, tu dois accepter les règles.",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="1️⃣ Respect",
        value="Sois respectueux avec tous les membres. Pas d'insultes, de discrimination ou de harcèlement.",
        inline=False
    )
    embed.add_field(
        name="2️⃣ Pas de spam",
        value="Ne spam pas les messages, les mentions ou les émojis.",
        inline=False
    )
    embed.add_field(
        name="3️⃣ Publicité interdite",
        value="Pas de publicité pour d'autres serveurs de tickets",
        inline=False
    )
    embed.add_field(
        value=f"Clique sur {VERIFICATION_EMOJI} ci-dessous pour accepter les règles et accéder au serveur.",
        inline=False
    )
    embed.set_footer(text="Merci de respecter ces règles les brothers !")
    return embed


@bot.event
async def on_ready():
    print(f'✅ Bot connecté en tant que {bot.user}')


@bot.command(name="setup_rules")
@commands.has_permissions(administrator=True)
async def setup_rules(ctx):
    """Poste l'embed des règles dans le salon actuel."""
    try:
        message = await ctx.send(embed=create_rules_embed())
        await message.add_reaction(VERIFICATION_EMOJI)
        await ctx.send(
            f"✅ Règles postées. Les membres peuvent cliquer sur {VERIFICATION_EMOJI} "
            f"pour recevoir le rôle **{MEMBER_ROLE_NAME}**.",
            delete_after=15
        )
    except Exception as e:
        await ctx.send(f"❌ Erreur : {e}")


async def _is_rules_message(payload):
    """Vérifie que la réaction est bien sur un message de règles posté par le bot.
    Aucun ID n'est stocké en mémoire : ça survit aux redémarrages."""
    if payload.emoji.name != VERIFICATION_EMOJI:
        return False
    if payload.guild_id is None:
        return False
    channel = bot.get_channel(payload.channel_id)
    if channel is None:
        return False
    try:
        message = await channel.fetch_message(payload.message_id)
    except (discord.NotFound, discord.Forbidden):
        return False
    if message.author.id != bot.user.id:
        return False
    return bool(message.embeds) and message.embeds[0].title == RULES_TITLE


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    if not await _is_rules_message(payload):
        return

    guild = bot.get_guild(payload.guild_id)
    member = payload.member or guild.get_member(payload.user_id)
    if member is None or member.bot:
        return

    try:
        role = discord.utils.get(guild.roles, name=MEMBER_ROLE_NAME)
        if role is None:
            role = await guild.create_role(name=MEMBER_ROLE_NAME, color=discord.Color.green())
            print(f"✅ Rôle {MEMBER_ROLE_NAME} créé")

        await member.add_roles(role, reason="A accepté les règles")
        print(f"✅ {member} a accepté les règles → rôle {MEMBER_ROLE_NAME}")

        try:
            await member.send("✅ Bienvenue ! Tu as accepté les règles, tu as maintenant accès au serveur.")
        except discord.Forbidden:
            pass

    except discord.Forbidden:
        print("❌ Permissions insuffisantes : le rôle du bot doit être AU-DESSUS de MEMBER.")
    except Exception as e:
        print(f"❌ Erreur ajout de rôle : {e}")


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user.id:
        return
    if not await _is_rules_message(payload):
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member is None:
        return

    try:
        role = discord.utils.get(guild.roles, name=MEMBER_ROLE_NAME)
        if role and role in member.roles:
            await member.remove_roles(role, reason="A retiré sa validation des règles")
            print(f"❌ {member} a retiré le rôle {MEMBER_ROLE_NAME}")
    except Exception as e:
        print(f"❌ Erreur retrait de rôle : {e}")


if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ ERREUR : DISCORD_TOKEN introuvable dans les variables d'environnement.")
