# Puppet manifest to set up the web servers for the deployment of web_static

# Install Nginx if not already installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories if they don't exist
file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>
<head>
</head>
<body>Holberton School</body>
</html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create symbolic link if it doesn't exist
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Update Nginx configuration
file_line { 'nginx_config':
  ensure => present,
  path   => '/etc/nginx/sites-available/default',
  line   => 'location /hbnb_static { alias /data/web_static/current; }',
}

# Restart Nginx to apply changes
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['nginx_config'],
}
