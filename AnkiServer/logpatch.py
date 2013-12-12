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

from email.utils import formatdate
import logging
import smtplib


# The SMTPHandler taken from python 2.6
class SMTPHandler(logging.Handler):
    """
    A handler class which sends an SMTP email for each logging event.
    """
    def __init__(self, mailhost, fromaddr, toaddrs, subject, credentials=None):
        """
        Initialize the handler.

        Initialize the instance with the from and to addresses and subject
        line of the email. To specify a non-standard SMTP port, use the
        (host, port) tuple format for the mailhost argument. To specify
        authentication credentials, supply a (username, password) tuple
        for the credentials argument.
        """
        logging.Handler.__init__(self)
        # if type(mailhost) == types.TupleType:
        if isinstance(mailhost, tuple):  # suggested by flake8
            self.mailhost, self.mailport = mailhost
        else:
            self.mailhost, self.mailport = mailhost, None
        # if type(credentials) == types.TupleType:
        if isinstance(credentials, tuple):
            self.username, self.password = credentials
        else:
            self.username = None
        self.fromaddr = fromaddr
        # if isinstance(toaddrs, (str, unicode)):
        if isinstance(toaddrs, (str, )):
            toaddrs = [toaddrs]
        self.toaddrs = toaddrs
        self.subject = subject

    def getSubject(self, record):
        """
        Determine the subject for the email.

        If you want to specify a subject line which is record-dependent,
        override this method.
        """
        return self.subject

    weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    monthname = [None,
                 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                self.fromaddr, ",".join(self.toaddrs),
                self.getSubject(record), formatdate(), msg)
            if self.username:
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


# Monkey patch logging.handlers
logging.handlers.SMTPHandler = SMTPHandler
