# Changelog

## 0.1.6

- Raise error when period to validate is invalid
- Add Tests to validate_period

## 0.1.5

- Fix when run at midnight (0 hour)

## 0.1.4

- Fix speaker to hour 0 (midnight) and 1 hour (1am)
- Add function to test/check speaker of hours sound
- Update README.md with new command to check speaker

## 0.1.3

- Improve Makefile
- Update README.md
- Fix `pip install timespeaker`

## 0.1.2

- Add envvars to PERIOD and DEBUG
- Add `make run-default` to Makefile for simple to run locally
- Add minutes to the speaker 
- Remove `timedelta`, no more used import
- Update commands of Makefile to use poetry 
- Update dependencies
- Add `.vscode` to .gitignore 
- Add configurations to `black` on pyproject
- Add package configurations to `pyproject.toml`
- Add pytest to dev dependencies
- Update `README.md` 

## 0.1.1

- Remove playsound from dependencies;
- Add pyttsx3 to dependencies;
- Add support to run on local player (mpv, vlc, aplay,...);
- Fix autocreate foldert to save audio from hours;
- Updated Makefile to future support to Cron
- Changed period validation;
- Files moved to home project, before in `timespeaker/`;

## 0.1.0

* Initial release
