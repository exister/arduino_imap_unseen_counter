# -*- coding: utf-8 -*-
from getpass import getpass
import imaplib
import sys
from time import sleep
import serial


class GmailUnreadCounter(object):
    SERIAL_PORT = '/dev/tty.usbmodemfa131'
    SERIAL_SPEED = 9600

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.login()

    def login(self):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        self.mail.login(self.email, self.password)
        print 'logged in'

    def get_unread_count(self):
        self.mail.select('INBOX')
        status, ids = self.mail.search(None, 'UNSEEN')
        self.mail.close()
        if status == 'OK':
            return len(ids[0].split(' '))
        return 0

    def send_to_serial(self, value):
        print 'sending to serial'
        connection = serial.Serial(self.SERIAL_PORT, self.SERIAL_SPEED, timeout=0, stopbits=serial.STOPBITS_TWO)
        connection.write(str(value))
        connection.close()
        print 'sent'

    def run(self):
        while True:
            try:
                c = self.get_unread_count()
                print 'count %s' % c
                self.send_to_serial(c)
                sleep(10)
            except KeyboardInterrupt:
                self.mail.close()
                self.mail.logout()
                sys.exit()


if __name__ == '__main__':
    login = raw_input('Enter your Gmail login: ')
    password = getpass(prompt='Enter your Gmail password: ')

    c = GmailUnreadCounter(login, password)
    c.run()