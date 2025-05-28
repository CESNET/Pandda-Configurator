<div align="center">
<picture>
  <source srcset="https://raw.githubusercontent.com/CESNET/Pandda-Configurator/refs/heads/main/img/logo_horizontal_white.svg" media="(prefers-color-scheme: dark)">
  <img src="https://raw.githubusercontent.com/CESNET/Pandda-Configurator/refs/heads/main/img/logo_horizontal_black.svg">
</picture>
</div>

# PANDDA Configurator
PANDDA Configurator is used to configure and provision network monitoring infrastructure with [ipfixprobe](https://github.com/CESNET/ipfixprobe), [ipfixcol2](https://github.com/CESNET/ipfixcol2), and [ADiCT](https://github.com/CESNET/Pandda-ADiCT).

Step-by-step configuration guide is available as a website that provision both network probes and the collector server.

## Installation

Configurator is distributed as ready-to-use [Dockerbox](https://hub.docker.com/r/projectpandda/configurator). However, you can build it yourself.
<br />
You can also use [Vagrantbox](https://portal.cloud.hashicorp.com/vagrant/discover/projectpandda/configurator) with our prepared [Vagrantfile](Vagrantfile).

Configurator is available at [localhost:8080](http://localhost:8080) **after installation.**
<br />
**Note** ports 8080 (frontend) and 8081 (backend) are used by PANDDA Configurator (in both Docker and Vagrant boxes) and **must not** be used by other processes.

### Dockerbox

Install the Dockerbox with Configurator by running:
```bash
docker pull projectpandda/configurator
docker run -d -p 8080:5000 -p 8081:5001 projectpandda/configurator
```

### Vagrantbox

Install the Vagrantbox with Configurator by putting [Vagrantfile](Vagrantfile) to the target folder and running:
```bash
vagrant up
```

## Running from the local repository

You can also run Docker and Vagrant from the locally cloned repository without using the prepared boxes.

Docker can be started by running:
```
docker build -t pandda-webconf .
docker run -d -p 8080:5000 -p 8081:5001 --name pandda-webconf pandda-webconf
```

Vagrant can be started by running:
```
mv Vagrantfile Vagrantfile.bak # optionally: backup the Vagrantfile
mv Vagrantfile.devel Vagrantfile
vagrant up
```

# Documentation

You can find PANDDA Configurator documentation at [PANDDA Docs](https://pandda.cesnet.cz/).
<br />
The documentation includes screenshots and step-by-step guige together with information about all other components of the PANDDA project.

# License

Configurator, PAssive Network Device Discovery and Analysis
<br />
[BSD-3-Clause license](LICENSE)
<br />
Copyright ©: 2025, CESNET z.s.p.o.


### Acknowledgement

<div>
Supported as part of financial support to third parties (FSTP) within the project National Coordination Center in the Czech Republic (NCC-CZ, project no. 101127941) co-financed by the Digital Europe program.
</div>
<br />

<div align="center">
<picture>
  <img src="https://raw.githubusercontent.com/CESNET/Pandda-Configurator/refs/heads/main/img/eccc_badge.png?raw=true" width="150">
</picture>
<picture>
  <img src="https://raw.githubusercontent.com/CESNET/Pandda-Configurator/refs/heads/main/img/ncc_badge.png?raw=true" width="165">
</picture>
<picture>
  <img src="https://raw.githubusercontent.com/CESNET/Pandda-Configurator/refs/heads/main/img/eu-badge.png?raw=true" width="200">
</picture>
</div>
<br />
