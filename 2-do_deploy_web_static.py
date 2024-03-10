#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['52.86.196.120', '100.24.235.246']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it
    """
    if not exists(archive_path):
        return False

    filename = archive_path.split('/')[-1]
    no_extension = filename.split('.')[0]
    release_path = f'/data/web_static/releases/{no_extension}'

    try:
        put(archive_path, '/tmp')
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{filename} -C {release_path}')
        run(f'rm /tmp/{filename}')
        run(f'mv {release_path}/web_static/* {release_path}/')
        run(f'rm -rf {release_path}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {release_path} /data/web_static/current')
        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False
