#!/usr/bin/python3
# -*- coding: utf-8 -*-
# util 脚本执行处，避免python包导入的问题

import getopt
import sys

from utils import privilege_escalation, init

FUN_DICT = {
    "PE": privilege_escalation,
    "privilege_escalation": privilege_escalation,
    "INI": init,
    "init": init
}


def fun_name():
    return ", ".join(key for key in FUN_DICT.keys())


def fun_choose(opts_list):
    try:
        for [(o, a)] in opts_list:
            if o in ("-f", "--fun"):
                fun = FUN_DICT.get(a)
                if not fun:
                    print("Wrong function name!")
                    print(fun_name(), "can be chosen!")
                    return
                fun()
                return
    except Exception:
        print("-f or --fun= is necessary!")
    else:
        print("-f or --fun= is necessary!")


if __name__ == "__main__":
    opts_list = getopt.getopt(sys.argv[1:], "f:", ["fun="])
    fun_choose(opts_list)
