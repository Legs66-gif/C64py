import pygame
import psutil
import time
import textwrap
import os

#Memory Data
memtotal = round(int(psutil.virtual_memory().total) / 1000000000)
memfree = round(int(psutil.virtual_memory().available) / 1000000)
memstring = " " + str(memtotal) + "G RAM SYSTEM   " + str(memfree) + " MEGABYTES FREE"
print(memstring)

#Colours
lightblue = 134,122,222
blue = 72,58,171

#Locations
cursors = 41,90,8,8
cursor = cursors

#Screen and Start Line Initialization
pygame.init()
screen = pygame.display.set_mode((395, 284))
font = pygame.font.Font('font.tff', 8)
power = True
input_status = True
cassete = 'Unknown'
text = ['','    **** COMMODORE 64 BASIC V2 ****','',memstring,'','READY.','']
promptinput = ''
operators = "=+-*/^"
x=6
dir_list = []
prog = []

print(eval("2+2"))
#Checks for BASIC command entry
def command(prompt, x, cursor, input_status, prog):
  promptls=prompt.split()
  print("Promt: ", promptls)
  if promptls[0] == 'HELP':
    x=x+7
    text.append("1) HELP - SHOWS LIST OF COMMANDS")
    text.append("2) PRINT - DISPLAYS TEXT ON DISPLAY")
    text.append("3) LOAD - LOADS PROGRAM FROM DISK")
    text.append('   LOAD "$",[DEVICE] - LOADS DIRECTORY')
    text.append("4) LIST - DISPLAYS PROGRAM")
    text.append("")
    text.append("DEVICE NUMBERS: 1=TAPE, 8=DISK")
    cursor = (41, cursor[1]+56, cursor[2], cursor[3])
  elif promptls[0] == 'PRINT' :
    x=x+1
    for i in range(len(promptls[1:])):
      try:
        text.append(str(eval(promptls[i+1])))
      except (NameError):
        text.append(" 0") 
    cursor = (41, cursor[1]+8, cursor[2], cursor[3])
  elif promptls[0] == 'LOAD' :
    text.append("")
    directory = os.getcwd()
    if len(promptls) > 1:
      parameters = promptls[1].split(',')
    if len(promptls) == 1 or promptls[1] == '1':
      text.append("PRESS PLAY ON TAPE")
      cursorsave = cursor
      cursor = (0,0,0,0)
      input_status = False
    elif parameters[0] == '"$"':
      x=x+3
      text.append("SEARCHING FOR $")
      text.append("LOADING")
      prog = []
      dir_list = os.listdir(str(os.getcwd())+"\\"+parameters[1])
      for i in range(len(dir_list)):
        file_location = str(os.getcwd())+"\\"+parameters[1]+"\\"+dir_list[i]
        file_size = os.stat(file_location)
        file_size = int(int(file_size.st_size))
        file_name = os.path.splitext(dir_list[i])
        file_name = '"'+file_name[0]+ '"', file_name[1][1:]
        linex = str(file_size),file_name[0], file_name[1]
        joiner = ' '*(5-len(linex[0]))
        joiner2 = ' '*(19-len(linex[1]))
        line = (linex[0]+joiner+linex[1]+joiner2+linex[2]).upper()
        print(line)
        prog.append(line)
      hdd = psutil.disk_usage('/')
      blocksfree = str(int(hdd.free/256))+" BLOCKS FREE."
      prog.append(blocksfree)
      cursor = (41, cursor[1]+24, cursor[2], cursor[3])
    elif parameters[0] == '"*"':
      x=x+3
      text.append("SEARCHING FOR *")
      if os.path.isdir("./"+parameters[1]):
        text.append("LOADING")
        prog = []
        dir_list = os.listdir(str(os.getcwd())+"\\"+parameters[1])
        print(dir_list)
        file = open(str(os.getcwd())+"\\"+parameters[1]+"\\"+dir_list[0], "r")
        while line := file.readline():
          current = line.rstrip().upper()
          print(current)
          prog.append(current)
        print(prog)
      else:
        text.append("?DEVICE NOT PRESENT  ERROR") 
      cursor = (41, cursor[1]+24, cursor[2], cursor[3])
    elif parameters[0][0] == '"':
      found = False
      print("Parameters:", parameters)
      print("Search Term:",parameters[0][1:-1])
      x=x+3
      text.append("SEARCHING FOR "+parameters[0][1:-1])
      directory = directory + "\\" + parameters[1]
      print("Directory:", directory)
      if os.path.isdir(directory):
        for file in os.listdir(directory):
          if os.path.splitext(file)[0].upper() == parameters[0][1:-1]:
            print("File Found")
            text.append("LOADING")
            print("File:", file)
            filename = file
            with open((directory + "\\" +filename), "r") as openfile:
              for num, line in enumerate(openfile, 1):
                if line != "\n":
                  print("Line:", num)
                  print("Prompt:", line)
                  print(type(line))
                  prog.append(str(num) + " " + line)
                  prompt = line
                  x, cursor, input_status, prog= command(prompt, x, cursor, input_status, prog)
            found = True
        if not found:
          print("File Not Found")
          text.append("?FILE NOT FOUND ERROR")
      else:
        text.append("?DEVICE NOT PRESENT  ERROR")
      cursor = (41, cursor[1]+24, cursor[2], cursor[3])
    else:
      x=x+2
      text.append("?SYNTAX ERROR")
      cursor = (41, cursor[1]+16, cursor[2], cursor[3])
  elif promptls[0] == 'LIST' :
    x=x+len(prog)+1
    text.append("")
    text.extend(prog)
    cursor = (41, cursor[1]+(8*(len(prog)+1)), cursor[2], cursor[3])
  elif promptls[0] == 'RUN' :
    for line in prog:
      prompt = line
      x, cursor, input_status, prog= command(prompt, x, cursor, input_status, prog)
  else:
    x=x+2
    text.append("")
    text.append("?SYNTAX ERROR")
    cursor = (41, cursor[1]+16, cursor[2], cursor[3])
  return x,cursor,input_status,prog
  
