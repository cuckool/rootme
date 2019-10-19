import socket
import time
import re
import math
import zlib
import codecs

SERVER = "irc.root-me.org"
CHANNEL = "#root-me_challenge"
NICKNAME = "gordonbot"


class IRCBot:

    def __init__(self, nickname, channel, server, port=6667):
        self.nickname = nickname
        self.channel = channel
        self.server = server
        self.port = port
        self.ircsock = None
        self.join()

    def join(self):
        """
        connect to the IRC chat and join the channel
        """
        ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ircsock.connect((self.server, self.port))
        ircsock.send(bytes("NICK " + self.nickname + "\n", "UTF-8"))
        ircsock.send(
            bytes("USER " + self.nickname + " " + self.nickname + " " + self.nickname + " " + self.nickname + "\n",
                  "UTF-8"))
        ircsock.send(bytes("JOIN " + self.channel + "\n", "UTF-8"))
        self.ircsock = ircsock

    def send_private_msg(self, msg, target):
        """
        Send private message to bot
        :param msg: message to be sent
        :param target: username of channel
        :return:
        """
        full_message = "PRIVMSG " + target + " :" + msg + "\n"
        print(full_message)
        self.ircsock.send(bytes(full_message, "UTF-8"))

    def run(self, init_msg, func, target="Candy"):
        self.send_private_msg(init_msg, target)
        while True:
            ircmsg = self.ircsock.recv(2048).decode("UTF-8")
            print(ircmsg)
            if "password" in ircmsg or "Bad reponse!" in ircmsg:
                break
            if "{}@root-me.org PRIVMSG {}".format(target, self.nickname) in ircmsg:
                ret_message = func(ircmsg)
                if ret_message is not None:
                    self.send_private_msg("{} -rep {}\n".format(init_msg, ret_message), "Candy")


def func_challenge_1(ircmsg):
    try:
        num_1, num_2 = re.findall('\d+', ircmsg)
        num_1, num_2 = int(num_1), int(num_2)
        return round(math.sqrt(num_1) * num_2, 2)
    except Exception as e:
        print(e)
        return None


def func_challenge_2(ircmsg):
    b64_chain = ircmsg.split(':')[-1].encode('ascii')
    return codecs.decode(b64_chain, 'base64').decode()


def func_challenge_3(ircmsg):
    rot13_chain = ircmsg.split(':')[-1]
    return codecs.encode(rot13_chain, 'rot_13')


def func_challenge_4(ircmsg):
    b64_chain = ircmsg.split(':')[-1].encode('ascii')
    zlib_data = codecs.decode(b64_chain, 'base64')
    return zlib.decompress(zlib_data).decode()


if __name__ == '__main__':
    bot = IRCBot(NICKNAME, CHANNEL, SERVER)
    time.sleep(1)
    bot.run(init_msg="!ep4", func=func_challenge_4)
