import discord
import os
from replit import db
from discord.ext import commands
from webserver import keep_alive
lists=[]
class lis:
    def __init__(self,key,description):
        self.key=key
        self.description=description
        self.items=[] 
    def getItems(self):
      s=self.key+"\n"+self.description+"\n"
      for i in range(0,len(self.items)):
        s=s+str(i+1)+": "+self.items[i]+"\n"
      return s
    def removeFromList(self,item):
      self.items.remove(item)
    def setItems(self,items):
      self.items=items
    def addToList(self,item):
      self.items.append(item)
    def isinList(self,item):
      return
    def toString(self):
      return self.key+", items: "+str(len(self.items))+"\n"+self.description+"\n"
    def printList(self):
      s=self.toString()
      for i in range(0,len(self.items)):
        s=s+(i+1)+": "+self.items[i]
def help():
  #!lis is call
  #help is this
  #create new list (key);(description)
  #delete (item);(key)
  #show lists
  #show (key)
  return "!list is the call\ncreate new list (key) ; (description)-adds a list using (key) as an id and (description) as guidence\ndelete (key)-deletes list\nadd (item) ;to (key)-adds (item) from list with that (key)\ndelete (item) ;from (key)-deletes (item) from list with that (key)\nshow lists-shows the keys of every list\nshow (key)-shows the list with that key"
def createList(key, desc):
  lists.append(lis(key,desc))
  print(key)
  print(desc)
  saveLists()
def removeList(num):
  lists.pop(num)
  saveLists()
def removeFormList(item, index):
  #add error catch for not in list
  lists[index].items.remove(item)
  saveLists()
def saveLists():
  k=[]
  d=[]

  for i in range(0, len(lists)):
    k.append(lists[i].key)
    d.append(lists[i].description)
    db[lists[i].key]=lists[i].items
  db["keys"]=k
  db["description"]=d
def loadLists():
  k=db["keys"]
  d=db["description"]
  for i in range(0,len(k)):
    l=(lis(k[i],d[i]))
    print("key: "+k[i])
    print("description: "+d[i])
    l.setItems(db[k[i]])
    print(l.getItems())
    lists.append(l)
def showLists():
  if len(lists) > 0:
    s="there are no lists"
  else:
    s="Lists:\n"
    for i in range(0, len(lists)):
      s=s+str(i+1)+". "+lists[i].toString()
  return s
def indexOfList(name):
  for i in range(0, len(lists)):
    if(lists[i].key == name):
      return i
  return -1
description = "desc"
intent = discord.Intents.default()
intent.members = True
bot = commands.Bot(command_prefix='!lis', description=description, intent=intent)
#startup command
@bot.event
async def on_ready():
    loadLists()
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
@bot.event
async def on_message(message):
    mess=message.content.split()
    if message.author==bot.user:
        return
    if(message.content.startswith('!list')):
      if('help' in message.content):
        await message.channel.send(help())
      elif('create' in message.content and ';' in message.content):
        key=" ".join(mess[2:mess.index(';')])#correct error given with no spaces
        desc=" ".join(mess[mess.index(';')+1:])
        if key in db.keys():
          await message.channel.send(key+" list already exists")
        else:
          createList(key,desc)
          await message.channel.send(key+" list has been created")
      elif(' add ' in message.content and ';to ' in message.content):
        #check if exsists
        l=" ".join(mess[mess.index(';to')+1:])
        item=" ".join(mess[mess.index('add')+1:mess.index(';to')])
        index=indexOfList(l)
        print("list :"+l)
        print("item :"+item)
        if index>=0:
          #print
          lists[index].addToList(item)
          await message.channel.send(item+" has been added to "+ l)
        else:
          await message.channel.send("that is not a list")
      elif('delete ' in message.content):
        if(';from' in message.content):
          l=" ".join(mess[mess.index(';from')+1:])
          item=" ".join(mess[mess.index('delete')+1:mess.index(';from')])
          index=indexOfList(l)
          if index>=0:
            removeFormList(item,index)
            await message.channel.send(item+" has been deleted from "+l)
          else:
            await message.channel.send("that is not a list")
        else:
          l=" ".join(mess[mess.index('delete')+1:])
          index=indexOfList(l)
          if index>=0:
            removeList(index)
            await message.channel.send(l+" list has been deleted")
          else:
            await message.channel.send(l+" is not a list")
      elif('show lists' in message.content):
        await message.channel.send(showLists())
      elif(' show ' in message.content):
        l=" ".join(mess[mess.index('show')+1:])
        index=indexOfList(l)
        if index>=0:
          await message.channel.send(lists[index].getItems())
        else:
          await message.channel.send(l+" is not a list")
keep_alive()
bot.run(os.getenv('TOKEN'))