# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Ensure the /data directory exists
file { '/data':
  ensure => directory,
}

# Ensure the /data/web_static directory structure exists
file { '/data/web_static':
  ensure => directory,
}

file { '/data/web_static/releases':
  ensure => directory,
}

file { '/data/web_static/shared':
  ensure => directory,
}

file { '/data/web_static/releases/test':
  ensure => directory,
}

# html file for testing
file { '/data/web_static/releases/test/index.html':
  content => '<html><head></head><body>Bernadette@alx</body></html>',
}

# Create a symbolic link to the latest release
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
}

# Ensure ownership of the /data directory is set to ubuntu user and group recursively
file { '/data':
  owner  => 'ubuntu',
  group  => 'ubuntu',
  recurse => true,
}

# Configure Nginx to serve the static content
file { '/etc/nginx/sites-available/default':
  ensure  => present,
  content => "
    server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location /hbnb_static {
            alias /data/web_static/current/;
        }
    }
  ",
  notify => Service['nginx'],
}

# Restart Nginx if the configuration changes
service { 'nginx':
  ensure  => running,
  enable  => true,
  require => File['/etc/nginx/sites-available/default'],
}
