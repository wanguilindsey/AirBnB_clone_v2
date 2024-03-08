#!/usr/bin/env bash
# sets up the web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file for testing
echo "<html>
<head>
</head>
<body>Holberton School</body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link if it doesn't exist
if [ ! -L /data/web_static/current ]; then
    sudo ln -sf /data/web_static/releases/test /data/web_static/current
fi

# Set ownership of /data folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data

# Update Nginx configuration
config="location /hbnb_static {\n\talias /data/web_static/current;\n}\n"
sudo sed -i "/server_name _;/a $config" /etc/nginx/sites-available/default

# Restart Nginx to apply changes
sudo service nginx restart

exit 0
