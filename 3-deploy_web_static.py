#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers using the function deploy
"""

from fabric.api import env
from fabric.operations import local, put, run
from datetime import datetime
from os.path import exists, isdir, basename
env.hosts = ['52.86.196.120', '100.24.235.246']


def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_path = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_path))
        return file_path
    except Exception as e:
        print("Error:", e)
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        archive_name = basename(archive_path)
        no_ext = archive_name.split(".")[0]
        release_path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(release_path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'
            .format(archive_name, release_path, no_ext))
        run('rm /tmp/{}'.format(archive_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(release_path, no_ext))
        run('rm -rf {0}{1}/web_static'.format(release_path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'
            .format(release_path, no_ext))
        return True
    except Exception as e:
        print("Error:", e)
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
