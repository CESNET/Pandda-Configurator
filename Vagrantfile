Vagrant.configure("2") do |config|
    config.vm.box = "projectpandda/configurator"
    config.vm.network "forwarded_port", guest: 5000, host: 8080
    config.vm.network "forwarded_port", guest: 5001, host: 8081
end
