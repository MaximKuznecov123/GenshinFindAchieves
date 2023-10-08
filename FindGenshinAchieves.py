from time import sleep
from pyautogui import position, locateOnScreen
import pydirectinput as GYGApag
from pyperclip import copy
from random import randint
import requests
from os.path import exists
import sys
import os

lang = 1 # 0 for Russian and 1 for English
gameLang = 1
lastAch = None
languages = {
   "ru":0,
   "eng":1
}

def resource_path(relative_path):
   base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
   return os.path.join(base_path, relative_path)

def check(sec:float):
   sec = int(sec*10)
   for i in range(sec):
      if position() == (0, 0): 
         return True
      else: False
   sleep(0.1)

def rand(start:float, end:float)-> float:
   return randint(start, end)

def getAchieves() -> tuple:
   def getRuAchieves() -> tuple:
      r = requests.get("https://genshin-impact.fandom.com/ru/wiki/Чудеса_света", timeout = 30, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36", "content-type": "text"})
      achieves = []
      for achieve in r.text.split("\n"):
         if achieve.startswith("<tr id="):
            achieves.append(achieve[8:-34].replace("_"," "))
      return tuple(dict.fromkeys(achieves))
   def getEngAchieves() -> tuple:
      r = requests.get("https://genshin-impact.fandom.com/wiki/Wonders_of_the_World", timeout = 30, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36", "content-type": "text"})
      achieves = []
      for achieve in r.text.split("\n"):
         if achieve.startswith('<td><a href="/') and '"Version/' not in achieve and achieve.endswith("</a>"): 
            achieves.append(achieve[achieve.rfind(">", 0, -4)+1:-4])
      return tuple(dict.fromkeys(achieves))

   achieves = ()
   if(gameLang == languages["ru"]):
      achieves = getRuAchieves()
   elif(gameLang == languages["eng"]):
      achieves = getEngAchieves()

   return achieves

def checkAchieves(achieves:list) -> (str, list): 
   result = []
   flag = False
   lastAch = ""
   GYGApag.FAILSAFE = False

   for achieve in achieves:
      if flag: break
      copy(achieve)
      flag = check(rand(1, 3))

      GYGApag.keyDown("ctrl")
      GYGApag.press("v")
      GYGApag.keyUp("ctrl")

      flag = check(rand(1, 3))
      GYGApag.press("enter")
      flag = check(rand(8, 10))

      if locateOnScreen(resource_path("where.png")) != None:
         result.append(achieve)
      flag = check(rand(1, 3))

      GYGApag.click()
      flag = check(rand(4, 6))
      GYGApag.press("backspace")
      flag = check(rand(4, 6))
      lastAch = achieve

   return (lastAch, result)

def printAndGetAnswer(message:str, answers:tuple) -> int:
   while True:
      print(message)
      answer = input()
      if len(answer) == 0: break
      try:
         index = answers.index(answer)
         return index
      except ValueError:
         print(cues[5][lang])

cues = (
   ("Введи язык, используемый в игре (ЭТО РЕАЛЬНО ВАЖНО - ВВОДИ КОРРЕКТНО)[ru] - для русского [eng] - для английского",  ("ru", "eng")),
   ("Теперь запусти Genshin Impact и передвинь курсор на левую сторону панели поиска достижений.\nЧерез 10 секунд после того как ты нажмешь [s] начнется автоматический поиск. В среднем на это уходит 10 минут.\nТы можешь остановить поиск(НЕ ПРОГРАММУ), переведя курсор в левый верхний угол, введенные тобой данные и достижение, на котором остановилась программа, сохранятся в папке с этой программой в файле savedInstance.txt.\n Если ты уже запускал программу и искал достижения, то новые найденные невыполненные достижения будут добавлены в файл result.txt", "Now run Genshin Impact and move cursor to left side of achievement search panel.\n10 seconds after you press [s] will start the automatic search. Usually it takes around 10 minutes.\nYou can stop the search(NOT PROGRAMM) by moving the cursor to the upper left corner, the data you entered and the achievement on which the program stopped will be saved in the folder with this program in the savedInstance.txt file.\n If you have already launched the program and started to search for achievements, new achievements will be added to the file result.txt", ("s",)),
   ("Невыполненные достижения сохранены в папку с этой программой в файл result.txt. Все введенные данные были сохранены в файл savedInstance.txt", "Unachieved achievements are saved to the folder with this program in the file result.txt. All entered data was saved to savedInstance.txt file"),
   ("Ипользовать ранее введенные данные? [y] - да [n] - нет", "Use previously entered data? [y] - yes [n] - no", ("y", "n")),
   ("Начать поиск с последнего сохраненного достижения? Учти, что возникнет ошибка, если ты, ответив на прошлый пункт НЕТ, поменяешь язык [y] - да, [n]  - нет", "Start the search with the last saved achievement? Note that error will occure if you, having answered the last paragraph NO, change language [y] - yes, [n] - no", ("y", "n")),
   ("Нет такого варианта. Попробуй еще раз", "There is no such option. Try again")
)

def main():
   try:
      global lang
      global gameLang
      useSavedData = False
      useSavedAchieve = False
      if exists("savedInstance.txt"):
         with open("savedInstance.txt", "r", encoding="utf-8") as file:
            instance = file.read().split("\n")
            lastAch = instance[0]
            lang = int(instance[1])
            gameLang = int(instance[2])
         useSavedData = True if printAndGetAnswer(cues[3][lang], cues[3][2]) == 0 else False
         useSavedAchieve = True if printAndGetAnswer(cues[4][lang], cues[3][2]) == 0 else False
      if not useSavedData:
         lang = printAndGetAnswer("Type your language(TYPE CORRECTLY - IT IS IMPORTANT): [ru] - for Russian; [eng] - for English (hereinafter without square brackets)", ("ru", "eng"))
         if lang == 0:
            gameLang = printAndGetAnswer(cues[0][0], cues[0][1])

      printAndGetAnswer(cues[1][lang], cues[1][2])
      
      achieves = getAchieves()
      
      for i in range(10):
         print(i)
         sleep(1)

      lastAch, result = checkAchieves(achieves if not useSavedAchieve else achieves[achieves.index(lastAch):])
      with open("savedInstance.txt", "w", encoding="utf-8") as file:
         indexLast = achieves.index(lastAch)
         file.write(achieves[indexLast - 2 if indexLast >= 2 else indexLast] + "\n")
         file.write(str(lang) + "\n")
         file.write(str(gameLang))
      with open("result.txt", "a", encoding="utf-8") as file:
         file.write("".join([each+"\n" for each  in result]))
         file.write("\n")
      printAndGetAnswer(cues[2][lang], ())
   except Exception as e:
      print(e)
main()