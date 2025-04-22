import os

import click

from curses_playlist.controller import PlistController


@click.command
@click.option(
    "--playlist",
    "-p",
    help="specify location to write playlist to",
    default="curses_playlist.m3u",
)
@click.option(
    "--working-directory", "-w", help="Where to look for video files", default="."
)
@click.option("--gain", "-g", help="Volume gain for VLC start in [-64, 0]", default=0)
@click.option(
    "--clear-playlist", "-c", help="clear playlist", is_flag=True, default=False
)
def main(playlist: str, working_directory: str, gain: float, clear_playlist: bool):
    if working_directory != ".":
        os.chdir(working_directory)

    print(f"gain: {gain}")
    PlistController(playlist, gain, clear_playlist)


if __name__ == "__main__":
    main()
