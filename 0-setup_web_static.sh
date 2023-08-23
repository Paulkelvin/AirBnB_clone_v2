#!/usr/bin/env bash
#script that sets up your web servers for the deployment of web_static
sudo apt -y update
sudo apt -y install nginx
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/current
sudo mkdir -p /data/web_static/shared/
echo "html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/  /data/web_static/current
sudo chown -R ubuntu /data/
sudo chgrp -R ubuntu /data/
hostname=$(hostname)
uri=$uri
sudo echo "server {
        listen 80 default_server;
        add_header X-Served-By $hostname;
        listen [::]:80 default_server;
        root /var/www/html;
        index index.html;
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
        }
        location /redirect_me {
            return 301 https://www.youtube.com;
        }
        error_page 404 /custom_404.html;

        location /hbnb_static/ {
            alias /data/web_static/current/;
            index index.html;
	}
}" | sudo tee /etc/nginx/sites-available/default
sudo service nginx restart
