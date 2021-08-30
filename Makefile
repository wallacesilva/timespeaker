DEFAULT_COMMAND = 'python -m timespeaker start'
CUSTOM_COMMAND = 'python -m timespeaker start --speaker=pyttsx3 --player=mpv --path-folder=/tmp/timespeaker/'
CUSTOM_COMMAND_GTTS_VLC = 'python -m timespeaker start --speaker=gtts --player=vlc --path-folder=/tmp/timespeaker/'

.PHONY: clean-pyc clean-build clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "release - package and upload a release"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.swp' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -f .coverage

build:
	poetry build

install:
	poetry install
	@echo "\e[0;92mIstall finished\e[0m"

run-default:
	poetry run timespeaker start --speaker=gtts --player=mpv

configure-systemd:
	sudo pip3 install timespeaker
	cp resources/systemd-timespeaker.service /lib/systemd/system/timespeaker.service
	systemctl enable timespeaker.service
	systemctl start timespeaker.service

configure-autostart:
	cp resources/timespeaker.desktop ~/.config/autostart/timespeaker.desktop

configure-cron:
	echo "Future configure to cron"

configure-i3:
	echo "# Startup TimeSpeaker (autogenerated)" >> ~/.i3/config
	echo "$(CUSTOM_COMMAND)" >> ~/.i3/config

remove-systemd:
	systemctl stop timespeaker.service
	systemctl disable timespeaker.service
	@rm -f /lib/systemd/system/timespeaker.service

remove-autostart:
	@rm -f ~/.config/autostart/timespeaker.desktop

remove-cron:
	echo "Future remove configs to cron"

test:
	poetry run pytest -sx

lint:
	poetry run black .
	@echo "\e[0;92mLinter (black) finished\e[0m"

release:
	poetry build
	poetry publish