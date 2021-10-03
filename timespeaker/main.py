#!/usr/bin/env python3

import os
import sys
import time
from datetime import datetime
from pathlib import Path

import click

# Required python 3.6+
if sys.version_info[0] < 3 and sys.version_info[1] < 6:
    raise Exception("Python 3.6+ required, sorry")

# TODO: remove and get from pyproject.toml
__title__ = "TimeSpeaker"
__description__ = "Announce the time every hour similar to Mac OS X. Say the Time using Google TTS or espeak."
__url__ = "https://github.com/wallacesilva/timespeaker"
__version__ = "0.1.3"
__author__ = "Wallace Silva"
__author_email__ = "contact@wallacesilva.com"
__license__ = "MIT License"
__copyright__ = "Copyright 2020-2021 Wallace Silva"

"""
CONSTANTS
"""
PERIOD_ALLOWED = ("hour", "halfhour", "5_min")
TIMESPEAKER_DEBUG = os.getenv("TIMESPEAKER_DEBUG", default=False)
TIMESPEAKER_PERIOD = os.getenv("TIMESPEAKER_PERIOD", default="hour")

if TIMESPEAKER_PERIOD not in PERIOD_ALLOWED:
    TIMESPEAKER_PERIOD = "hour"

if TIMESPEAKER_DEBUG is not False:
    boolean_default_values = {
        "1": True,
        "true": True,
        "yes": True,
        "y": True,
        "on": True,
        "t": True,
        "0": False,
        "false": False,
        "no": False,
        "n": False,
        "off": False,
        "f": False,
    }
    try:
        TIMESPEAKER_DEBUG = boolean_default_values[TIMESPEAKER_DEBUG]
    except KeyError:
        TIMESPEAKER_DEBUG = False


class BgColors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


"""
EXCEPTIONS
"""


class SpeakerSaveNotValidError(Exception):
    pass


class SpeakerSaveGttsNotSavedError(Exception):
    pass


class SpeakerSavePytts3NotSavedError(Exception):
    pass


"""
FUNCTIONS
"""


def get_cli_txt_red(msg):
    return "{}{}{}".format(BgColors.FAIL, msg, BgColors.ENDC)


def get_cli_txt_green(msg):
    return "{}{}{}".format(BgColors.OKGREEN, msg, BgColors.ENDC)


def get_cli_txt_blue(msg):
    return "{}{}{}".format(BgColors.OKBLUE, msg, BgColors.ENDC)


def print_warn(msg):
    click.echo(get_cli_txt_red(msg))


def print_info(msg):
    click.echo(get_cli_txt_blue(msg))


def print_success(msg):
    click.echo(get_cli_txt_green(msg))


def play_sound(hour_file: str, player: str):
    os.system("{} {}".format(player, hour_file))


def speaker_save(speaker: str, hour_speak: str, file, debug: bool = False):
    if speaker not in ["gtts", "pyttsx3"]:
        # TODO: change to logging
        if debug:
            click.echo("Speaker {} not supported.".format(speaker))
        raise SpeakerSaveNotValidError

    if speaker == "gtts":
        try:
            from gtts import gTTS

            tts = gTTS(hour_speak)
            tts.save(file)
            # TODO: change to logging
            if debug:
                click.echo("gtts saved in {}".format(file))
            return True
        except Exception as exc:
            # TODO: change to logging
            if debug:
                print_warn("gtts error on save. Details: {}".format(str(exc)))
            raise SpeakerSaveGttsNotSavedError
    elif speaker == "pyttsx3":
        try:
            import pyttsx3

            engine = pyttsx3.init()
            # On linux make sure that 'espeak' and 'ffmpeg' are installed
            engine.save_to_file(hour_speak, file)
            # engine.say("I will speak this text")
            engine.runAndWait()
            # TODO: change to logging
            if debug:
                click.echo("pyttsx3 saved in {}".format(file))
            return True
        except Exception as exc:
            # TODO: change to logging
            if debug:
                print_warn("pyttsx3 error on save. Details: {}".format(str(exc)))
            raise SpeakerSavePytts3NotSavedError

    return False


def validate_period(name: str, time_now: datetime, last_time_run: datetime, debug=False):
    rules = {
        "hour": time_now.minute == 0 and time_now.second == 0 and last_time_run.hour != time_now.hour,
        "halfhour": time_now.minute in (0, 30) and time_now.second == 0,  # future
        "5_min": (time_now.minute % 5 == 0) and time_now.second == 0,  # for debug
    }

    if debug:
        print("Rule: {} | Rules: {} | Time: {}".format(name, rules, time_now))

    if name in rules:
        return rules[name]