#Main Loop
while power:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        power = False
    elif event.type == pygame.KEYDOWN and input_status:
        print(x)
        if event.key == pygame.K_RETURN:
          print("key registered")
          print(x, text)
          print("Number of Lines:",range(len(text)))
          if text[x] != "":
            prompt = text[x]
            print("Command In:",x)
            x, cursor, input_status, prog= command(prompt, x, cursor, input_status, prog)
            text.append("")
            text.append("READY.")
            x=x+2
            cursor = (41, cursor[1]+16, cursor[2], cursor[3])
            print("Command Out:",x)
          for i in range(1+(len(text[x]) // 39)) :
            x=x+1
            text.append("")
          print(x, text)
          cursor = (41, cursor[1]+(8), cursor[2], cursor[3])
        elif event.key == pygame.K_BACKSPACE:
            if cursor[1] == 42 + x*8 and cursor[0] < (49):
              print("Nothing")
            else:
              text[x] =  text[x][:-1]
              cursor = (cursor[0] - 8, cursor[1], cursor[2], cursor[3])
        elif event.key == pygame.K_SPACE:
            text[x] += " "
            cursor = (cursor[0] + 8, cursor[1], cursor[2], cursor[3])
        else:
          if len(pygame.key.name(event.key))<=1:
            text[x] += event.unicode
            cursor = (cursor[0] + 8, cursor[1], cursor[2], cursor[3])
  
  screen.fill((lightblue))
  pygame.draw.rect(screen, blue, (41,42,312,200))
  if len(text) > 25:
      del text[0]
      cursor = 41, cursor[1]-(8), cursor[2], cursor[3]
      x=x-1
  for y in range(len(text)) :
    text[x] = text[x].upper()
    lines = textwrap.wrap(text[y], 39 , break_long_words=True)
    for i in range(len(lines)):
      text_surf = font.render(lines[i], True, lightblue)
      screen.blit(text_surf, (41,(42 + y*8 + i * 8)))
  if cursor[0] > 345 :
    cursor = (41,cursor[1] + 8,8,8)
  if cursor[0] < 41 and cursor[1] > 90:
    cursor = (345,cursor[1]-8,8,8)
  if time.time() % 1 > 0.33:
    pygame.draw.rect(screen, lightblue, cursor)
  pygame.display.flip()


#if len(promptls) == 2 and any(char.isdigit() for char in promptls[1]) and any(char in operators for char in promptls[1]):
#        print("Printing: ", eval(promptls[1]))
#        text.append(str(eval(promptls[1])))
#    else :
#      text.append(' '.join(promptls[1:]))