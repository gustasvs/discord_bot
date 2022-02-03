import discord
import sys
import time
import datetime
from random import choice
import asyncio
import string
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import io

global chatbot_version
chatbot_version = 4

# #chatbot_v3
if chatbot_version == 3:
    from inference import process_questions
    process_questions(f"test")

# chatbot_v4
if chatbot_version == 4:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
    print("Loaded tokenizer")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
    print("Loaded model")

client = discord.Client()

token = open("token.txt", "r").read()
global admin_name
global admin_required
global current_guild_id

last_bot_answer = ""
current_guild_id = 619226759115571221
admin_required = True
admin_name = "gustasvs"
bot_name = "super bots v4"

chat_step = 0

sasveicinasanas = []
with open("sasveicinasanas.txt", "r") as f:
    for line in f:
        sasveicinasanas.append(str(line)[:-1])

def community_report(guild):
    online = 0
    afk = 0
    offline = 0
    for mem in guild.members:
        if str(mem.status) == "online":
            online += 1
        if str(mem.status) == "offline":
            offline += 1
        else:
            afk += 1
    return online, afk, offline

def message_acceptable(message):
    if message.author.name != bot_name and str(message.content)[0] != "!":
        return True
    return False

def randomize_text(bot_answer):
    cip = random.randint(0, 7)
    if cip == 1:
        bot_answer += "*"
        bot_answer = "*" + bot_answer
    if cip == 2:
        bot_answer += "**"
        bot_answer = "**" + bot_answer
    if cip == 3:
        bot_answer += "***"
        bot_answer = "***" + bot_answer
    if cip == 4:
        random_emoji = random.choice([":smirk:", ":man_facepalming:", ":woman_facepalming:", 
        ":chart_withdownwards_trend:", ":yum:", ":star_struck:", ":sob:", ":stuck_out_tongue_closed_eyes:", 
        ":ok_hand:", ":partying_face:", ":rainbow:", ":boom:"])
        bot_answer += " " + random_emoji
    return bot_answer

def random_answer(message):
    return random.choice(["***adios amigos***", f"adios <@{message.author.id}>", 
                        "*You are not funny.*", "ahhaha... man iet labi pastaasti kaa iet tev? (ar kājām?)", f"why is {message.author.name} so annoying?", 
                        ":smirk:", ":smirk:", ":man_facepalming:", ":woman_facepalming:", ":chart_withdownwards_trend", 
                        f"please kick {message.author.name} from here...", f"I think that {message.author.name} is gay."])

@client.event
async def on_ready():
    global current_guild
    current_guild = client.get_guild(current_guild_id)

    print(f"server name - {current_guild}")
    print(f"client info - {client.user}")

    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="Teletubbies"))


