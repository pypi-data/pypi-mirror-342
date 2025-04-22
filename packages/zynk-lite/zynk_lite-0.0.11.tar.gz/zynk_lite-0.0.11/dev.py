# SPDX-FileCopyrightText: 2025-present Guille <guilleleiratemes@gmail.com>
#
# SPDX-License-Identifier: GPLv3

from src.zynk_lite import interpreter as intp
interpreter = intp.ZynkLInterpreter(debug=True)
case = """
func chao(x) {
    print x;
}
var x = 5;
call chao( x );
"""
interpreter.eval(case)