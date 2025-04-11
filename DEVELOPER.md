# Git Submodules Update

The submodules can be updated to the newest version by running:
```
git submodule update --init --recursive
git submodule update --remote
```

# Devel Environment

Dockerfile and Vagrantfile are available in this project. The default settings is to run the npm server with its **devel** features.

Firstly, you must download submodules:
```bash
git submodule init
```

## Vagrant

You can build the box locally by running:
```bash
vagrant box add generic/oracle9 --provider=virtualbox
vagrant up
```

Connect to the virtual machine:
```bash
vagrant ssh
```

See logs of PANDDA services:
```bash
vagrant ssh
sudo su -
journalctl -u pandda_webconf.service # frontend with Vue.js and vite server
journalctl -u pandda_webconf_server.service # backend with Flask
```

## Docker
You can build the box locally by running:
```
docker build -t pandda-webconf .
docker run -d -p 8080:5000 -p 8081:5001 --name pandda-webconf pandda-webconf
```

Connect to the virtual machine:
```
docker exec -i -t pandda-webconf bash
```

See logs of PANDDA services:
```
docker logs <containerID>
```
