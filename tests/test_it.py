# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import shutil
import sys
from pathlib import Path
from tempfile import mkdtemp
from textwrap import dedent

from flake8.main import main as flake8_main

from .utils import captured_stdout

MODULE_DIR = Path(__file__).parent.resolve()
TMP_DIR = None


def setup_module(module):
    global TMP_DIR
    TMP_DIR = Path(mkdtemp())


def teardown_module(module):
    shutil.rmtree(str(TMP_DIR))


def run_flake8(file_contents):
    with open(str(TMP_DIR / "example.py"), 'w') as tempf:
        tempf.write(dedent(file_contents.lstrip('\n')).strip() + '\n')

    orig_dir = os.getcwd()
    os.chdir(str(TMP_DIR))
    orig_args = sys.argv
    try:
        # Can't pass args to flake8 but can set to sys.argv
        sys.argv = [
            'flake8',
            '--jobs', '1',
            '--exit-zero',
            'example.py',
        ]

        # Run it
        with captured_stdout() as stdout:
            flake8_main()
        out = stdout.getvalue().strip()
        lines = out.split('\n')
        if lines[-1] == '':
            lines = lines[:-1]
        return lines
    finally:
        sys.argv = orig_args
        os.chdir(orig_dir)


def test_C400_list_pass_1():
    errors = run_flake8("""
        foo = [x for x in range(10)]
    """)
    assert errors == []


def test_C400_list_fail_1():
    errors = run_flake8("""
        foo = list(x for x in range(10))
    """)
    assert errors == [
        'example.py:1:7: C400 Unnecessary generator - rewrite as a list comprehension.',
    ]


def test_C400_list_fail_2():
    errors = run_flake8("""
        foobar = list(
            str(x)
            for x
            in range(10)
        )
    """)
    assert errors == [
        'example.py:1:10: C400 Unnecessary generator - rewrite as a list comprehension.',
    ]


def test_C400_set_pass_1():
    errors = run_flake8("""
        foo = {x for x in range(10)}
    """)
    assert errors == []


def test_C400_set_fail_1():
    errors = run_flake8("""
        foo = set(x for x in range(10))
    """)
    assert errors == [
        'example.py:1:7: C400 Unnecessary generator - rewrite as a set comprehension.',
    ]


def test_C400_set_fail_2():
    errors = run_flake8("""
        foobar = set(
            str(x) for x
            in range(10)
        )
    """)
    assert errors == [
        'example.py:1:10: C400 Unnecessary generator - rewrite as a set comprehension.',
    ]


def test_C400_dict_pass_1():
    errors = run_flake8("""
        foo = {x: str(x) for x in range(10)}
    """)
    assert errors == []


def test_C400_dict__fail_1():
    errors = run_flake8("""
        foo = dict((x, str(x)) for x in range(10))
    """)
    assert errors == [
        'example.py:1:7: C400 Unnecessary generator - rewrite as a dict comprehension.',
    ]


def test_C400_dict__fail_2():
    errors = run_flake8("""
        foobar = dict(
            (x, str(x))
            for x
            in range(10)
        )
    """)
    assert errors == [
        'example.py:1:10: C400 Unnecessary generator - rewrite as a dict comprehension.',
    ]


def test_C401_set_pass_1():
    errors = run_flake8("""
        foo = {x for x in range(10)}
    """)
    assert errors == []


def test_C401_set_fail_1():
    errors = run_flake8("""
        foo = set([x for x in range(10)])
    """)
    assert errors == [
        'example.py:1:7: C401 Unnecessary list comprehension - rewrite as a set comprehension.',
    ]


def test_C401_dict_pass_1():
    errors = run_flake8("""
        foo = {x: x for x in range(10)}
    """)
    assert errors == []


def test_C401_dict_fail_1():
    errors = run_flake8("""
        foo = dict([(x, x) for x in range(10)])
    """)
    assert errors == [
        'example.py:1:7: C401 Unnecessary list comprehension - rewrite as a dict comprehension.',
    ]


def test_C402_set_pass_1():
    errors = run_flake8("""
        foo = set(range)
    """)
    assert errors == []


def test_C402_set_fail_1():
    errors = run_flake8("""
        foo = set([])
    """)
    assert errors == [
        'example.py:1:7: C402 Unnecessary list literal - rewrite as a set literal.',
    ]


def test_C402_set_fail_2():
    errors = run_flake8("""
        foo = set([1])
    """)
    assert errors == [
        'example.py:1:7: C402 Unnecessary list literal - rewrite as a set literal.',
    ]


def test_C402_dict_pass_1():
    errors = run_flake8("""
        foo = dict(range)
    """)
    assert errors == []


def test_C402_dict_fail_1():
    errors = run_flake8("""
        foo = dict([])
    """)
    assert errors == [
        'example.py:1:7: C402 Unnecessary list literal - rewrite as a dict literal.',
    ]


def test_C402_dict_fail_2():
    errors = run_flake8("""
        foo = dict([(1, 2)])
    """)
    assert errors == [
        'example.py:1:7: C402 Unnecessary list literal - rewrite as a dict literal.',
    ]
