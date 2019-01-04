# -*- mode: ruby -*-
# vi: set ft=ruby :

# https://www.vagrantup.com/docs/
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/cosmic64" # https://cloud-images.ubuntu.com

  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", "4096"]
    vb.name = "edn_format"
  end

  # https://www.vagrantup.com/docs/provisioning/shell.html
  config.vm.provision "shell", path: "install.sh", privileged: false, sensitive: true
end
