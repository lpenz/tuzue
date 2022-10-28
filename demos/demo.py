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


def demo_pdb():
    py = Session()
    py.sendwait("import tuzue.inspect\r")
    py.sendwait("import tuzue\r")
    py.slowsend('r = tuzue.inspect.inspect(tuzue, "tuzue")')
    py.sleep(2)
    py.sendsleep("\r", 1)
    for _ in range(6):
        py.sendsleep(DOWN)
    py.sendsleep("\r", 1)
    py.sendsleep("c", 1)
    py.sendsleep("\r", 1)
    py.sendsleep("B", 1)
    py.sendsleep("\r", 1)
    py.slowsend("a")
    py.sleep(1)
    py.sendsleep(DOWN, 1)
    py.sendsleep("\r", 1)
    py.sendsleep("\r", 2)
    py.sendwait("\r")
    py.slowsend("print(tuzue.ui.curses.UiCursesBase.edit_actions_default)\r")
    py.sleep(5)
    py.pquit()


def main():
    demos = {"demo-navigate": demo_navigate, "demo-pdb": demo_pdb}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("demo", nargs=1, choices=demos.keys())
    args = parser.parse_args()
    demos[args.demo[0]]()


if __name__ == "__main__":
    main()
