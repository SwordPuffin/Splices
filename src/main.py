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

from gi.repository import Gtk, Gio, Gdk
from .window import SplicesWindow

class SplicesApplication(Gtk.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='org.swordpuffin.splices',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)

        icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        icon_theme.add_resource_path("../data/icons/scalable/apps")

        self.set_accels_for_action('win.enter', ['w'])
        self.set_accels_for_action('win.start', ['s'])

        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('free_play', self.free_play)
        self.create_action('free_play_with_timer', self.free_play_with_timer)
        self.create_action('normal_game', self.normal)

    # The three functions that run when the player hits the buttons that game mode
    # free_play: no timer or word limit
    # free_play_with_timer: no word limit but must be completed within a certain time frame
    # normal: no time limit but there only a limited number of words so try to make them as long as possible
    def free_play(self, widget, _):
        self.window = self.props.active_window
        self.window.normal_game = False
        self.window.clock.set_visible(False)

    def free_play_with_timer(self, widget, _):
        self.window.clock.set_label("Time: 30s")
        self.window = self.props.active_window
        self.window.normal_game = False
        self.window.clock.set_visible(True)

    def normal(self, widget, _):
        self.window = self.props.active_window
        self.window.normal_game = True
        self.window.clock.set_visible(True)
        self.window.clock.set_label("Words: 5")

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = SplicesWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Gtk.AboutDialog(transient_for=self.props.active_window,
                                modal=True,
                                program_name='Splices',
                                logo_icon_name='org.swordpuffin.splices',
                                version='0.1.0',
                                authors=['Nathan Perlman (SwordPuffin)'],
                                copyright='© 2024 Nathan Perlman')
        about.set_website('https://github.com/SwordPuffin')
        about.present()


    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

def main(version):
    """The application's entry point."""
    app = SplicesApplication()
    return app.run(sys.argv)
