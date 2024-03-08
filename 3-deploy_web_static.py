#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import local, run, env
from datetime import datetime
import os

env.hosts = ['52.86.196.120', '100.24.235.246']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    local("mkdir -p versions")
    current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    file_path = "versions/web_static_{}.tgz".format(current_time)
    result = local("tar -cvzf {} web_static".format(file_path))
    if result.failed:
        return None
    print("web_static packed: {} -> {}Bytes".format(file_path,
                                                    result.stdout.split()[-2]))
    return file_path


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        print("Archive doesn't exist:", archive_path)
        return False

    file_name = archive_path.split("/")[-1]
    file_name_no_ext = file_name.split(".")[0]
    remote_path = "/tmp/{}".format(file_name)
    release_path = "/data/web_static/releases/{}/".format(file_name_no_ext)

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(release_path))
        run("tar -xzf {} -C {}".format(remote_path, release_path))
        run("rm {}".format(remote_path))
        run("mv {}web_static/* {}".format(release_path, release_path))
        run("rm -rf {}web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False


def deploy():
    """
    Calls do_pack and do_deploy functions
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
