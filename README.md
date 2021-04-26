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

```
pip install timespeaker
```

## Local

```bash
# pyenv shell +3.6.0
python -m venv .venv 
make install
```

# Configure

## AutoStart (Working In Progress)

```
make configure-autostart
```

## i3 (Working In Progress)

```
make configure-i3
```

## Cron (Working In Progress)

Coming Soon

```
sudo make configure-cron
```

## Systemd (Working In Progress)

```
sudo make configure-systemd
```

## Remove configurations

```
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
```
python -m timespeaker start

# OR if configured

timespeaker start
```

Custom command:
```
python -m timespeaker start --speaker=pyttsx3 --path-folder=/tmp/timespeaker/
```

# Development

Using virtualenv:

```
# create virtualenv
# virtualenv .venv [-p /path/to/python3.6+] # require virtualenv
python -m venv .venv

# Enter virtualenv
source .venv/bin/activate

# to exit of virtual env run 
deactivate
```

Dev install (poetry required)
```
poetry install
```

See more commands with
```
make help
```

# Tests

```
make tests 
```

# License

MIT LICENSE

# Contributing

I encourage you to contribute to this project! Join us!

Trying to report a possible security vulnerability? [Open a issue now](https://github.com/wallacesilva/timespeaker/issues/new)

Everyone interacting in this project and its sub-projects' codebases, issue trackers, chat rooms, and mailing lists is expected to follow the code of conduct (building, but respect everyone).
