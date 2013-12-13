# -*- mode: python ; coding: utf-8 -*-
#
# AnkiServer - A personal Anki sync server
# Copyright (C) 2013 David Snopek
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.version import StrictVersion
import sys
import os.path

sys_strict_version = StrictVersion('{}.{}.{}'.format(
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro))
if sys_strict_version < StrictVersion('2.6'):
    raise Exception("Please upgrade your Python to 2.6 or 2.7")
if sys_strict_version >= StrictVersion('3.0'):
    raise Exception("AnkiServer does not work with Python 3")

# We put the system installed Anki first!
sys.path.insert(0, "/usr/share/anki")
# We'll put our bundled Anki after it
sys.path.insert(1, os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'anki-bundled'))

__author__ = "David Snopek <dsnopek@gmail.com>"
__copyright__ = "Copyright (C) 2013 David Snopek"
__license__ = "GNU Affero General Public License v3 or later (AGPLv3+)"
__version__ = "2.0.4"

__all__ = []


def server_runner(app, global_conf, **kw):
    """ Special version of paste.httpserver.server_runner which calls
    AnkiServer.threading.shutdown() on server exit."""

    from paste.httpserver import server_runner as paste_server_runner
    from AnkiServer.threading import shutdown
    try:
        paste_server_runner(app, global_conf, **kw)
    finally:
        shutdown()
