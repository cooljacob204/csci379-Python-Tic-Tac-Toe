# CSCI 379
# Programming Project 2
# Jacob Feldman

import time


class GameMain:
    def __init__(self, p1, p2):
        self.player1 = p1
        self.player2 = p2
        self.gamestate = [['1', '2', '3'],
                          ['4', '5', '6'],
                          ['7', '8', '9']]

    def start(self):
        self.game_send(self.player2, self.player1, 'X', 'O')
        i = 0
        while True:
            self.game_send(self.player1, self.player2, 'O', 'O')
            self.game_send(self.player1, self.player2, 'O', 'X')
            i += 1
            if self.winstate() == 'O':
                self.game_send(self.player1, self.player2, 'O', 'w')
                self.game_send(self.player2, self.player1, 'X', 'w')
                break
            elif i == 9:
                self.game_send(self.player2, self.player1, 'X', 'l')
                self.game_send(self.player1, self.player2, 'O', 'l')
                break
            self.game_send(self.player2, self.player1, 'X', 'X')
            self.game_send(self.player2, self.player1, 'X', 'O')
            i += 1
            if self.winstate() == 'X':
                self.game_send(self.player2, self.player1, 'X', 'w')
                self.game_send(self.player1, self.player2, 'O', 'w')
                break
            elif i == 9:
                self.game_send(self.player2, self.player1, 'X', 'l')
                self.game_send(self.player1, self.player2, 'O', 'l')
                break
        self.player1.game_end()
        self.player2.game_end()

    def move(self, p, o, z, turn): #p is player o is opponent and z is your type; ie o or x turn = 'w' means win
        y = p.conn.recv(1024)
        if y == '1':
            if self.gamestate[0][0] == '1':
                self.gamestate[0][0] = turn
                return
            else:
                p.conn.send('display Invalid move try again')
                time.sleep(3)
                self.game_send(p, o, z, turn)
        if y == '2':
            if self.gamestate[0][1] == '2':
                self.gamestate[0][1] = turn
                return
            else:
                p.conn.send('display Invalid move try again')
                time.sleep(3)
                self.game_send(p, o, z, turn)
        if y == '3':
            if self.gamestate[0][2] == '3':
                self.gamestate[0][2] = turn
                return
            else:
                p.conn.send('display Invalid move try again')
                time.sleep(3)
                self.game_send(p, o, z, turn)
        if y == '4':
            if self.gamestate[1][0] == '4':
                self.gamestate[1][0] = turn
                return
            else:
                p.conn.send('display Invalid move try again')
                time.sleep(3)
                self.game_send(p, o, z, turn)
        if y == '5':
            if self.gamestate[1][1] == '5':
                self.gamestate[1][1] = turn
                return
            else:
                p.conn.send('display Invalid move try again')
                time.sleep(3)
                self.game_send(p, o, z, turn)
        if y == '6':
            if self.gamestate[1][2] == '6':
                self.gamestate[1][2] = turn
                return
            else:
                p.conn.send('display Invalid move try again')
                time.sleep(3)
                self.game_send(p, o, z, turn)
        if y == '7':
            if self.gamestate[2][0] == '7':
                self.gamestate[2][0] = turn
                return
            else:
                p.conn.send('display Invalid move try again')
                time.sleep(3)
                self.game_send(p, o, z, turn)
        if y == '8':
            if self.gamestate[2][1] == '8':
                self.gamestate[2][1] = turn
                return
            else:
                p.conn.send('display Invalid move try again')
                time.sleep(3)
                self.game_send(p, o, z, turn)
        if y == '9':
            if self.gamestate[2][2] == '9':
                self.gamestate[2][2] = turn
                return
            else:
                p.conn.send('display Invalid move try again')
                time.sleep(3)
                self.game_send(p, o, z, turn)

    def game_send(self, p, o, z, turn): #p is player o is opponent and z is your type; ie o or x turn = 'w' means win L means no winners
        if z == turn:
            p.conn.send('display_respond In game against: ' + o.user +
                        '\nYou are ' + z + '. Currently it is your turn'
                        '\n\n\n\n' +
                        self.return_state(self.gamestate))
            self.move(p, o, z, turn)

        elif turn != 'w' and turn != 'l':
            p.conn.send('display In game against: ' + o.user +
                        '\nYou are ' + z + '. Currently it is ' + turn + '\'s turn'
                        '\n\n\n\n' +
                        self.return_state(self.gamestate))
        if turn == 'w':
            if z == self.winstate():
                p.conn.send('display_enter In game against:' + o.user +
                            '\nYOU WON!!!!!!!'
                            '\n\n\n\n' +
                            self.return_state(self.gamestate) +
                            '\nPress Enter to continue: ')
            else:
                p.conn.send('display_enter In game against:' + o.user +
                            '\nSorry you lost :('
                            '\n\n\n\n' +
                            self.return_state(self.gamestate) +
                            '\nPress Enter to continue: ')
        if turn == 'l':
            p.conn.send('display_enter In game against:' + o.user +
                        '\nGame was a tie.'
                        '\n\n\n\n' +
                        self.return_state(self.gamestate) +
                        '\nPress Enter to continue: ')

    def return_state(self, y):
        return ('\033[4m' +
                y[0][0] + '|' + y[0][1] + '|' + y[0][2] + '\n' +
                y[1][0] + '|' + y[1][1] + '|' + y[1][2] + '\n''\033[0m' +
                y[2][0] + '|' + y[2][1] + '|' + y[2][2])

    def winstate(self):
        for i in range(0, 3):
            if self.wdown(0, i, (self.gamestate[0][i])):
                return self.gamestate[0][i]

        for i in range(0, 3):
            if self.wright(i, 0, (self.gamestate[i][0])):
                return self.gamestate[i][0]

        if self.wdiag(0, 0):
            return self.wdiag(0, 0)

        else:
            return 0

    def wdown(self, x, y, p):
        if self.gamestate[x][y] != p:
            return False
        else:
            if x < 2:
                return self.wdown(x+1, y, p)
            else:
                return self.gamestate[x][y]

    def wright(self, x, y, p):
        if self.gamestate[x][y] != p:
            return False
        else:
            if y < 2:
                return self.wright(x, y+1, p)
            else:
                return self.gamestate[x][y]

    def wdiag(self, x, y):
        if (
            (self.gamestate[0][0] == self.gamestate[1][1] == self.gamestate[2][2]) or
            (self.gamestate[0][2] == self.gamestate[1][1] == self.gamestate[2][0])
        ):
            return self.gamestate[1][1]