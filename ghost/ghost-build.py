# H17I Github Actions Ghost Build System - https://github.com/Highway-17-Interactive/Ghost

from sys import exit as sys_exit

from platform import system

from os.path import exists

from subprocess import run, CalledProcessError

from json import load


def ghost_fail(code: int) -> None:
    print(f'Ghost Building Error: {code}')

    sys_exit(code)

print('[Ghost] Parsing build config...')

if not exists('ghost/ghost-build.json'): ghost_fail(1)

with open('ghost/ghost-build.json', 'r') as gb: gbc: dict = load(gb)

if 'CMainFile' not in gbc: ghost_fail(2)
if 'CType' not in gbc: ghost_fail(3)
if 'CFlags' not in gbc: ghost_fail(4)
if 'COutputWindows' not in gbc: ghost_fail(5)
if 'COutputLinux' not in gbc: ghost_fail(6)

cmf = gbc['CMainFile']

if not cmf or not exists(cmf): ghost_fail(7)

ct = gbc['CType']

if not ct or ct not in ['C', 'C++', 'CPP']: ghost_fail(8)

cf = gbc['CFlags']

cf = '' if not cf else ' ' + cf

co_win = gbc.get('COutputWindows', 'ghost-build-windows')
co_linux = gbc.get('COutputLinux', 'ghost-build-linux')

sys = system()

compiler = 'gcc' if ct == 'C' else 'g++'

if sys == 'Windows':
    cmd = f'{compiler} {cmf} /Fe:{co_win}.exe{cf}'

elif sys == 'Linux':
    cmd = f'{compiler} {cmf} -o {co_linux}{cf}'

else:
    ghost_fail(9)

print('[Ghost] Building...')

try:
    run(cmd, shell=True, check=True)
except CalledProcessError:
    ghost_fail(10)

print('[Ghost] Success!')

sys_exit(0)
