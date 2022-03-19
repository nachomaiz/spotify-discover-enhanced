import pandas as pd

import spotipy

from .data import Playlist


def render_playlist(playlist: Playlist) -> tuple[str, str]:
    """Render Spotify Playlist"""
    table = playlist.summary()

    total_duration = pd.to_datetime(table["Duration"].sum(), unit='s').strftime("%M:%S")

    # Convert Duration into seconds.
    table["Duration"] = pd.to_datetime(table["Duration"], unit="s")

    # Album Cover
    table["Cover"] = table["Cover"].apply(html_img_url, args=(64, 64))

    # Generate combined Track Column
    table["Track"] = table["Name"] + "<br/>" + table["Artists"]
    table = table.loc[:, ["Cover", "Track", "Album", "Duration"]]

    # Set numerical index before rendering
    table = table.reset_index(drop=True)
    table.index += 1

    styled_table = table.style.format({"Duration": lambda s: s.strftime("%M:%S")})

    return styled_table.to_html(border=0), total_duration


def html_img_url(url: str, width: int, height: int) -> str:
    """Convert an image URL to HTML."""
    return f'<img src="{url}" width="{width}" height="{height}"></img>'
