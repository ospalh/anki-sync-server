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

import logging

def setup_logging(config_file=None):
    """Setup logging based on a config_file."""
    if config_file is not None:
        # load the config file
         logging.config.fileConfig(config_file)
    else:
        logging.getLogger().setLevel(logging.INFO)
