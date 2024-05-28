#!/usr/bin/python3
"""
Distributes an archive to my web servers,
using the function do_deploy
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['54.160.108.55', '100.26.164.108']
env.user = 'ubuntu'


def do_pack():
    '''
    Generates a tgz archive from the
    contents of the web_static folder
    '''
    try:
        local('mkdir -p versions')
        datetime_format = '%Y%m%d%H%M%S'
        archive_path = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(datetime_format))
        local('tar -cvzf {} web_static'.format(archive_path))
        print('web_static packed: {} -> {}'.format(archive_path,
              os.path.getsize(archive_path)))
        return archive_path  # Return the path of the created archive
    except Exception as e:
        print(e)
        return None


def do_deploy(archive_path):
    '''
    Deploy archive to web server
    '''
    if not os.path.exists(archive_path):
        return False

    try:
        # Extracting file name from path
        file_name = os.path.basename(archive_path)
        
        # Setting up file paths
        releases_path = '/data/web_static/releases/'
        current_link_path = '/data/web_static/current'

        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp')

        # Uncompress the archive to releases directory
        run('mkdir -p {}'.format(releases_path))
        run('tar -xzf /tmp/{} -C {}/{}'.format(file_name, releases_path, file_name[:-4]))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_name))

        # Move contents of web_static/ into current release folder
        run('mv {}/{}/web_static/* {}/{}'.format(releases_path, file_name[:-4], releases_path, file_name[:-4]))

        # Delete the web_static/ folder
        run('rm -rf {}/{}/web_static'.format(releases_path, file_name[:-4]))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf {}'.format(current_link_path))

        # Create a new symbolic link
        run('ln -s {}/{} {}'.format(releases_path, file_name[:-4], current_link_path))

        print('New version deployed!')
        return True
    except Exception as e:
        print(e)
        return False

