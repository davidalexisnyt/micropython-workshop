#! /bin/bash

echo "Installing Mosquitto MQTT broker..."
sudo apt install mosquitto mosquitto-clients -y

echo -n "Let's configure a user account for Mosquitto.  Enter a user name:  "
read userName

# Prompt the user for a password for the user. The password is stored encrypted in
# the specified password file. Mosquitto must then be configured to use the password
# file for authenticating users.
sudo mosquitto_passwd -c /etc/mosquitto/users $userName

# Disable anonymous logins so that a user and password are required to connect
printf "\nallow_anonymous false\npassword_file /etc/mosquitto/users\n" | sudo tee -a /etc/mosquitto/conf.d/default.conf > /dev/null

sudo service mosquitto stop
sudo service mosquitto start

printf "\nDone.  You can add more users with:\n\tsudo mosquitto_passwd /etc/mosquitto/users <new user name>\n"
