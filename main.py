import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# ============ CONFIGURATION ============
MEMBER_ROLE_NAME = "MEMBER"
VERIFICATION_EMOJI = "✅"

# Menu des rôles : emoji -> nom du rôle
ROLE_MENU = {
    "🛒": "CART",
    "🎫": "SIGN UP",
    "📦": "GEN ACC",
}

# Titres qui servent de "signature" aux messages du bot (ne pas modifier à la légère)
RULES_TITLE = "📋 Règles du Serveur"
WELCOME_TITLE = "🎯 Choisis ton rôle"
ROLES_TITLE = "🎭 Sélection des rôles"
# =======================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


def _norm(emoji: str) -> str:
    """Retire le sélecteur de variation pour comparer les emojis de façon fiable."""
    return emoji.replace("️", "")


ROLE_LOOKUP = {_norm(e): r for e, r in ROLE_MENU.items()}


# ---------- EMBEDS ----------

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
        value="Pas de publicité pour d'autres serveurs tickets.",
        inline=False
    )
    embed.add_field(
        name="✅ Pour continuer",
        value=f"Clique sur {VERIFICATION_EMOJI} ci-dessous pour accepter les règles et accéder au serveur.",
        inline=False
    )
    embed.set_footer(text="Merci de respecter ces règles les Brothers !")
    return embed


def create_welcome_embed(roles_channel):
    embed = discord.Embed(
        title=WELCOME_TITLE,
        description=(
            f"Tu as validé les règles, bienvenue parmi nous !\n\n"
            f"➡️ Rends-toi dans {roles_channel.mention} pour récupérer tes rôles "
            f"et débloquer les salons qui t'intéressent."
        ),
        color=discord.Color.green()
    )
    embed.set_footer(text="Un clic sur un emoji suffit !")
    return embed


def create_roles_embed():
    lignes = "\n".join(f"{emoji} — **{role}**" for emoji, role in ROLE_MENU.items())
    embed = discord.Embed(
        title=ROLES_TITLE,
        description=f"Veuillez choisir votre rôle :\n\n{lignes}",
        color=discord.Color.purple()
    )
    embed.set_footer(text="Clique sur un emoji pour obtenir le rôle • Reclique pour le retirer")
    return embed


# ---------- COMMANDES ----------

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
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"❌ Erreur : {e}")


@bot.command(name="setup_welcome")
@commands.has_permissions(administrator=True)
async def setup_welcome(ctx, salon: discord.TextChannel = None):
    """Poste l'embed qui renvoie vers le salon des rôles.
    Usage : !setup_welcome #rôles"""
    if salon is None:
        await ctx.send("❌ Usage : `!setup_welcome #rôles` (mentionne le salon des rôles)")
        return
    try:
        await ctx.send(embed=create_welcome_embed(salon))
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"❌ Erreur : {e}")


@bot.command(name="setup_roles")
@commands.has_permissions(administrator=True)
async def setup_roles(ctx):
    """Poste le menu de sélection des rôles dans le salon actuel."""
    try:
        message = await ctx.send(embed=create_roles_embed())
        for emoji in ROLE_MENU:
            await message.add_reaction(emoji)
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"❌ Erreur : {e}")


# ---------- LOGIQUE DES RÉACTIONS ----------

async def _identify_menu(payload):
    """Retourne 'rules', 'roles' ou None selon le message réagi.
    Aucun ID stocké en mémoire : ça survit aux redémarrages du bot."""
    if payload.guild_id is None:
        return None
    channel = bot.get_channel(payload.channel_id)
    if channel is None:
        return None
    try:
        message = await channel.fetch_message(payload.message_id)
    except (discord.NotFound, discord.Forbidden, discord.HTTPException):
        return None
    if message.author.id != bot.user.id or not message.embeds:
        return None
    title = message.embeds[0].title
    if title == RULES_TITLE:
        return 'rules'
    if title == ROLES_TITLE:
        return 'roles'
    return None


async def _get_or_create_role(guild, name, color=discord.Color.default()):
    role = discord.utils.get(guild.roles, name=name)
    if role is None:
        role = await guild.create_role(name=name, color=color)
        print(f"✅ Rôle « {name} » créé")
    return role


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    menu = await _identify_menu(payload)
    if menu is None:
        return

    guild = bot.get_guild(payload.guild_id)
    member = payload.member or guild.get_member(payload.user_id)
    if member is None or member.bot:
        return

    emoji = _norm(str(payload.emoji))

    try:
        if menu == 'rules':
            if emoji != _norm(VERIFICATION_EMOJI):
                return
            role = await _get_or_create_role(guild, MEMBER_ROLE_NAME, discord.Color.green())
            await member.add_roles(role, reason="A accepté les règles")
            print(f"✅ {member} → {MEMBER_ROLE_NAME}")
            try:
                await member.send("✅ Bienvenue ! Tu as accepté les règles, tu as maintenant accès au serveur.")
            except discord.Forbidden:
                pass

        elif menu == 'roles':
            role_name = ROLE_LOOKUP.get(emoji)
            if role_name is None:
                return
            role = await _get_or_create_role(guild, role_name)
            await member.add_roles(role, reason="Sélection de rôle")
            print(f"✅ {member} → {role_name}")

    except discord.Forbidden:
        print("❌ Permissions insuffisantes : le rôle du bot doit être AU-DESSUS des rôles qu'il attribue.")
    except Exception as e:
        print(f"❌ Erreur ajout de rôle : {e}")


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == bot.user.id:
        return

    menu = await _identify_menu(payload)
    if menu is None:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    if member is None or member.bot:
        return

    emoji = _norm(str(payload.emoji))

    if menu == 'rules':
        if emoji != _norm(VERIFICATION_EMOJI):
            return
        role_name = MEMBER_ROLE_NAME
    else:
        role_name = ROLE_LOOKUP.get(emoji)
        if role_name is None:
            return

    try:
        role = discord.utils.get(guild.roles, name=role_name)
        if role and role in member.roles:
            await member.remove_roles(role, reason="Réaction retirée")
            print(f"❌ {member} ✂ {role_name}")
    except discord.Forbidden:
        print("❌ Permissions insuffisantes pour retirer le rôle.")
    except Exception as e:
        print(f"❌ Erreur retrait de rôle : {e}")


if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ ERREUR : DISCORD_TOKEN introuvable dans les variables d'environnement.")



# ============ EMBED ACC-GEN ============
# ⬇️ Écris ton texte ici ⬇️
ACCGEN_TITLE = "🎫 Service disponible !"
ACCGEN_TEXT = (
    "On peut vous générer des comptes Ticketmaster"
    "Ticketmaster FR 🇫🇷"
    "Ticketmaster US 🇺🇸"
    "➡️ Ouvre un ticket ci-dessous pour plus d'infos."
)
ACCGEN_COLOR = discord.Color.green()   # ou .blue() .red() .gold() .purple()
# =======================================


@bot.command(name="setup_accgen")
@commands.has_permissions(administrator=True)
async def setup_accgen(ctx):
    """Poste l'embed du service dans le salon actuel."""
    try:
        embed = discord.Embed(
            title=ACCGEN_TITLE,
            description=ACCGEN_TEXT,
            color=ACCGEN_COLOR
        )
        await ctx.send(embed=embed)
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"❌ Erreur : {e}")
