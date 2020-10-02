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

- Update/Fix to PyPi (`pip install timespeaker`)
- Move Makefile to Parent
- Configure PULL_REQUESTS AND ISSUES template
- Create tests
- Configure lint
- Configure github actions (or circleci)
- Test i3 configs
- When merge to `main` build and publish to PyPi (github actions)
- Create a simples page documentation (readthedocs.org or github wiki)

# Install

## Default

```
pip install timespeaker
```

## Local

```
virtualenv .venv 
make install
```

# Configure

## AutoStart

```
make configure-autostart
```

## i3

```
make configure-i3
```

## Systemd

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
python -m timespeaker start --speaker=pyspeaker --path-folder=/tmp/timespeaker/
```

# Development

Using virtualenv:

```
# create virtualenv
virtualenv .venv [-p /path/to/python3.6+]

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
