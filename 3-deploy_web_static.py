#!/usr/bin/python3
"""
distributes an archive to your web servers
"""
import os
from datetime import datetime
from fabric.api import *

env.hosts = ["54.237.117.152", "18.204.16.158"]
env.user = "ubuntu"
env.key = "~/.ssh/school"


def do_pack():
    """
    generates a .tgz archive
    """
    try:
        local("mkdir -p versions")
        tp = datetime.now().strftime("%Y%m%d%H%M%s")
        archive_path = ("versions/web_static_{}.tgz".format(tp))
        local("tar -cvzf versions/web_static_{}.tgz web_static/".format(tp))
        return (archive_path)
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    distributes an archive to your web servers
    Args:
        archive_path(str): path to archive to distribute
    Returns:
       Returns True if all operations have been done correctly,
       otherwise returns False
    """
    if not os.path.exists(archive_path):
        return (False)
    try:
        put(archive_path, "/tmp")
        file_name = archive_path.split('/')[-1]
        folder_name = file_name.split('.')[0]
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.
            format(file_name, folder_name))
        run('sudo rm /tmp/{}'.format(file_name))
        run('sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(folder_name, folder_name))
        run('sudo rm -rf /data/web_static/releases/{}//web_static/'
            .format(folder_name))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(folder_name))
        return (True)
    except Exception as e:
        return (False)


def deploy():
    """
    distributes an archive to your web servers
    """
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
