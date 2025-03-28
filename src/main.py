# main.py
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

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Gdk, Adw
from .window import SplicesWindow

class SplicesApplication(Adw.Application):

    def __init__(self):
        super().__init__(application_id='io.github.swordpuffin.splices',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)

        # icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        # icon_theme.add_resource_path("../data/icons/scalable/apps")
        # icon_theme.add_resource_path("../data/icons/symbolic/apps")

        self.set_accels_for_action('win.enter', ['space'])
        self.set_accels_for_action('win.start', ['s'])

        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('free_play', self.free_play)
        self.create_action('timed', self.timed)
        self.create_action('length', self.length)
        self.create_action('normal', self.normal)
        self.create_action('hard', self.hard)
        self.create_action('hardest', self.hardest)

    # The three functions that run when the player hits the buttons that game mode
    # free_play: no timer or word limit
    # timed: no word limit but must be completed within a certain time frame
    # length: no time limit but there only a limited number of words so try to make them as long as possible
    def free_play(self, widget, _):
        self.window = self.props.active_window
        self.window.normal_game = False
        self.window.clock.set_visible(False)
        self.window.extra.set_visible(False)

    def timed(self, widget, _):
        self.window = self.props.active_window
        self.window.clock.set_label("Time: 30s")
        self.window = self.props.active_window
        self.window.normal_game = False
        self.window.clock.set_visible(True)
        self.window.extra.set_visible(True)
        
    def length(self, widget, _):
        self.window = self.props.active_window
        self.window.normal_game = True
        self.window.clock.set_visible(True)
        self.window.extra.set_visible(True)
        self.window.clock.set_label("Words left: 5")
        
    def normal(self, widget, _):
        self.window = self.props.active_window
        self.window.consonant_list = self.window.normal_consonants
    
    def hard(self, widget, _):
        self.window = self.props.active_window
        self.window.consonant_list = self.window.hard_consonants
    
    def hardest(self, widget, _):
        self.window = self.props.active_window
        self.window.consonant_list = self.window.hardest_consonants

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = SplicesWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Gtk.AboutDialog(transient_for=self.props.active_window,
                                modal=True,
                                program_name='Splices',
                                logo_icon_name='io.github.swordpuffin.splices',
                                version='1.1.3',
                                authors=['Nathan Perlman (SwordPuffin)'],
                                copyright='© 2024 Nathan Perlman')
        about.set_website('https://github.com/SwordPuffin')
        about.present()


    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

def main(version):
    app = SplicesApplication()
    return app.run(sys.argv)
