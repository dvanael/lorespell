import discord
import random
from decouple import config

# Coloque o token do bot aqui
TOKEN = config("TOKEN")

# Configuração dos intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)


# Função para rolar os dados
def rolar_dados(qtd, faces):
    return [random.randint(1, faces) for _ in range(qtd)]


# Dicionário com magias de D&D
magias = {
    "bola de fogo": {
        "nível": "3º nível",
        "escola": "Evocação",
        "tempo_conjuração": "1 ação",
        "alcance": "45 metros",
        "componentes": "V, S, M (uma pequena bola de guano de morcego e enxofre)",
        "duração": "Instantânea",
        "dano": lambda: rolar_dados(8, 6),  # Rola 8d6
        "descrição": "Um feixe brilhante lampeja de seu dedo indicador para um ponto que você escolher dentro do alcance e então explode com um estampido baixo, explodindo em chamas.",
    },
    "mísseis mágicos": {
        "nível": "1º nível",
        "escola": "Evocação",
        "tempo_conjuração": "1 ação",
        "alcance": "36 metros",
        "componentes": "V, S",
        "duração": "Instantânea",
        "dano": lambda: [
            random.randint(1, 4) + 1 for _ in range(3)
        ],  # 3 dardos de 1d4+1
        "descrição": "Três dardos mágicos brilham e atingem os alvos automaticamente.",
    },
}


@client.event
async def on_ready():
    print(f"Bot {client.user} está online!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    comando = message.content.lower()

    if comando.startswith("!magia "):
        nome_magia = comando.replace("!magia ", "").strip()
        if nome_magia in magias:
            magia = magias[nome_magia]
            dano = magia["dano"]()
            total_dano = sum(dano)

            embed = discord.Embed(
                title=f"✨ {nome_magia.capitalize()}",
                description=magia["descrição"],
                color=discord.Color.red(),
            )
            embed.add_field(name="🔹 Nível", value=magia["nível"], inline=True)
            embed.add_field(name="🔹 Escola", value=magia["escola"], inline=True)
            embed.add_field(
                name="🔹 Tempo de Conjuração",
                value=magia["tempo_conjuração"],
                inline=False,
            )
            embed.add_field(name="🔹 Alcance", value=magia["alcance"], inline=True)
            embed.add_field(
                name="🔹 Componentes", value=magia["componentes"], inline=True
            )
            embed.add_field(name="🔹 Duração", value=magia["duração"], inline=True)
            embed.add_field(
                name="🔥 Dano Causado",
                value=f"{total_dano} de dano ({' + '.join(map(str, dano))})",
                inline=False,
            )

            await message.channel.send(embed=embed)
        else:
            await message.channel.send("🔮 Essa magia não está no meu grimório!")


client.run(TOKEN)
