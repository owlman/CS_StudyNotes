vm_list = [
    {
        :name => "k8s-master",
        :eth1 => "192.168.100.21",
        :mem => "4096",
        :cpu => "2",
        :sshport => 22230
    },
    {
        :name => "k8s-worker1",
        :eth1 => "192.168.100.22",
        :mem => "2048",
        :cpu => "2",
        :sshport => 22231
    },
    {
        :name => "k8s-worker2",
        :eth1 => "192.168.100.23",
        :mem => "2048",
        :cpu => "2",
        :sshport => 22232
    }
]

Vagrant.configure(2) do |config|
    config.vm.box = "gusztavvargadr/ubuntu-server"
    config.vm.box_check_update = false
    Encoding.default_external = 'UTF-8'
    vm_list.each do |item|
        config.vm.define item[:name] do |vm_config|
            vm_config.vm.hostname = item[:name]
            vm_config.vm.network "public_network", ip: item[:eth1]
            vm_config.vm.network "forwarded_port", guest: 22, host: 2222, id: "ssh", disabled: "true"
            vm_config.vm.network "forwarded_port", guest: 22, host: item[:sshport]
            vm_config.vm.provider "virtualbox" do |vb|
                vb.memory = item[:mem];
                vb.cpus = item[:cpu];
                vb.name = item[:name];
            end
            vm_config.vm.provision "shell", path: "scripts/common.sh"
            if item[:name] == "k8s-master"
                vm_config.vm.provision "shell", path: "scripts/master.sh"
            else
                vm_config.vm.provision "shell", path: "scripts/worker.sh"
            end
        end
    end
end
