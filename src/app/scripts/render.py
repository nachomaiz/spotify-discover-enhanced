import pandas as pd

import spotipy

from .data import Playlist

def render_playlist(playlist: Playlist) -> str:
    """Render Spotify Playlist"""
    table = playlist.summary()
    
    # Convert Duration into seconds.
    table["Duration"] = pd.to_datetime(table["Duration"], unit='s')
    
    # Album Cover
    # Get from Spotify
    # try:
    #     album_covers = get_album_covers(album_ids)
    # except 
    # table["Album Cover"] = album_covers
    
    # Set numerical index before rendering
    table = table.reset_index(drop=True)
    table.index += 1
    
    styled_table = table.style.format({"Duration": lambda s: s.strftime("%M:%S")})
    
    return styled_table.to_html(border=0)
