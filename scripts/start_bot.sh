#!/bin/bash

NC="\033[0m" # No Color
GREEN="\033[0;32m"
LIGHT_GREEN="\033[1;32m"

#----------
echo -e "${GREEN}Starts the bot (saves the logs in 'output.log')${NC}"
echo -e "${LIGHT_GREEN}$ python3.8 -u bot.py > output.log &${NC}"
python3.8 -u bot.py > output.log &
echo ""

