#!/usr/bin/env python3

import argparse
import sys

import pexpect


class Session(pexpect.spawn):
    def __init__(self):
        pexpect.spawn.__init__(
            self,
            "python",
            encoding="utf-8",
            timeout=10,
        )
        self.logfile_read = sys.stdout
        self.prompt = ">>> "
        self.delaybeforesend = 0.01
        self.expect_exact(self.prompt)

    def slowsend(self, tosend):
        for char in tosend:
            self.send(char)
            self.expect_exact(char)

    def waitprompt(self):
        self.expect_exact(self.prompt)

    def sendwait(self, tosend, towait=None):
        self.slowsend(tosend)
        towait = towait if towait is not None else self.prompt
        self.expect_exact(towait)

    def sleep(self, time=1):
        self.expect(pexpect.TIMEOUT, timeout=time)

    def sendsleep(self, tosend, time=0.3):
        self.send(tosend)
        self.sleep(time)

    def pquit(self):
        self.slowsend("quit()\r")
        self.expect(pexpect.EOF)
        self.wait()


def do_main():
    py = Session()
    py.sendwait("import tuzue\r")
    py.sendwait("""fruits = [ "avocado", "berry", "cherry", "durian", "eggfruit" ]\r""")
    py.slowsend("""favorite = tuzue.navigate(fruits, "What is your favorite fruit?")""")
    py.sleep()
    py.slowsend("\r")
    py.sleep()
    down = "\x1bOB"
    py.sendsleep(down)
    py.sendsleep(down)
    py.sendsleep(down)
    py.slowsend("e")
    py.sleep()
    py.sendsleep(down)
    py.slowsend("\r")
    py.waitprompt()
    py.sendwait("""print("Your favorite fruit is:", favorite)\r""")
    py.sleep(5)
    py.pquit()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    do_main()


if __name__ == "__main__":
    main()
