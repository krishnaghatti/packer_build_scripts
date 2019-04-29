#!/bin/bash -x

main() {
  # random wait for the system services to start
  sleep 60
  # disabling auto update of package cache
  function wait_for_apt_lock() {
      while [ "" = "" ]; do
          eval "$1" 2>/dev/null
          if [ $? -eq 0 ]; then
              break
          fi
          sleep 10
          echo "Waiting for apt lock to be released..."
      done
  }
  wait_for_apt_lock "sudo apt update"
  sudo apt upgrade

  # adding ansible repo
  sudo apt-add-repository --yes --update ppa:ansible/ansible

  # list of system packages to be installed. please add any new packages that need to be installed to the variable "packages_to_install"
  packages_to_install=( vim htop sysstat atop software-properties-common ansible python-apt locales locales-all )

  for package in "${packages_to_install[@]}"
  do
    sudo apt install -y $package
  done 

  locale-gen --purge en_US.UTF-8
  echo -e 'LANG="en_US.UTF-8"\nLANGUAGE="en_US:en"\n' > /etc/default/locale

  # adding the ssh publick key for ansible
  mkdir -p /home/ubuntu/.ssh && echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDZVkJu83Z5Ln2gXsHXAoDCr7mDAyRIFzqSdwl6Vari0EfnHAn1JCgXI6Udehwx2bzFYUdysXyZ98QVtvm8TfUb3NmrpCNQ1DFxP42DvgpqpzILs1c0RZZI5d3JG0ihFHiR88YychZ2sVXSX4izuzjqf2mA8ePOyxkVlCaYh+F2s2/tPmhxeFa6CxpwMrZDduVftGatW2XMZ7OSAndPqEe6s8+AEQ41OWn6Rn82H3dNvcoU0zMYNWLn2ejdkYpJZN9d29pDChB+TcvCwVeabZiWbEtQdzGYsjJ3uS3+5BvovFyJ/7q6QRT9eFs4U2UoFtKnIYTKz/7ShnpZjPjJvCK1vwa1+8TwoxVOwcYsIl2B2oEbUYdr2iQ/XMKvpuWOkOtMB6RW/3ofc4bzBOAf/kosYEMX48jn8mX7jngSDCp/4ASuPqiueYMnZMOExVxMjKsgCEMcrWaHFaOJaMrRwW+43dohARBCb6uECgKo6/kJUSlJwRy+0Mjr1jeDJiEmD4cSk/ho2h+XiH9KTJKVsq7AF80uMVDw3a47NAdxTKRsh586cRX/lp3VUyPQi92oxt6oap/ULjwa9w60EpNex45a9YMJBg5xuDX3Z6i3UzXe1vVCQDoLJ9zftd+3q2gatuV2rrOg4w/upeVZsjhgc4u8UzIkTSK91D94rOV7/V48iw== root@ip-10-200-1-173" >> ~/.ssh/authorized_keys
 
  ansible-galaxy install -r /tmp/cis_hardening/roles/requirements.yml
  ansible-playbook -l localhost /tmp/cis_hardening/tasks/main.yml
  ## DO NOT MAKE ANY CHANGES BEYOND THIS 
  # random wait for the system services to start
  sudo apt remove ansible -y && sudo apt autoremove -y
}

main
