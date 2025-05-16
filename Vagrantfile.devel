$prepare_environment = <<SCRIPT
dnf install -y npm python3.9 python3.9-pip sshpass

groupadd pandda -g 4200
useradd pandda -u 4201 -g 4200

firewall-cmd --permanent --add-port=5000/tcp
firewall-cmd --permanent --add-port=5001/tcp
firewall-cmd --reload
SCRIPT

$install_app_service = <<SCRIPT
mkdir /etc/ansible
echo -e "[defaults]\nhost_key_checking = False" > /etc/ansible/ansible.cfg

cd /web
npm i

cd /backend
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
su - pandda -c 'source /backend/venv/bin/activate && ansible-galaxy collection install community.docker --force'

chown -R pandda:pandda /backend
chown -R pandda:pandda /web
chown -R pandda:pandda /opt/pandda_playbooks
chown -R pandda:pandda /opt/pandda_autodiscovery

cat > /opt/start_pandda_webconf.sh <<SCRIPT2
#!/bin/bash

cd /web
npm i
npm run dev
SCRIPT2

cat > /opt/start_pandda_webconf_server.sh <<SCRIPT2
#!/bin/bash

cd /backend
source venv/bin/activate
flask --app pandda_webconf_server run --debug --host 0.0.0.0 --port 5001
SCRIPT2

chown pandda:pandda /opt/start_pandda_webconf.sh
chmod 0755 /opt/start_pandda_webconf.sh

chown pandda:pandda /opt/start_pandda_webconf_server.sh
chmod 0755 /opt/start_pandda_webconf_server.sh

cat > /etc/systemd/system/pandda_webconf.service <<SCRIPT2
[Unit]
Description=PANDDA Web Configuration Tool

[Service]
ExecStart=/opt/start_pandda_webconf.sh
Restart=always
User=pandda
Group=pandda


[Install]
WantedBy=default.target
SCRIPT2

cat > /etc/systemd/system/pandda_webconf_server.service <<SCRIPT2
[Unit]
Description=PANDDA Web Configuration Tool Server

[Service]
ExecStart=/opt/start_pandda_webconf_server.sh
Restart=always
User=pandda
Group=pandda


[Install]
WantedBy=default.target
SCRIPT2

systemctl daemon-reload
SCRIPT

$start_app = <<SCRIPT
systemctl enable --now pandda_webconf.service
systemctl enable --now pandda_webconf_server.service
SCRIPT

Vagrant.configure("2") do |config|
    config.vm.define "PANDDA-WEBCONF" do |panddawebconf|
        panddawebconf.vm.box = "generic/oracle9"
        panddawebconf.vm.network "forwarded_port", guest: 5000, host: 8080
        panddawebconf.vm.network "forwarded_port", guest: 5001, host: 8081

        config.vm.synced_folder "app", "/web", type: "rsync",
            owner: 4201,
            group: 4200,
            rsync__exclude: ".git/",
            rsync__exclude: "node_modules/",
            rsync__auto: true

        config.vm.synced_folder "backend", "/backend", type: "rsync",
            owner: 4201,
            group: 4200,
            rsync__exclude: ".git/",
            rsync__exclude: "venv/",
            rsync__auto: true

        config.vm.synced_folder "pandda_playbooks", "/opt/pandda_playbooks", type: "rsync",
            owner: 4201,
            group: 4200,
            rsync__auto: true

        config.vm.synced_folder "ansible", "/opt/pandda_autodiscovery", type: "rsync",
            owner: 4201,
            group: 4200,
            rsync__auto: true

        panddawebconf.vm.provision :shell, inline: $prepare_environment
        panddawebconf.vm.provision :shell, inline: $install_app_service
        panddawebconf.vm.provision :shell, inline: $start_app
    end
end
