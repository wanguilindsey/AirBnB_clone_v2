#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives using do_clean
"""

from fabric.api import local, run, lcd, env

env.hosts = ['52.86.196.120', '100.24.235.246']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """Deletes out-of-date archives"""
    number = int(number)
    if number < 0:
        return

    try:
        with lcd("versions"):
            local("ls -1t | tail -n +{} | xargs -I {{}} rm {{}}"
                  .format(number + 1))

        with cd("/data/web_static/releases"):
            run("ls -1t | tail -n +{} | xargs -I {{}} rm -rf {{}}"
                .format(number + 1))
    except Exception as e:
        print("Error:", e)
