#!/usr/bin/python3
"""
    Generates a .tgz archive from contents of
    the web_static folder of your AirBnB Clone
    repo, using the function do_pack.
<<<<<<< HEAD

    def do_pack():
    All files must be added to the final archive
    and stored in the folder "versions"

    The name of the archive created must be
    web_static_<year><month><day><hour><minute><second>.tgz

    The function do_pack must return the archive
    path if the archive has been correctly generated.
    Otherwise, it should return None
=======
>>>>>>> cad2f8870189f452856cbf2ffe1f5e3ee3cb985d
"""
import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
<<<<<<< HEAD
    """Compresses the web_static folder into a .tgz archive"""
=======
    """Compresses the web_static folder."""
>>>>>>> cad2f8870189f452856cbf2ffe1f5e3ee3cb985d
    try:
        day = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_N = "versions/web_static_{}.tgz".format(day)
        local("tar -czvf {} web_static".format(file_N))
        return file_N
    except FileNotFoundError:
        return None