![workflow](https://github.com/addicteduser/dnd-hp-calc-discordbot/actions/workflows/ci.yml/badge.svg?branch=master)

# Valron the HP Calculator

![Valron the HP Calculator](https://i.imgur.com/0bByXQ4.png?s=200)

_Art by [Zentrend](https://www.instagram.com/neil_is_zen/)._

[![Discord Bots](https://top.gg/api/widget/666625461811413008.svg)](https://top.gg/bot/666625461811413008)

Discord Bot for computing your AL D&amp;D 5e character's hit points, given the Constitution modifier, its classes and levels, and other HP modifiers such as Tough feat or being a Hill Dwarf.

## Discord Server Invitation

Invite it to your Discord server with this [link](https://discordapp.com/api/oauth2/authorize?client_id=666625461811413008&permissions=11264&scope=bot).

## Usage

### Command

`?hp <con_modifier> <classA#/classB#/etc> [hp_mod1/hp_mod2/etc]`

#### Example

`?hp 3 fighter1/barb2/paladin1`

#### Example with HP modifiers

`?hp 3 fighter1/barb2/paladin1 tough/hilldwarf`

### Other commands

- `?help` - main help command
- `?options` - to see the list of supported classes and HP modifiers
- `?links` - to view some helpful links

## Dependencies

- [Python 3.7](https://docs.python.org/3.7/)
- [discord.py v1.6.0](https://discordpy.readthedocs.io/en/v1.6.0/), a modern, easy to use, feature-rich, and async ready API wrapper for Discord
- See `requirements.txt` for full list of dependencies
- For unit tests (see `test-requirements.txt`):
  - [pytest](https://docs.pytest.org/en/stable/) for running unit tests.
  - [pytest-asyncio](https://pypi.org/project/pytest-asyncio/) for testing asyncio code with pytest.

## Local Development

- Install dependencies with `pip install -r requirements.txt`
- Run with `python bot.py`
- Install unit test dependencies with `pip install -r test-requirements.txt`
- Run unit tests with `pytest`

## Dontation/Support

Hello, hello! This bot that I have made is just a little passion project of mine. Any support or donation ([PayPal](https://paypal.me/addicteduser) | [Ko-Fi](https://ko-fi.com/addicteduser) | [GCash](https://i.imgur.com/fnMORVa.jpg)) is much appreciated to keep up with the hosting fees. Thank you very much!

For feedback or suggestions, join the support discord server [here](https://discord.gg/waCBQuD).

<!--
CHEAT SHEET
- See if app is running: ps ax | grep bot.py
- End the app with: pkill -f bot.py
- Run app while saving logs: python3 -u bot.py > output.log &
-->
