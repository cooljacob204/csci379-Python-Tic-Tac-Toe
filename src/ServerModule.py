# CSCI 379
# Programming Project 1
# Jacob Feldman
# Splitting it into separate files because programming is the only thing I like neat

import threading
import time
import Game


class User:
    def __init__(self, user, conn):
        self.user = user
        self.conn = conn

    def main_menu(self):
        global users
        self.conn.send('display_respond Welcome to Tic Tac Toe!  Players online: ' + str(len(users)) + '\n\n'
                       'Enter the one of the following numbers to continue:\n'
                       '1: Find a game\n'
                       '2: Check who is online\n'
                       '3: Check who is in game\n'
                       '4: Check who is idle\n'
                       '5: Disconnect\n\n')
        sent = self.conn.recv(1024)
        self.parse(sent)

    def parse(self, sent):
        global users
        global users_idle
        global looking
        global in_game
        print('User ' + self.user + ': ' + sent)
        command = ''
        sentence = ''
        if ' ' in sent:
            command = (sent.split(' ', 1)[0]).lower()
            sentence = sent.split(' ', 1)[1]
        else:
            command = sent
        if command == '1':
            self.search()
            self.conn.recv(1024)
            self.main_menu()
        if command == 'unused':
            users_idle.append(self.user)
            self.conn.send('display_enter You are currently idle.\nPress enter to cancel')
            self.conn.recv(1024)
            users_idle.remove(self.user)
            self.main_menu()
        elif command == '2':
            self.conn.send('display_enter Users online: ' + ', '.join([str(i) for i in users]) + '\n\n'
                           'Press enter to continue')
            self.conn.recv(1024)
            self.main_menu()
        elif command == '3':
            self.conn.send('display_enter Users in Game: ' + ', '.join([str(i) for i in in_game]) + '\n\n'
                           'Press enter to continue')
            self.conn.recv(1024)
            self.main_menu()
        elif command == '4':
            self.conn.send('display_enter Idle Users: ' + ', '.join([str(i) for i in users_idle]) + '\n\n'
                           'Press enter to continue')
            self.conn.recv(1024)
            self.main_menu()
        elif command == '5':
            self.conn.close()
            users.remove(self.user)
            users_idle.remove(self.user)
        else:
            self.conn.send('display Invalid command please try again.')
            time.sleep(3)
            self.main_menu()

    def search(self):
        self.conn.send('display Looking for lobby, please wait...')
        global looking
        global in_game
        global users_idle
        try:
            looking
        except NameError:
            looking = [self]
        else:
            looking.append(self)
        users_idle.remove(self.user)
        try:
            in_game
        except NameError:
            while self in looking:
                time.sleep(1)
        while self in looking or self.user in in_game:
            time.sleep(1)
        users_idle.append(self.user)
        print 'Exiting Search'

    def game_end(self):
        global in_game
        in_game.remove(self.user)


def gamestart(a, b):
    game = Game.GameMain(a, b)
    game.start()
    del game
    print('game deleted')


def pairing():
    global looking
    global in_game
    while True:
        try:
            looking
        except NameError:
            time.sleep(1)
            continue
        if len(looking) > 1: #Going to use a queue system, if enough players connect it should be naturally random. Don't want some players waiting longer then others.
            threading.Thread(target=gamestart, args=(looking[0], looking[1])).start()
            try:
                in_game
            except NameError:
                in_game = [looking[0].user]
            else:
                in_game.append(looking[0].user)  # Not popping immediately because I need to make sure my other search loop in the threads don't break.
            in_game.append(looking[1].user)
            del looking[0]
            del looking[0]
        if len(looking) < 2:
            time.sleep(1)


def getusername(conn):
    while True:
        global users
        global users_idle
        conn.send('user ')
        user = conn.recv(1024)
        try:
            users
        except NameError:
            users = [user]
            users_idle = [user]
            print 'User ' + user + ' connected'
            return user
        if user in users:
            conn.send('display invalid username')
            time.sleep(3)
        else:
            users.append(user)
            users_idle.append(user)
            print 'User ' + user + ' connected'
            return user


def serverclient(conn, addr):
    global users
    global users_idle
    client = User(getusername(conn), conn)
    client.main_menu()
    users.remove(client.user)
    users_idle.remove(client.user)
