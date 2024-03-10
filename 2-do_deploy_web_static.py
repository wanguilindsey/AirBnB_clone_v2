#!/usr/bin/python3
"""
Fabric script that distributes an archive to the web servers using do_deploy
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['52.86.196.120', '100.24.235.246']

def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split("/")[-1]
        no_ext = archive_name.split(".")[0]
        release_path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run(f'mkdir -p {release_path}{no_ext}/')
        run(f'tar -xzf /tmp/{archive_name} -C {release_path}{no_ext}/')
        run(f'rm /tmp/{archive_name}')
        run(f'mv {release_path}{no_ext}/web_static/* {release_path}{no_ext}/')
        run(f'rm -rf {release_path}{no_ext}/web_static')
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {release_path}{no_ext}/ /data/web_static/current')
        return True
    except Exception as e:
        print(f"Error deploying archive: {e}")
        return False
