# TimeSpeaker

Announce the time every hour similar to Mac OS X. Say the Time using Google TTS or espeak.

# Requirements

- python3.6+
- playsound
- gtts or pyttsx3

For development

- poetry 
- flake8
- black
- pytest

# TODO

- Use python: [threading.Timer](https://docs.python.org/3/library/threading.html?highlight=timer#threading.Timer)
- Create tests
- Add system tray (opcional) by cli
- Update/Fix to PyPi (`pip install timespeaker`)
- Move Makefile to Parent
- Configure PULL_REQUESTS AND ISSUES template
- Configure lint
- Configure github actions (or circleci)
- Test i3 configs
- Add support to Cron
- Use a global DEBUG
- When merge to `main` build and publish to PyPi (github actions)

# Install

## Default (Working In Progress)

```bash
pip install timespeaker
```

## Local

### On Local User

```bash
# pyenv shell +3.6.0
# asdf shell python +3.6.0

# optional (poetry create a virtualenv for you)
python -m venv .venv 

# install dependencies
make install

# clean old builds
make clean

# build package
make build

# install on local user package (python)
pip install --user dist/{path_from_last_command}.whl
```

**Test local install**
```bash
timespeaker check --speaker gtts
```

# Configure

## AutoStart (Working In Progress)

```bash
make configure-autostart
```

## i3 (Working In Progress)

```bash
make configure-i3
```

## Cron (Working In Progress)

Coming Soon

```bash
sudo make configure-cron
```

## Systemd (Working In Progress)

```bash
sudo make configure-systemd
```

## Remove configurations

```bash
# Systemd
sudo make remove-systemd

# Autostart
make remove-autostart

# i3
# coming soon

# Cron
# coming soon
```

# Usage

Default usage using gtts to speak and saving in `/tmp/timespeaker/`

```bash
# after make install (or poetry install)
poetry run timespeaker start

# OR if configured (local user or via pip install timespeaker)
timespeaker start
```

Custom command:

```bash
poetry run timespeaker start --speaker=pyttsx3 --player=vlc --path-folder=/tmp/timespeaker/
```

## How to check sounds

This speakes sound each 2 second from **midnight** to **23 hours**.

```bash
poetry run timespeaker check-hours-sound gtts
```

# Development

Using virtualenv (python venv):

```bash
# create virtualenv
# virtualenv .venv [-p /path/to/python3.6+] # require virtualenv
python -m venv .venv

# Enter virtualenv
source .venv/bin/activate

# to exit of virtual env run 
deactivate
```

Dev install (poetry required)

```bash
poetry install
```

See more commands with

```bash
make help
```

# Tests

```bash
make test
```

# License

MIT LICENSE

# Contributing

I encourage you to contribute to this project! Join us!

Trying to report a possible security vulnerability? [Open a issue now](https://github.com/wallacesilva/timespeaker/issues/new)

Everyone interacting in this project and its sub-projects' codebases, issue trackers, chat rooms, and mailing lists is expected to follow the code of conduct (building, but respect everyone).
