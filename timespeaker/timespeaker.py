#!/usr/bin/env python3

import os
import sys
import time
from datetime import datetime

import click
from playsound import playsound

# Required python 3.6+
if sys.version_info[0] < 3 and sys.version_info[1] < 6:
    raise Exception("Python 3.6+ required, sorry")

# TODO: remove and get from pyproject.toml
__title__ = "TimeSpeaker"
__description__ = "Announce the time every hour similar to Mac OS X. Say the Time using Google TTS or espeak."
__url__ = "https://github.com/wallacesilva/timespeaker"
__version__ = "0.1.0"
__author__ = "Wallace Silva"
__author_email__ = "contact@wallacesilva.com"
__license__ = "MIT License"
__copyright__ = "Copyright 2020 Wallace Silva"

"""
CONSTANTS
"""


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


def start_loop(speaker: str, path_folder: str, debug: bool):
    last_hour_runned = None
    custom_minute = 0

    while True:

        time_now = time_now = datetime.now()

        if (
            time_now.minute == custom_minute
            and time_now.second == 0
            and last_hour_runned != time_now.hour
        ):
            hour = time_now.hour

            hour_speak = str(hour) + " hours" if hour > 1 else " hour"
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
            playsound(hour_file_abspath)

            last_hour_runned = time_now.hour

        # wait for next run
        seconds_to_next = (
            time_now.replace(hour=time_now.hour + 1, minute=custom_minute, second=0)
            - time_now
        )
        if custom_minute:
            seconds_to_next = time_now.replace(minute=custom_minute) - time_now
        seconds_wait = seconds_to_next.seconds - 1

        # print("Time Now: {time_now}".format(time_now=time_now))
        # print("Time Now Future: {custom_minute}".format(custom_minute=time_now.replace(minute=custom_minute)))
        # print("Custom Minute: {custom_minute}".format(custom_minute=custom_minute))

        if seconds_wait > 1:
            # TODO: change to logging
            if debug:
                click.echo(
                    "Waiting {seconds_wait} seconds for next run...".format(
                        seconds_wait=seconds_wait
                    )
                )
            time.sleep(seconds_wait)


"""
COMMANDS
"""


@click.group()
def cli():
    pass


@cli.command("start")
@click.option(
    "--speaker", type=click.Choice(["gtts", "pyspeaker"]), help="Choose speaker to use."
)
@click.option(
    "--path-folder",
    default="/tmp/timespeaker/",
    help="Choose to store hour files. \n\nDefault: /tmp/timespeaker/",
)
@click.option("--debug", is_flag=True)
def run_start(speaker, path_folder, debug):
    """
    Startup TimeSpeaker
    """
    return start_loop(speaker, path_folder, debug)


@cli.command()
@click.option("--version", is_flag=True)
def run_default(version):
    """
    Default command of TimeSpeaker
    """
    if version:
        click.echo(
            "{} version {} using python {}".format(__title__, __version__, sys.version)
        )
        return 0


@cli.command("check")
@click.argument(
    "speaker",
    type=click.Choice(["gtts", "pyspeaker"]),
)
def check_requirements(speaker):
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
        playsound(hour_file_tmp)
        click.echo(get_cli_txt_green("Works"))
    else:
        click.echo(get_cli_txt_red("Not works"))

    click.echo("Done")


if __name__ == "__main__":
    cli()
