#!/usr/bin/python3
"""
Fabric script that distributes an archive to the web servers using do_deploy
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['52.86.196.120', '100.24.235.246']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        archive_name = archive_path.split("/")[-1]
        no_ext = archive_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(archive_name, path, no_ext))
        run('rm /tmp/{}'.format(archive_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except Exception as e:
        print("Error:", e)
        return False
