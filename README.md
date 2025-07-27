<img width="590" height="341" alt="image" src="https://github.com/user-attachments/assets/c5d0dad0-1f9e-4692-92a4-2b7c1f008919" />

An Among Us tool created with Python that allows bypassing settings limits in local and online lobbies.

# Table of contents
- [📈 Roadmap](#📈-roadmap)

- [📌 How to use](#how-to-use)

⠀⠀⠀⠀⠀◦ [🖥 Windows](##windows)

⠀⠀⠀⠀⠀◦ [📱 Android](##android)

⠀⠀⠀⠀⠀◦ [💻📳 MacOS, iOS](##macOS,-ios)

- [✅ FAQ](#faq)

# 📈 Roadmap

🟡 Release

🔴 Hide N Seek generator mode support

🔴 Normal generator mode roles support

🔴 Compatibility for all platforms

# 📌 How to use
## 🖥 Windows
0️⃣. Go to %userprofile%\AppData\LocalLow\Innersloth\Among Us path in your file explorer (or press Win+R and paste the same), it should open Among Us AppData folder. Now backup the "settings.amogus" file to another folder (that is needed for you to recover the file if you mess up with base64. You can still reinstall the game if you don't create one).

1️⃣. Go to [releases](https://github.com/Zaxerf1234/AmongUsLimitBypasser/releases) tab and download release that fits your Among Us version (note: releases for older versions won't be supported if there's a completely new hex arrangement in the new versions) or build one yourself from the source code.

2️⃣. Launch "Among Us Limit Bypasser.exe" file and type settings generator mode (1 - normal game, 2 - hide n seek (coming soon)).

3️⃣. Fill each setting line with value you want to use for that setting.

4️⃣. After you've done, copy the base64 output and go to %userprofile%\AppData\LocalLow\Innersloth\Among Us again. Open "settings.amogus" file with notepad or any text editor you want and paste your base64 into "normalHostOptions" value or "hideNSeekHostOptions" depending on what generator mode you used (note: if you want to edit hex settings manually, you can copy the hex value output and edit it in a hex editor and then use "Encode modified hex to Base64" option in the program menu (3) to encode it back). Make sure Among Us is closed at that moment!

5️⃣. Launch the game and host a local or online lobby to see the changes. Enjoy!

## 📱 Android
0️⃣. Go to /storage/emulated/0/Android/data/com.innersloth.spacemafia/files/ path in your android file explorer (if your explorer doesn't allow you to go to the "data" folder, install an external explorer from google play market or whatever and give it permission to view system folders). Now backup the "settings.amogus" file to another folder (that is needed for you to recover the file if you mess up with base64. You can still reinstall the game if you don't create one).

1️⃣. Install a Python IDE for android that supports pip such as Pydroid. Then go to [releases](https://github.com/Zaxerf1234/AmongUsLimitBypasser/releases) tab, choose release that fits your Among Us version (note: releases for older versions won't be supported if there's a completely new hex arrangement in the new versions) and download "Source code (zip)". It will download you a zip file with the source code. Now open your IDE console and run: 
```bash
cd insert_path_to_the_folder_here
```
Replace "insert_path_to_the_folder_here" with your actual path to the folder you downloaded. Should look like this: /storage/emulated/0/Download/AmongUsLimitBypasser-main. Then, run in console
```bash
pip install -r requirements.txt
```
This will install all dependencies. If for some reason the method above doesn't work, install all libraries separately:
```bash
pip install colorama pyfiglet
```
2️⃣. Run the "main.py" file in your IDE and type settings generator mode (1 - normal game, 2 - hide n seek (coming soon)).

3️⃣. Fill each setting line with value you want to use for that setting.

4️⃣. After you've done, copy the base64 output and go to /storage/emulated/0/Android/data/com.innersloth.spacemafia/files/ path again. Open "settings.amogus" file with any text editor and paste your base64 into "normalHostOptions" value or "hideNSeekHostOptions" depending on what generator mode you used (note: if you want to edit hex settings manually, you can copy the hex value output and edit it in a hex editor and then use "Encode modified hex to Base64" option in the program menu (3) to encode it back). Make sure Among Us is closed at that moment!

5️⃣. Launch the game and host a local or online lobby to see the changes. Enjoy!

## 💻📳 MacOS, iOS
No data.

If you know how to modify settings on following platforms, feel free to open an issue and tell me there!


# ✅ FAQ
In this section you can find answers for frequently asked questions and issues with the tool.

## Q: Is this program a virus?
A: No.

## Q: Can I customize role settings with this tool?
A: Currently, role settings cannot be customized—only basic settings are available. However, I’m working on this feature, and it will be included in a future update.

## Q: There's no "settings.amogus" file. What should I do?
A: Make sure you’ve launched the game and created a room at least once. Then try again.

## Q: Does this work on cracked version of Among Us?
A: It should work fine, but come on - are you really pirating a $5 game? Support the developers if you can.

**FAQ may change at any time if I get more questions asked.**
