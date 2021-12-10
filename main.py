# import the needed libraries
import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

# create connection with discord
client = discord.Client()

# save different sets of words in lists for bot to recognize 
greet_words = ["Hello", "Hi", "Hey"]

bye_words = ["Bye", "Goodbye", "Talk to you later"]

help_words = ["help", "information", "instructions", "i do not know", "confused"]

down_words = ["unmotivated", "tired", "exhausted","giving up", "done"]

# instructions to give user
instructions = 'I am the motivational bot! Ask me for a famous quote for some motivation or tell me if you are feeling tired, exhausted, etc for some encouragement! For a complete list of my motivating messages, use the "list" command. If you would like to add to my list of encouragements used, use the "new" command followed my a new motivating message. If you would like to delete from my list of encouragements, use the "delete" command followed the index of the message you wish to remove.'

# motivational phrases that bot starts with 
starter_motivations = ["Take it day by day.", "You are doing great!", "Hang in there!"]

# this function pulls a quote from the quotable api address and returns it.  Quotable is a website from Salesforce with a plethora of quotes accessible through its API 
def get_quote():
  response = requests.get("https://api.quotable.io/random")
  # use json to extract the quote content and author
  json_data = json.loads(response.text)
  quote = json_data['content'] + " -" + json_data['author']
  return(quote)

# this function adds new phrases to the starter_motivations list using append() 
def update_motivations(motivating_message):
  if "motivations" in db.keys():
    motivations = db["motivations"]
    motivations.append(motivating_message)
    db["motivations"] = motivations
  else: 
    db["motivations"] = [motivating_message]

# this function removes phrases from the motivations list using the index of the phrase
def delete_motivations(index):
  motivations = db["motivations"]
  if len(motivations) > index:
    del motivations[index]
    db["motivations"] = motivations

# this function indicates in the server that the bot has accessed the discord server
@client.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# this function includes all of the bot response functionality
@client.event
async def on_message(message):
    # do not respond if the message is from the both
    if message.author == client.user:
        return
    
    # save message.content as msg for short-hand
    msg = message.content

    # if the user uses any greeting in the greet_words list, respond with Hello there!
    if any(word in msg for word in greet_words):
      await message.channel.send("Hello there!")

    # if the user uses any term in the bye_words list, respond with Goodbye!
    if any(word in msg for word in bye_words):
      await message.channel.send("Goodbye!")

    # if the user asks for help in any of the help words, respond with the instructions
    if any(word in msg for word in help_words):
      await message.channel.send(instructions)

    # create options as the starting motivations and data base 
    options = starter_motivations
    if "motivations" in db.keys():
      options = options + db["motivations"].value

    # if any user word is in the "down words" list, respond with a motivational phrase from options
    if any(word in msg for word in down_words):
      await message.channel.send(random.choice(options))

    # if the user uses the new command, add the following new phrase to the motvation database 
    if msg.startswith("new"):
      motivating_message = msg.split("new ", 1)[1]
      update_motivations(motivating_message)
      await message.channel.send("The new motivating message has been added!")

    # if the user uses the delete command, remove the phrase at the given index and respond with the remaining phrases
    if msg.startswith("delete"):
      motivations = []
      if "motivations" in db.keys():
        index = int(msg.split("delete", 1)[1])
        delete_motivations(index)
        motivations = db["motivations"].value + options
      await message.channel.send(motivations)

    # if the user uses the list command, list out all of the motivational phrases known
    if msg.startswith("list"):
      if "motivations" in db.keys():
        motivations = db["motivations"].value + options
      await message.channel.send(motivations)

    # if the user includes the term quote, give them a quote for motivation
    if 'quote' in msg:
        quote = get_quote()
        await message.channel.send(quote)

# keep alive calls a function that continuously calls the bot so that it does not go to sleep 
keep_alive()

# use my bot's token to access my bot's abilities 
client.run(os.getenv('TOKEN'))