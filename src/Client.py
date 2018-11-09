# CSCI 379
# Programming Project 1
# Jacob Feldman

from socket import *
import os
import time

ip = ''
port = 9999

ip = raw_input('IP?: ')

cSocket = socket(AF_INET, SOCK_STREAM)  # TCP connection
cSocket.connect((ip, port))


def user(sent):
    os.system('cls' if os.name == 'nt' else 'clear')
    y = raw_input('Input Username: ')[:8]
    while not y:
        os.system('cls' if os.name == 'nt' else 'clear')
        print ('Invalid Username try again')
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        y = raw_input('Input Username: ')[:8]
    cSocket.send(y)


def display(sent):
    os.system('cls' if os.name == 'nt' else 'clear')
    print sent


def display_respond(sent):
    os.system('cls' if os.name == 'nt' else 'clear')
    print sent
    y = raw_input('Input: ')[:8]
    while not y:
        y = '    '
    cSocket.send(y)


def display_enter(sent):
    os.system('cls' if os.name == 'nt' else 'clear')
    print sent
    raw_input('Input: ')[:8]
    cSocket.send('    ')


def parse(sent):
    command = ''
    sentence = ''
    if ' ' in sent:
        command = (sent.split(' ', 1)[0]).lower()
        sentence = sent.split(' ', 1)[1]
    if command == 'user':
        user(sentence)
    elif command == 'display':
        display(sentence)
    elif command == 'display_respond':
        display_respond(sentence)
    elif command == 'display_enter':
        display_enter(sentence)


while True:
    mSentence = cSocket.recv(1024)
    if not mSentence:
        break
    parse(mSentence)
    mSentence = ''

cSocket.close()
