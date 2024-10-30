# window.py
#
# Copyright 2024 Nathan Perlman
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import gi
import random
gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk
@Gtk.Template(resource_path='/io/github/swordpuffin/splices/window.ui')
class SplicesWindow(Gtk.ApplicationWindow):

    __gtype_name__ = 'SplicesWindow'

    #All child components from the window.ui file that need to be referenced in the code
    score = Gtk.Template.Child()
    start_button = Gtk.Template.Child()
    clock = Gtk.Template.Child()
    grid = Gtk.Template.Child()
    current_word = Gtk.Template.Child()
    game_list = Gtk.Template.Child()
    found_words = Gtk.Template.Child()

    found = []
    game_active = False
    consonants = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]
    vowels = ["A", "E", "I", "O", "U"]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("/app/share/splices/splices/style.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        start_action = Gio.SimpleAction(name="start")
        start_action.connect("activate", self.on_start_clicked)
        self.add_action(start_action)

        #The countdown clock or the words remaining counter depending on the game mode
        change_time = Gio.SimpleAction.new(name="times_words_change")
        change_time.connect("activate", self.times_words_change)
        self.add_action(change_time)

        check_word = Gio.SimpleAction.new("enter", None)
        check_word.connect("activate", self.check)
        self.add_action(check_word)

        self.timer = 30

        #Start timer logs the time that has elapsed since the start to be used in the results dialog when the time runs out
        self.start_time = 30

        self.current_score = 0
        self.timer_id = None

        #I felt it was better to keep it at one set size just given its layout looked very unusual at full screen
        self.set_resizable(False)

        self.set_title("")
        self.normal_game = False
        self.words = 5
        # self.set_cursor_theme_size(31)

    #Checks if the submitted word exists in words.txt
    def check(self, actiom, _):
        #Only activate this code when there is actually a word that the player is trying to submit. This stops spam which causes the timer to lag
         if(len(self.current_word.get_label()) > 0):
             self.color_change()
             with open("/app/share/splices/splices/words.txt", 'r') as file:
                 for line in file:
                    #If the word was in words.txt and was not already found. The brackets are used to signify the start and end of the word. EX. /start/
                     if f"/{self.current_word.get_label().lower()}/" in line and f"/{self.current_word.get_label().lower()}/" not in self.found:
                        self.found.append(f"/{self.current_word.get_label().lower()}/")
                        self.current_score += len(self.current_word.get_label())
                        self.score.set_label(f"Score: {self.current_score}")
                        self.found_words.set_label(self.found_words.get_label() + "  " + self.current_word.get_label())
                        self.current_word.set_label("")
                        if(self.normal_game):
                            self.words -= 1
                            self.clock.set_label(f"Words left: {self.words}")
                            if(self.words == 0):
                                #Show the end dialog once the player has run out of words
                                self.end_dialog()
                                self.on_start_clicked(None, _)
                        return True
             self.current_word.set_label("")
             self.shake()
             return False

    #Shakes the current_word box when the word the user is trying to enter does not exist.
    def shake(self):
        #Moves it 5px to the left/right
        self.current_word.add_css_class("shake")
        def remove_shake():
            self.current_word.remove_css_class("shake")
            return False
        GLib.timeout_add(500, remove_shake)

    #Function activated when a letter is selected from the grid.
    def letter_selected(self, action, _, button):
        self.current_word.set_label(self.current_word.get_label() + button.get_label())
        button.add_css_class("selected_button")
        button.set_sensitive(False)

    #Either adds 5 seconds or 1 more available word when the clock button is clicked depending on the game mode
    def times_words_change(self, action, _):
        if(self.normal_game == False):
            self.timer += 5
            self.clock.set_label(f"Time: {self.timer}s")
            self.start_time = self.timer
        else:
            self.words += 1
            self.clock.set_label(f"Words left: {self.words}")

    #Function that is activated to either forcefully stop or start the game
    def on_start_clicked(self, action, _):
        self.game_active = not self.game_active
        self.game_list.set_visible(not self.game_active)
        self.game_state()
        self.color_change()
        self.elapsed_time = 0
        self.found.clear()

        #If it is a normal game, just reset the words back to five. If it is a timed game, set the clock to 30 seconds once the game is over
        if(self.game_active == False and self.normal_game == False):
            self.timer = 30
            self.clock.set_label("Time: 30s")
        elif(self.game_active == False and self.normal_game):
            self.words = 5
            self.clock.set_label("Words left: 5")
        if(self.clock.is_visible() and self.normal_game == False):
            self.clock.set_sensitive(not self.game_active)
            self.timer_id = GLib.timeout_add(100, self.update)

    #Reset the color of the all the letter buttons in the grid to grey
    def color_change(self):
        for child in self.grid:
            child.remove_css_class("selected_button")
            child.set_sensitive(True)

    #Changes aspects of the game when it either runs out of time, or the stop/start button is clicked
    def game_state(self):
        self.clock.set_sensitive(not self.game_active)
        self.grid.set_sensitive(self.game_active)
        if(self.game_active == True):
            self.start_button.add_css_class("destructive-action")
            self.start_button.remove_css_class("suggested-action")
            self.start_button.set_label("Stop")
            self.score.set_label("Score: 0")
        else:
            self.start_button.remove_css_class("destructive-action")
            self.start_button.add_css_class("suggested-action")
            self.start_button.set_label("Start")
            self.current_word.set_label("")
            self.found_words.set_label("")
            self.score.set_label("")
            self.current_score = 0
        self.set()

    #When the game starts, this function will assign a letter to each button in the grid to make the words
    def set(self):
        count = 1
        for child_of_grid in self.grid:
            if(self.game_active):
                vowel_or_consonant = random.choice([self.vowels, self.consonants])
                child_of_grid.set_label(random.choice(vowel_or_consonant))
            else:
                child_of_grid.set_label("")
            letter_action = Gio.SimpleAction.new(f"item{count}", None)
            letter_action.connect("activate", self.letter_selected, child_of_grid)
            self.add_action(letter_action)
            count += 1

    #Every 0.1 seconds, decrease timer by 0.1 and display the end dialog when it reaches ~0.
    def update(self):
        if(self.timer <= 0.1):
            self.end_dialog()
            self.on_start_clicked(None, _)
        if(self.game_active == True):
            self.timer -= 0.1
            self.clock.set_label("Time: " + str(round(self.timer, 1)) + "s")
            return True
        else:
            return False

    #Dialog that runs when the time runs out or the player has used all available words. Shows them the number of points with either how long it took or the number of words.
    def end_dialog(self):
        dialog = Gtk.Dialog(transient_for=self, modal=True)
        dialog.set_title("Results")
        content = dialog.get_content_area()
        if(self.normal_game):
            length = Gtk.Label(label="You got " + self.score.get_label().replace("Score: ", "") + " points in " + str(len(self.found)) + " words")
        else:
            length = Gtk.Label(label="You got " + self.score.get_label().replace("Score: ", "") + " points in " + str(self.start_time) + " seconds")
        found_list = Gtk.Label(label=self.found_words.get_label())
        content.append(length), content.append(found_list)
        length.set_margin_start(30),  found_list.set_margin_start(30)
        length.set_margin_end(30), found_list.set_margin_end(30)
        length.set_margin_bottom(10), found_list.set_margin_bottom(10)
        length.add_css_class("title-3"), found_list.add_css_class("title-4")
        dialog.present()
