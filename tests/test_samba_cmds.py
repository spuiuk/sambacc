#
# sambacc: a samba container configuration tool
# Copyright (C) 2021  John Mulligan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

import sambacc.samba_cmds


def test_create_samba_command():
    cmd = sambacc.samba_cmds.SambaCommand("hello")
    assert cmd.name == "hello"
    cmd2 = cmd["world"]
    assert cmd.name == "hello"
    assert list(cmd) == ["hello"]
    assert list(cmd2) == ["hello", "world"]


def test_debug_command():
    cmd = sambacc.samba_cmds.SambaCommand("beep", debug="5")
    assert list(cmd) == ["beep", "--debuglevel=5"]


def test_global_debug():
    sambacc.samba_cmds.set_global_debug("7")
    try:
        cmd = sambacc.samba_cmds.SambaCommand("cheep")
        assert list(cmd) == ["cheep", "--debuglevel=7"]
    finally:
        sambacc.samba_cmds.set_global_debug("")


def test_global_prefix():
    sambacc.samba_cmds.set_global_prefix(["bob"])
    try:
        cmd = sambacc.samba_cmds.SambaCommand("deep")
        assert list(cmd) == ["bob", "deep"]
    finally:
        sambacc.samba_cmds.set_global_prefix([])


def test_command_repr():
    cmd = sambacc.samba_cmds.SambaCommand("doop")
    cr = repr(cmd)
    assert cr.startswith("SambaCommand")
    assert "doop" in cr


def test_encode_none():
    res = sambacc.samba_cmds.encode(None)
    assert res == b""


def test_execute():
    import os

    cmd = sambacc.samba_cmds.SambaCommand("true")
    pid = os.fork()
    if pid == 0:
        sambacc.samba_cmds.execute(cmd)
    else:
        _, status = os.waitpid(pid, 0)
        assert status == 0
