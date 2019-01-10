#!/usr/bin/python2

import sys
import ledger
import os
from collections import defaultdict
from datetime import date, timedelta
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def minus_month(d):
    first_day = d.replace(day=1)
    return first_day  - timedelta(days=1)

def same_month(a, b):
    return a.year == b.year and a.month == b.month

journal  = ledger.read_journal(os.environ['LEDGER_FILE'])
total = defaultdict(lambda : ledger.Balance())

today = date.today()
this_month = defaultdict(lambda : ledger.Balance())

last_month_today = minus_month(today)
last_month = defaultdict(lambda : ledger.Balance())

for post in journal.query(" ".join(sys.argv[1:])):
    total[str(post.account)] += post.amount
    if same_month(today, post.date):
        this_month[str(post.account)] += post.amount
    if same_month(last_month_today, post.date):
        last_month[str(post.account)] += post.amount

def fmt_amount(bal):
    if '-' in bal:
        return "\033[91m%s\033[0m" % bal
    else:
        return bal

widths = [12, 12, 12, 0]
def print_line(widths, *line):
    lr = ['>', '>', '>', "<"]
    line = [u"{:{}{}}".format(x.decode('utf-8'),l,w) for x,l, w in zip(line, lr, widths)]
    line[1:] = map(fmt_amount, line[1:])
    print u" ".join(line)

widths[-1] = max([len(unicode(str(x))) for x in total])

print_line(widths, "Total", "This Month", "Last Month", "")
for account in sorted(total.keys()):
    line = str(total[account]), str(this_month[account]), str(last_month[account]), str(account),
    print_line(widths, *line)
