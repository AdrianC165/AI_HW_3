#!/usr/bin/env bash

apt-get install -y gcc-10 gcc-10-base gcc-10-doc g++-10 libstdc++-10-dev libstdc++-10-doc 

apt-get install software-properties-common
add-apt-repository ppa:deadsnakes/ppa
apt-get update
# apt-get install python3.9
# python3.9 -m pip install pip
# pip3 install --upgrade pip

apt-get install -y python3.8 python3.8-dev python3.8-distutils python3.8-venv

python3.8 --version

python3.8 -m pip install -r /autograder/source/requirements.txt

g++ --version

# gcc -v --help 2> /dev/null | sed -n '/^ *-std=\([^<][^ ]\+\).*/ {s//\1/p}'

cd /autograder/source/

# g++ main.cpp -o a.out -std=c++17
# ./a.out

# apt-get -y install openjdk-11-jdk

java --version
javac --version

# javac Main.java
# java Main