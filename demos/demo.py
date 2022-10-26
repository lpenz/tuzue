#!/usr/bin/env python3

import argparse
import sys

import pexpect

DOWN = "\x1bOB"


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
        self.delaybeforesend = 0.02
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


def demo_navigate():
    py = Session()
    py.sendwait("import tuzue\r")
    py.sendwait("""fruits = [ "avocado", "berry", "cherry", "durian", "eggfruit" ]\r""")
    py.slowsend("""favorite = tuzue.navigate(fruits, "What is your favorite fruit?")""")
    py.sleep()
    py.slowsend("\r")
    py.sleep()
    py.sendsleep(DOWN)
    py.sendsleep(DOWN)
    py.sendsleep(DOWN)
    py.slowsend("e")
    py.sleep()
    py.sendsleep(DOWN)
    py.slowsend("\r")
    py.waitprompt()
    py.sendwait("""print("Your favorite fruit is:", favorite)\r""")
    py.sleep(5)
    py.pquit()


def main():
    demos = {"demo-navigate": demo_navigate}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", nargs=1, choices=demos.keys())
    args = parser.parse_args()
    demos[args.demo[0]]()


if __name__ == "__main__":
    main()
