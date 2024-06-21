#!/bin/bash

echo "[*] Fetching instructions.xml"
wget https://uops.info/instructions.xml

echo "[*] Updating gcc and nasm"
sudo apt-get upgrade gcc nasm

echo "[*] Installing msr module"
sudo modprobe msr

echo "[*] Listing available Instruction Set Extensions"
echo "[*] Vector Extensions"
lscpu | tr ' ' '\n' | grep avx

echo "[*] SIMD Extensions"
lscpu | tr ' ' '\n' | grep sse

echo "[*] FMA Extensions"
lscpu | tr ' ' '\n' | grep fma

echo "[*] AES Extensions"
lscpu | tr ' ' '\n' | grep aes

echo "[*] BMI Extensions"
lscpu | tr ' ' '\n' | grep bmi

echo "[*] CET Extension"
lscpu | tr ' ' '\n' | grep cet

echo "[*] XSAVE Extensions"
lscpu | tr ' ' '\n' | grep xsave
