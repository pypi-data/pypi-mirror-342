"""
GPG utils, including manipulation of passwords managed by `pass` (see: https://www.passwordstore.org/).
"""
from __future__ import annotations

import logging
import os
import re
from argparse import ArgumentParser
from contextlib import contextmanager
from datetime import datetime
from getpass import getpass
from pathlib import Path
from tempfile import TemporaryDirectory, mkstemp
from uuid import uuid4

from zut import Literal, Secret, add_command, run_process

_logger = logging.getLogger(__name__)

_pass_dir = Path.home().joinpath('.password-store')
_gpg_id: str|None = '__unset__'


#region Usage as "pass" command

def add_arguments(parser: ArgumentParser):
    subparsers = parser.add_subparsers(title='subcommands')
    add_command(subparsers, _handle_list)
    add_command(subparsers, _handle_show)
    add_command(subparsers, _handle_insert)
    add_command(subparsers, _handle_rm)


def handle():
    """
    Manipulate passwords managed by `pass`, the "standard UNIX password manager", based on GPG.

    See: https://www.passwordstore.org/
    """
    return _handle_list()

handle.name = 'pass'


def _handle_list():
    """
    List password names.
    """
    gpg_id = get_pass_gpg_id()
    _logger.debug("GPG id: %s", gpg_id)
    for p in get_pass_list():
        print(p)

_handle_list.name = 'ls'


def _add_arguments(parser: ArgumentParser):
    parser.add_argument('name')

def _handle_show(name: str):
    """
    Show a password value.
    """
    try:
        password = get_pass(name, default=FileNotFoundError)
        print(password)
        return 0
    except FileNotFoundError as err:
        _logger.error(err)
        return 2

_handle_show.name = 'show'
_handle_show.add_arguments = _add_arguments


def _add_arguments(parser: ArgumentParser):
    parser.add_argument('name')
    parser.add_argument('password', nargs='?')

def _handle_insert(name: str, password: Secret|str|None = None):
    """
    Insert a new password.
    """
    if password is None:
        password = getpass("Password: ")
        confirm_password = None
        while confirm_password != password:
            if confirm_password is not None:
                _logger.error("Invalid password confirmation. Try again.")
            confirm_password = getpass("Confirm password: ")
    
    insert_pass(name, password)

_handle_insert.name = 'insert'
_handle_insert.add_arguments = _add_arguments


def _add_arguments(parser: ArgumentParser):
    parser.add_argument('name')

def _handle_rm(name: str):
    """
    Remove a password.
    """
    remove_pass(name)

_handle_rm.name = 'rm'
_handle_rm.add_arguments = _add_arguments

#endregion


def get_pass_list():
    passes: list[str] = []

    def recurse(dir: Path):
        for path in dir.iterdir():
            if path.is_dir():
                recurse(path)
            elif path.suffix == '.gpg' and not path.name.startswith('.'):
                path = path.relative_to(_pass_dir)
                passes.append(path.with_suffix('').as_posix())

    recurse(_pass_dir)
    passes.sort()
    return passes


def get_pass(name: str, default: str|type[Exception]|None = None):
    # ROADMAP: display info message if we detect pinentry will be launched (because this may be very long!) - See on personal computer! Or 'pass-diff'?
    # Use something like `ensure_gpg_key()` but with additional parameters such as `--pinentry-mode`?
    # See https://superuser.com/questions/739085/programmatically-determine-if-gpg-agent-will-ask-for-passphrase

    path = get_pass_path(name)
    if not path.exists():
        if isinstance(default, type):
            raise default(f"Pass not found: {name}")
        else:
            _logger.debug("Pass not found: %s at %s", name, path)
            return default

    _logger.debug("Decrypt pass %s at %s", name, path)
    return run_process(['gpg', '--batch', '--no-tty', '--decrypt', path], check=True, capture_output='rstrip').stdout


@contextmanager
def open_pass(file: str|os.PathLike, password_name: str, buffering: int = -1, encoding: str = None, newline: str = None, **kwargs):
    """
    Open a file encrypted using `pass` with the given password name.
    """
    password = get_pass(password_name, FileNotFoundError)
    yield from open_gpg_encrypted(file, password=password, buffering=buffering, encoding=encoding, newline=newline, **kwargs)


