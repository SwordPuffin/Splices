# Splices

A small time killing game where you build words with a random set of letters. Made with GTK4 and Python.

# How To Play

There are three modes: length, free play, and timed. The goal in length mode is to maximise the length of the words available given a limited number of guesses. Free play has no maximum word count or timer, unlike timed which (obviously) has a limited time frame. Modes can be changed with the game controller icon in the top right

# Keybinds

w - Enter completed word (or not completed word to delete it)

s - Stop or start a game

Ctl-q - Exit

Ctl-? - Show keyboard shortcuts

# Screenshots

![Screenshot](https://github.com/SwordPuffin/Splices/blob/master/data/Screenshot1.png)

![Screenshot](https://github.com/SwordPuffin/Splices/blob/master/data/Screenshot2.png)

# Downloading

<a href='https://flathub.org/apps/io.github.swordpuffin.splices'>
    <img width='240' alt='Get it on Flathub' src='https://flathub.org/api/badge?locale=en'/>
</a>

Splices is available on the web with Flathub, or:
```
flatpak install flathub io.github.swordpuffin.splices
```
# To edit the app in Gnome-Builder

Run the following commands in a terminal:

(Make a folder named 'Projects' in your home directory if it doesn't already exist)
```
cd Projects
```
```
git clone https://github.com/SwordPuffin/Splices
```
Open Gnome-Builder and then hit select folder at the bottom to add the project