def start_loop(speaker: str, player: str, path_folder: str, debug: bool):
    hour_replace = datetime.now().hour - 1
    minute_replace = datetime.now().minute
    if hour_replace < 1:
        hour_replace = 0
        minute_replace = 0
    last_time_run = datetime.now().replace(hour=hour_replace, minute=minute_replace)
    Path(path_folder).mkdir(mode=0o755, parents=True, exist_ok=True)

    while True:

        time_now = time_now = datetime.now()

        if validate_period(
            name=TIMESPEAKER_PERIOD, time_now=time_now, last_time_run=last_time_run, debug=debug
        ):
            hour = time_now.hour
            minute = time_now.minute

            if hour == 0:
                hour_speak = "midnight"
            elif hour == 1:
                hour_speak = "one hour"
            else:
                hour_speak = str(hour) + " hours"

            if minute > 0:
                hour_speak = hour_speak + " and " + str(minute) + " minutes"
            hour_file = hour_speak.replace(" ", "_") + ".mp3"
            hour_file_abspath = os.path.join(path_folder, hour_file)

            if not os.path.exists(hour_file_abspath):
                # TODO: change to logging
                if debug:
                    click.echo("Creating file {}".format(hour_file_abspath))
                speaker_save(speaker, hour_speak, hour_file_abspath, debug=debug)

            # TODO: change to logging
            if debug:
                click.echo("Playing audio file {}".format(hour_file_abspath))
            play_sound(hour_file_abspath, player)

            last_time_run = time_now

        # TODO: Abstract to a function
        # wait for next run
        # seconds_to_next = (
        #     time_now.replace(hour=time_now.hour + 1, minute=minute_check, second=0)
        #     - time_now
        # )
        # if minute_check:
        #     seconds_to_next = time_now.replace(minute=minute_check) - time_now
        # seconds_wait = seconds_to_next.seconds - 1

        # # print("Time Now: {time_now}".format(time_now=time_now))
        # # print("Time Now Future: {minute_check}".format(minute_check=time_now.replace(minute=minute_check)))
        # # print("Custom Minute: {minute_check}".format(minute_check=minute_check))

        # if seconds_wait > 1:
        #     # TODO: change to logging
        #     if debug:
        #         click.echo(
        #             "Waiting {seconds_wait} seconds for next run...".format(
        #                 seconds_wait=seconds_wait
        #             )
        #         )
        #     time.sleep(seconds_wait)
        time.sleep(1)


"""
COMMANDS
"""


@click.group()
def cli():
    pass


@cli.command("start")
@click.option(
    "--speaker",
    default="pyttsx3",
    type=click.Choice(["gtts", "pyttsx3"]),
    help="Choose speaker to use.",
)
@click.option("--player", default="mpv", help="Choose player command. Eg. mpv, vlc")
@click.option(
    "--path-folder",
    default="/tmp/timespeaker/",
    help="Choose to store hour files. \n\nDefault: /tmp/timespeaker/",
)
@click.option("--debug", is_flag=True)
def run_start(speaker, player, path_folder, debug):
    """
    Startup TimeSpeaker
    """
    # TODO: Define global DEBUG
    if debug:
        print("Started at ", datetime.now())
    return start_loop(speaker, player, path_folder, debug)


@cli.command()
@click.option("--version", is_flag=True)
def run_default(version):
    """
    Default command of TimeSpeaker
    """
    if version:
        click.echo("{} version {} using python {}".format(__title__, __version__, sys.version))
        return 0


@cli.command("check")
@click.argument(
    "speaker",
    type=click.Choice(["gtts", "pyttsx3"]),
)
@click.option("--player", default="mpv", help="Choose player command. Eg. mpv, vlc")
def check_requirements(speaker, player):
    """
    Check requirements to use TimeSpeaker
    """
    hour_file_tmp = "/tmp/15_hours.mp3"
    speaker_works = False

    try:
        speaker_works = speaker_save(speaker, "15 hours", hour_file_tmp)
    except Exception as exc:
        click.echo(get_cli_txt_green("Error: ") + str(exc))
        click.echo("Try install python -m pip install {}".format(speaker))

    if speaker_works:
        play_sound(hour_file_tmp, player)
        click.echo(get_cli_txt_green("Works"))
    else:
        click.echo(get_cli_txt_red("Not works"))

    click.echo("Done")


@cli.command("check-hours-sound")
@click.argument(
    "speaker",
    type=click.Choice(["gtts", "pyttsx3"]),
)
@click.option("--player", default="mpv", help="Choose player command. Eg. mpv, vlc")
def check_hours_sound(speaker, player):
    """
    Check hours sound to TimeSpeaker
    """
    path_folder = "/tmp/timespeaker/"
    debug = True

    for hour in range(0, 24):

        if hour == 0:
            hour_speak = "midnight"
        elif hour == 1:
            hour_speak = "one hour"
        else:
            hour_speak = str(hour) + " hours"

        hour_file = hour_speak.replace(" ", "_") + ".mp3"
        hour_file_abspath = os.path.join(path_folder, hour_file)

        if not os.path.exists(hour_file_abspath):
            # TODO: change to logging
            if debug:
                click.echo("Creating file {}".format(hour_file_abspath))
            speaker_save(speaker, hour_speak, hour_file_abspath, debug=debug)

        click.echo("Playing file {} with text {}".format(hour_file_abspath, hour_speak))
        play_sound(hour_file_abspath, player)

        time.sleep(2)

    click.echo("Done")
