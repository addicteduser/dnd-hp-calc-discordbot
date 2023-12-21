#!/bin/bash

NC="\033[0m" # No Color
GREEN="\033[0;32m"
LIGHT_GREEN="\033[1;32m"

#----------
echo -e "${GREEN}Check if the bot is running${NC}"
echo -e "${LIGHT_GREEN}$ ps ax | grep bot.py${NC}"
ps ax | grep bot.py
echo ""

