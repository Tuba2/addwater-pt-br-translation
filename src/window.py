# window.py
#
# Copyright 2024 Claire
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

import logging, os.path
from gi.repository import Adw, Gtk, GLib, Gio, Gdk, GObject
from .pages.firefox_page import FirefoxPage
from .utils.profiles import find_firefox_path
from .utils import logs

log = logging.getLogger(__name__)

@Gtk.Template(resource_path='/dev/qwery/AddWater/gtk/window.ui')
class AddwaterWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'AddwaterWindow'

    main_page_switcher = Gtk.Template.Child()
    main_view_stack = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = Gio.Settings(schema_id="dev.qwery.AddWater")

        firefox_path = os.path.expanduser(self.settings.get_string("firefox-path"))
        if os.path.exists(firefox_path) is False:
            firefox_path = find_firefox_path()
            if firefox_path is None:
                log.error("Could not find Firefox path automatically. User must set it manually.")
            else:
                self.settings.set_string("firefox-path", firefox_path)
                log.info(f"Found Firefox path.{firefox_path}")

        self.main_view_stack.add_titled_with_icon(
            child=FirefoxPage(firefox_path=firefox_path),
            name="Firefox",
            title="Firefox",
            icon_name="globe-symbolic"
        )

