#!/bin/bash

NC="\033[0m" # No Color
GREEN="\033[0;32m"
LIGHT_GREEN="\033[1;32m"

#----------
echo -e "${GREEN}Installs the python packages${NC}"
echo -e "${LIGHT_GREEN}$ pip3 install -r requirements.txt${NC}"
pip3 install -r requirements.txt
echo ""