@client.event
async def on_message(message):
    msg = message.content
    tagged = False
    if "<@!696057995125194792>" in msg:
        msg = msg[23:]
        tagged = True
    global current_guild
    global admin_name
    global admin_required

    message_stats = f"{message.channel}/{message.author} - {msg}"
    with io.open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{message_stats}\n")
    
    if message_acceptable(message):

        await message.channel.trigger_typing()
        # for mes in sasveicinasanas:
        #     if mes == msg.lower():
        #         messageee = choice([f"bonjour {message.author.name}", "buenos dias", f"buenos dias {message.author.name}", f"sup {message.author.name}", "labas vakaras moi latgalīsu drauks", "yo, whats up?", "YO KAS LABS?", "man iet labi pastaasti kaa iet tev? (ar kājām?)", f"wyd {message.author.name}?", str(mes) + f" {message.author.name} xd !!!"])
        #         await message.channel.send(messageee)
        #         break

        if ("glogout" == msg.lower()):
            if message.author.name == admin_name or admin_required == False:
                await message.channel.send(f"**logging out...**")
                await client.close()
                exit(0)
            else:
                await message.channel.send(f"**permission denied**")

        elif "gcrash" == msg.lower():
            if message.author.name == admin_name or admin_required == False:
                letters = string.ascii_lowercase + string.ascii_uppercase
                mes = ""
                for e in range(random.randint(4, 12)):
                    streng = ''.join(random.choice(letters) for i in range(random.randint(2, 20)))
                    if random.randint(1, 2) == 1:
                        cip = random.randint(1, 3)
                        if cip == 1:
                            streng = "*" + streng
                            streng += "*"
                        if cip == 2:
                            streng = "**" + streng
                            streng += "**"
                        if cip == 3:
                            streng = "***" + streng
                            streng += "***"

                    mes += streng
                    mes += '\n'
                await message.channel.send(mes)
                await message.channel.send("*error 0x0000003b*\nquitting aplication\n***quitti***\n*ng ap*")
                await client.close()
                sys.exit()
            else:
                await message.channel.send(f"**permission denied**")

        elif "ghelp" in msg.lower():
            await message.channel.send("```gspam - gspam @kuru\ncik on - cik on serveri\nkas on - kuri tiesi on\ncik vispar - cik vispar serveri dalibnieku\nglogout - izslegt botu\njebkura cita zina - bots pats izdoma ko atbildeet :D```")

        elif "gspam" in msg.lower():
            mention_id = message.mentions[0].id
            target = client.get_user(mention_id)
            saturs = message.content[10 + len(str(mention_id)):]
            await message.channel.send(f"Spamming <@{mention_id}>")
            for j in range(5):
                await target.send(f"<@{mention_id}> message from {message.author.name} \n-->       ***{saturs}***        <--")

        elif "cik on" in msg.lower():
            online, afk, offline = community_report(current_guild)
            await message.channel.send(f"```Online - {online + afk}\nOffline - {offline}```")

        elif "kas on" in msg.lower():
            on = []
            for mem in current_guild.members:
                if str(mem.status) != "offline":
                    on.append(mem.name.lower())
            on.sort()
            messageee = str()
            for mem in on:
                messageee += str(mem) + "\n"
            await message.channel.send(f"```{messageee}```")

        elif "cik vispar" in msg.lower():
            await message.channel.send(f"```{current_guild.member_count}```")

        else:

            if chatbot_version == 3:

                answers_list = process_questions(msg)

                answerss = []
                best_score = 0

                for index, answer in enumerate(answers_list):
                    if answer['best_score'] == None: # ja botsd nevar izdomat kkada imeesla deel...
                        answerss.append(random_answer(message))
                    else:
                        best_score = int(answer['best_score'])
                        for e in range(len(answer['answers'])):
                            answ = answer['answers'][e]
                            scor = int(answer['scores'][e])
                            if str(answ[-1]).isalpha():
                                answ = str(answ) + "."
                            answ.capitalize()
                            print(answ)
                            for j in range(scor):
                                answerss.append(answ)
                                
                        
                print(len(answerss), best_score)
                bot_answer = random.choice(answerss)

                bot_answer = randomize_text(bot_answer)            

                if tagged:
                    await message.channel.send(f"<@{message.author.id}> {bot_answer}") 
                else:
                    await message.channel.send(bot_answer) 
            
            if chatbot_version == 4:    
                global chat_step
                global last_bot_answer
                global bot_input_ids
                global chat_history_ids
                new_user_input_ids = tokenizer.encode(msg + tokenizer.eos_token, return_tensors='pt')
                if chat_step == 0:
                    bot_input_ids = new_user_input_ids
                else:
                    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
                chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
                
                bot_answer = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
                
                if bot_answer == last_bot_answer or 'not sure' in bot_answer.lower():
                    chat_step = 0
                    bot_answer = random_answer(message)
                else:
                    bot_answer = randomize_text(bot_answer)
                    # chat_step += 1

                print(bot_answer)
                
                last_bot_answer = bot_answer
                await message.channel.send(bot_answer)
                


client.run(token)