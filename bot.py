import asyncio
import random
import time
from paroliamo import find as parofind

import discord
from discord.ext import commands

ROUND_NUM = 3
ROUND_TIME = 10
REST_TIME = 10

with open('paroliamo.txt', 'r') as f:
    treccani = [tuple(w[:-1].split(' ')) for w in f.readlines()]


def generate_letters():
    ret = list()
    for i in range(2):
        for j in range(5):
            p = ['e', 'a', 'i', 'o', 'u'] if i == 1 else \
                ['b', 'c', 'd', 'f', 'g', 'h', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'z']
            w = [11.79, 11.74, 11.28, 9.83, 3.01] if i == 1 else \
                [.92, 4.5, 3.73, .95, 1.64, 1.54, 6.51, 2.51, 6.88, 3.05, .51, 6.37, 4.98, 5.62, 2.10, .49]
            ret.append(random.choices(population=p, weights=w)[0])
    return ret


def is_valid_word(w, l, done):
    if w in done:
        return False
    tmp_l = [ch for ch in l]
    for ch in w:
        if ch not in tmp_l:
            return False
        tmp_l.remove(ch)
    return w in [entry[1] for entry in treccani]


with open('token_testing.txt', 'r') as f:
    TOKEN = f.read()

bot = discord.ext.commands.Bot(command_prefix='')


@bot.event
async def on_ready():
    print('ready')


def print_scores(s):
    return '\n'.join(f'{p}: {s[p]}p' for p in s)


@bot.command(aliases=["start"])
async def play(ctx):
    scores = dict()
    for i in range(ROUND_NUM):
        await ctx.send(embed=discord.Embed(title=f'**Round {i + 1}/3**'))
        await ctx.send(f'Si inizia fra {REST_TIME}s')
        await asyncio.sleep(REST_TIME)
        round_scores = await play_round(ctx)
        for s in round_scores:
            if s not in scores:
                scores[s] = 0
            scores[s] += round_scores[s]
        if i + 1 < ROUND_NUM:
            await ctx.send(f'**Risultati parziali\n{print_scores(scores)}**')
    await ctx.send(embed=discord.Embed(title=f'Risultati finali\n{print_scores(scores)}'))


async def play_round(ctx):
    letters = generate_letters()
    emoji_letters = ' '.join(f':regional_indicator_{ch}:' for ch in letters)
    await ctx.send('via!\n ' + emoji_letters[:114] + '\n' + emoji_letters[114:])
    start = time.time()
    scores = dict()
    already_done = set()
    while True:
        try:
            msg = await bot.wait_for('message',
                                     check=lambda m: is_valid_word(m.content, letters, already_done),
                                     timeout=ROUND_TIME - (time.time() - start))
            already_done.add(msg.content)
            usr = msg.author.name
            if usr not in scores:
                scores[usr] = 0
            scores[usr] = max(scores[usr], len(msg.content))
            await ctx.send(f'{usr}: {len(msg.content)} punti (max: {scores[usr]})')
            await ctx.send(f'**Tempo rimasto: {ROUND_TIME - (int(time.time() - start))}s**')
        except asyncio.TimeoutError:
            await ctx.send(f'Round terminato.\nLe parole migliori: **{", ".join(parofind(letters, auto=True))}**')
            break
    return scores


bot.run(TOKEN)
