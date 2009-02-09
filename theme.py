# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import gtk
import shutil
from math import ceil

from sugar.activity.activity import get_bundle_path, get_activity_root
from sugar.graphics import style

SOUND_SPEAKER = 'images/sounds/speaker.png'
SOUND_MUTE    = 'images/sounds/custom.png'
SOUND_CUSTOM  = 'images/sounds/custom.png'

LOGO_WIDTH = 275
TAPE_COUNT = 11
FRAME_COUNT = 14

DESKTOP_WIDTH = gtk.gdk.screen_width()
DESKTOP_HEIGHT = gtk.gdk.screen_height() - style.LARGE_ICON_SIZE

THUMB_SIZE = min(100, DESKTOP_WIDTH / (TAPE_COUNT+1))

FRAME_COLS = max(1, ((DESKTOP_WIDTH-LOGO_WIDTH) -
        min(DESKTOP_HEIGHT-THUMB_SIZE-THUMB_SIZE/2, DESKTOP_WIDTH-LOGO_WIDTH))
        / THUMB_SIZE)

FRAME_ROWS = max((DESKTOP_HEIGHT - THUMB_SIZE*3) / THUMB_SIZE,
        int(ceil(float(FRAME_COUNT) / FRAME_COLS)))

BORDER_WIDTH = 10

# Colors from the Rich's UI design

GRAY = "#B7B7B7" # gray
PINK = "#FF0099" # pink
YELLOW = "#FFFF00" # yellow
WHITE = "#FFFFFF"
BLACK = "#000000"
BACKGROUND = "#66CC00" # light green
BUTTON_FOREGROUND = "#CCFB99" # very light green
BUTTON_BACKGROUND = "#027F01" # dark green
COLOR_FG_BUTTONS = (
    (gtk.STATE_NORMAL,"#CCFF99"),
    (gtk.STATE_ACTIVE,"#CCFF99"),
    (gtk.STATE_PRELIGHT,"#CCFF99"),
    (gtk.STATE_SELECTED,"#CCFF99"),
    (gtk.STATE_INSENSITIVE,"#CCFF99"),
    ) # very light green
COLOR_BG_BUTTONS = (
    (gtk.STATE_NORMAL,"#027F01"),
    (gtk.STATE_ACTIVE,"#CCFF99"),
    (gtk.STATE_PRELIGHT,"#016D01"),
    (gtk.STATE_SELECTED,"#CCFF99"),
    (gtk.STATE_INSENSITIVE,"#027F01"),
    )
OLD_COLOR_BG_BUTTONS = (
    (gtk.STATE_NORMAL,"#027F01"),
    (gtk.STATE_ACTIVE,"#014D01"),
    (gtk.STATE_PRELIGHT,"#016D01"),
    (gtk.STATE_SELECTED,"#027F01"),
    (gtk.STATE_INSENSITIVE,"#027F01"),
    )

SESSION_PATH = os.path.join(get_activity_root(), 'tmp', '.session')
if os.path.isdir(SESSION_PATH):
    shutil.rmtree(SESSION_PATH)
os.mkdir(SESSION_PATH)

def path(*args):
    file = os.path.join(*args)

    if os.path.isabs(file):
        return file
    else:
        return os.path.join(get_bundle_path(), file)

def pixbuf(file, size = None):
    if size:
        out = gtk.gdk.pixbuf_new_from_file_at_size(path(file), size, size)
    else:
        out = gtk.gdk.pixbuf_new_from_file(path(file))
    return out

def scale(pixbuf, size = THUMB_SIZE):
    return pixbuf.scale_simple(size, size, gtk.gdk.INTERP_BILINEAR)

EMPTY_FILENAME = 'images/pics/empty.png'
EMPTY_ORIG = pixbuf(EMPTY_FILENAME)
EMPTY_THUMB = scale(EMPTY_ORIG)

#CUSTOM_GROUND   EMPTY_FILENAME = 'images/pics/empty.png'

CUSTOM_FRAME_ORIG = pixbuf('images/pics/custom.png')
CUSTOM_FRAME_THUMB = scale(CUSTOM_FRAME_ORIG)

def choose(out_fun, default=None):
    from sugar.graphics.objectchooser import ObjectChooser

    chooser = ObjectChooser()
    jobject = None

    try:
        result = chooser.run()

        if result == gtk.RESPONSE_ACCEPT:
            jobject = chooser.get_selected_object()
            if jobject and jobject.file_path:
                return out_fun(jobject)
    finally:
        if jobject: jobject.destroy()
        chooser.destroy()
        del chooser

    return default

def pixbuf2str(pixbuf):
    def push(data, buffer):
        buffer.write(data)

    import cStringIO
    buffer = cStringIO.StringIO()
    pixbuf.save_to_callback(push, 'png', user_data=buffer)
    return buffer.getvalue()

def str2pixbuf(data):
    tmpfile = os.path.join(SESSION_PATH, '.tmp.png')
    file(tmpfile, 'w').write(data)
    out = pixbuf(tmpfile)
    os.unlink(tmpfile)
    return out

# customize theme
gtkrc = os.path.join(get_bundle_path(), 'gtkrc')
gtk.rc_add_default_file(gtkrc)
settings = gtk.settings_get_default()
gtk.rc_reset_styles(settings)
gtk.rc_reparse_all_for_settings(settings, True)