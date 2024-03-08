#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import run, put, env
import os


env.hosts = ['52.86.196.120', '100.24.235.246']
env.user = 'ubuntu'  # Assuming Ubuntu user for SSH access


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        print("Archive doesn't exist:", archive_path)
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_folder = '/data/web_static/releases/' + \
            archive_name.replace('.tgz', '')

        print("Uploading archive to the servers...")
        put(archive_path, '/tmp/')

        print("Creating directory for the new version...")
        run('mkdir -p {}'.format(archive_folder))

        print("Uncompressing the archive...")
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, archive_folder))

        print("Cleaning up...")
        run('rm /tmp/{}'.format(archive_name))
        run('mv {}/web_static/* {}'.format(archive_folder, archive_folder))
        run('rm -rf {}/web_static'.format(archive_folder))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(archive_folder))

        print("New version deployed successfully!")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False
