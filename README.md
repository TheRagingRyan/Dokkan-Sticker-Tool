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
![1](https://github.com/user-attachments/assets/dc85cf2c-3347-4f2d-89d4-fdafbd661042)
- **You can load a singular color mask to preview the effect of said mask color (as shown below).**  
![2](https://github.com/user-attachments/assets/c5b06443-f0ff-41b2-9fa8-9a3be4fd235b)
- **Or even just load the mask, and it will display the effects of everything.**  
![3](https://github.com/user-attachments/assets/bd21333f-2730-482d-90ae-06eaa83f0aad)

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
