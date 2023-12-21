#!/bin/bash

NC="\033[0m" # No Color
GREEN="\033[0;32m"
LIGHT_GREEN="\033[1;32m"

#----------
echo -e "${GREEN}Installs the python packages${NC}"
echo -e "${LIGHT_GREEN}$ python3 -m pip install -r requirements.txt${NC}"
python3 -m pip install -r requirements.txt
echo ""