def insert_pass(name: str, password: Secret|str):
    path = get_pass_path(name)
    gpg_id = get_pass_gpg_id()
    if not gpg_id:
        raise ValueError(f"Pass GPG id not registered")
    
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_in_fd = None
    tmp_in = None
    tmp_out = path.with_name(f'{path.name}.tmp')
    try:
        tmp_in_fd, tmp_in = mkstemp()
        with open(tmp_in, 'w', encoding='utf-8') as fp:
            if isinstance(password, Secret):
                password = password.value
            fp.write(password)
        os.close(tmp_in_fd)
        tmp_in_fd = None
        
        _logger.debug("Encrypt pass %s at %s", name, path)
        run_process(['gpg', '--batch', '--no-tty', '--output', tmp_out, '--encrypt', '--recipient', gpg_id, tmp_in], check=True)
        if path.exists():
            archive_path = path.with_name(f".{path.stem}-{datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y%m%d-%H%M%S')}.gpg")
            oc = 2
            while archive_path.exists():
                archive_path = archive_path.with_name(f"{archive_path.stem}-{oc}.gpg")
                oc += 1
            path.rename(archive_path)
        tmp_out.rename(path)
    finally:
        if tmp_in_fd:
            os.close(tmp_in_fd)
        if tmp_in and os.path.exists(tmp_in):
           os.unlink(tmp_in)
        if tmp_out.exists():
            tmp_out.unlink()


def remove_pass(name: str):
    """
    Remove a password.
    """
    path = get_pass_path(name)
    if not path.exists():
        _logger.error(f"Pass does not exist: {name}")
        return False
    path.unlink()
    return True


def get_pass_gpg_id():
    global _gpg_id
    if _gpg_id == '__unset__':
        path = _pass_dir.joinpath('.gpg-id')
        if path.exists():
            _gpg_id = path.read_text('utf-8').strip()
        else:
            _gpg_id = None        
    return _gpg_id


def get_pass_path(name: str):
    if not name:
        raise ValueError(f"Name cannot be empty")
    name = re.sub(r'\\', '', name)
    parts = name.split('/')
    path = _pass_dir.joinpath(*parts)
    return path.with_name(f'{path.name}.gpg')


def ensure_gpg_key(key: str|None = None):
    """
    Ensure the given gpg key (by default: `pass` GPG key) is available in the GPG agent.
    """
    if not key:
        key = get_pass_gpg_id()
    
    # Make a signing test
    cp = run_process(['gpg', '--batch', '--no-tty', '--local-user', key, '-as'], input='test', stdout='disable', stderr='disable')
    if cp.returncode != 0:
        raise ValueError("Cannot use GPG key %s (gpg returned code %d)" % (key, cp.returncode))


def gpg_encrypt(file: str|os.PathLike, *, recipient: str = None, output: str|os.PathLike = None, delete_existing_encrypted = False, delete_original_clear = False):
    if not recipient:
        recipient = get_pass_gpg_id()
    if not output:
        output = f"{file}.gpg"

    if delete_existing_encrypted:
        if os.path.exists(output):
            os.unlink(output)

    _logger.debug("Encrypt file %s", file)
    run_process(['gpg', '--batch', '--no-tty', '--output', output, '--encrypt', '--recipient', recipient, file], check=True)

    if delete_original_clear:
        os.unlink(file)


@contextmanager
def open_gpg_encrypted(file: str|os.PathLike, password: Secret|str|None = None, buffering: int = -1, encoding: str = None, newline: str = None, **kwargs):
    """
    Open a GPG encrypted file.
    """
    tmpdir = TemporaryDirectory()
    fp = None
    try:
        tmp = os.path.join(tmpdir.name, str(uuid4()))

        _logger.debug("Decrypt %s to %s%s", file, tmp, ' using a password' if password is not None else '')
        args = ['gpg', '--batch', '--no-tty', '--output', tmp, '--decrypt', file]
        if password is not None:
            args += ['--passphrase-fd', '0']
            if isinstance(password, Secret):
                password = password.value
        run_process(args, check=True, input=password)
        
        fp = open(tmp, 'r', buffering=buffering, encoding=encoding, newline=newline, **kwargs)
        yield fp

    finally:
        if fp:
            fp.close()
        tmpdir.cleanup()
