#!/bin/bash

NC="\033[0m" # No Color
GREEN="\033[0;32m"
LIGHT_GREEN="\033[1;32m"

#----------
echo -e "${GREEN}Stops the bot${NC}"
echo -e "${LIGHT_GREEN}$ pkill -f bot.py${NC}"
pkill -f bot.py
echo ""
