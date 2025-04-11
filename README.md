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

Configurator is distributed as ready-to-use [Dockerbox](https://hub.docker.com/r/plnyrich/pandda-devel). However, you can build it yourself.
<br />
You can also use vagrant with our prepared Vagrantfile.

Configurator is available at [localhost:8080](http://localhost:8080) **after installation.**
<br />
**Note** ports 8080 (frontend) and 8081 (backend) are used by PANDDA Configurator and **must not** be used by other processes.

### Dockerbox

Install the Dockerbox with Configurator by running:
```bash
docker pull plnyrich/pandda-configurator
docker run -d -p 8080:5000 -p 8081:5001 plnyrich/pandda-configurator
```

### Vagrant

Run the following commands to start the vagrant box with Configurator:
```bash
vagrant box add generic/oracle9 --provider=virtualbox
vagrant up
```

Note: It might take a while to fully provision & install the vagrant box.

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
