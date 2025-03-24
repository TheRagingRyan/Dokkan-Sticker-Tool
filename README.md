# Dokkan Sticker Tool
 A tool that lets you modify/create stickers in the game Dokkan Battle.

---
## Python Version 3.13

[Download Python 3.13.0](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe)  
Make sure to add to **PATH** as always.
---
## Dependencies
- ***numpy***  
- ***pillow***  
- ***pyglm***  
- ***PyOpenGL***  
- ***PySide6***  
- ***PySide6_Addons***  
- ***PySide6_Essentials*** 

Also located in **requirements.txt** with the appropriate versions used.

---
## How to Run

- Run **Install Dependencies.bat** first to install the previously mentioned dependencies.  
- Then **Run.bat**
- Done
---
## Preview
- **Files used in the previews are available in *"character\card"***
- **Open File expects the same structure as the game. If it's a modded card, makes sure the files are named appropriately.**  
![Loading Files](https://cdn.discordapp.com/attachments/334448718067662860/1353793248421744670/pythonw_z2qX3u8oh0.gif?ex=67e2f1b6&is=67e1a036&hm=44da98468fafae0512999747f534b525c233d5fb2fae12efbf1d44c583401c4c&)
- **You can load a singular color mask to preview the effect of said mask color (as shown below).**  
![Color Mask Effect](https://cdn.discordapp.com/attachments/334448718067662860/1353795216020078662/pythonw_o790nXEhFu.gif?ex=67e2f38b&is=67e1a20b&hm=f997335a51ede656d6144bf0bcc5db8149aeb7243079ab980c248b6fe7cfc0a9&)  
- **Or even just load the mask, and it will display the effects of everything.**  
![Sticker Mask Effect](https://cdn.discordapp.com/attachments/334448718067662860/1353796365037338664/pythonw_6xWCGY6mm1.gif?ex=67e2f49d&is=67e1a31d&hm=9c25e30bab60fea0b010beb93f2afa72ad055ed83389741751fdb36f6df65200&)

---
## Notable Mentions
- Coordinate mode needs to be enabled in the specific effect's tab in order to move the effect.
- Coordinate mode gets turned off by default when changing effect tabs; in order to prevent unintentionally moving an effect.
- If you need to exceed the window with your coordinates, you can manually edit the json and reload it.

| Screen Position | X Offset | Y Offset |
|-----------------|----------|----------|
| Top Left        | 0.0      | 0.0      |
| Top Right       | -1.0     | 0.0      |
| Bottom Left     | 0.0      | -1.0     |
| Bottom Right    | -1.0     | -1.0     |
