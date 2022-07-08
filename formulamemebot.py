from cgitb import text
from itertools import count
import random
import time
from io import BytesIO

import os
from dotenv import load_dotenv
import telebot
from PIL import Image
import praw
import requests

load_dotenv(override=True)

api = (os.getenv('API_KEY'))
cid = (os.getenv('CLIENT_ID'))
cse = (os.getenv('CLIENT_SECRET'))
un = (os.getenv('USERNAME'))
pw = (os.getenv('PASSWORD'))
bot = telebot.TeleBot(api)


reddit = praw.Reddit(client_id = cid,
                     client_secret = cse,
                     username = un,
                     password = pw,
                     user_agent = "joo")


def get_post(rddt, sbrddt, first_x_posts = 100):
  subreddit = rddt.subreddit(sbrddt)
  hot = subreddit.hot(limit=first_x_posts)
  post = random.choice(list(hot))
  return post


# f1 in any part in the message and the bot sends a meme from FormulaDank to the group
@bot.message_handler(func=lambda message: message.text is not None and 'f1' in message.text)
def send_post(message):
  post = get_post(rddt=reddit, sbrddt="formuladank")
  try:
    response = requests.get(post.url)
    img = Image.open(BytesIO(response.content))
    bot.send_photo(message.chat.id, img, caption=post.title)
  except Exception as e:
   if "cannot identify image file <_io.BytesIO object at" in str(e):
            bot.send_message(message.chat.id, f"{post.url}\n{post.title}")


# When username "Saarikeisari" messages to the group with "1337", the bot answers with a meme from the Formuladank subreddit
@bot.message_handler(func=lambda message: message.text is not None and '1337' in message.text and message.from_user.username == "Saarikeisari")
def send_post(message):
  post = get_post(rddt=reddit, sbrddt="formuladank")
  try:
    response = requests.get(post.url)
    img = Image.open(BytesIO(response.content))
    bot.send_photo(message.chat.id, img, caption=post.title)
  except Exception as e:
   if "cannot identify image file <_io.BytesIO object at" in str(e):
            bot.send_message(message.chat.id, f"{post.url}\n{post.title}")


# When messages are edited in the group, the bot answers with "Sakkoo :D"
@bot.edited_message_handler(func=lambda message: message.text is not None)
def send_edit_message(message):
  bot.send_message(chat_id=message.chat.id, text="Sakkoo :D")


bot.polling()