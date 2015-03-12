__author__ = 'sunzhennan'

import time

MONTH_DAY = {
    1 : 31,
    2 : 29,
    3 : 31,
    4 : 30,
    5 : 31,
    6 : 30,
    7 : 31,
    8 : 31,
    9 : 30,
    10 : 31,
    11 : 30,
    12 : 31
}
class lbeymd():

    def __init__(self, str="today"):
        if str is None or len(str) == 0 or str == "today":
            self.valid = True;
            now = time.localtime()
            self.year = now.tm_year
            self.month = now.tm_mon
            self.day = now.tm_mday
        else:
            self.valid = False
            self.parse(str)

    def parse(self, str):
        if len(str) != 8 or not str.isdigit():
            return
        self.year = int(str[:4])
        self.month = int(str[4:6])
        self.day = int(str[6:])
        if self.year < 2000 or self.year > 3000 or self.month < 1 or self.month > 12:
            return
        if self.day < 1 or self.day > MONTH_DAY[self.month]:
            return

        self.valid = True

    def toString(self):
        if not self.valid:
            raise Exception("invalid ymd object")
        return "%04d%02d%02d" % (self.year, self.month, self.day)

    def inc(self):
        if not self.valid:
            raise Exception("invalid ymd object")
        self.day += 1
        if self.day > MONTH_DAY[self.month]:
            self.day = 1
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
        return

if __name__ == "__main__":
    ymd = lbeymd()
    ymd.inc()
    print ymd.toString()
