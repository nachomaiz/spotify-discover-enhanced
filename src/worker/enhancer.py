from typing import Any

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import pandas as pd

from .data import Playlist

SCOPES = ["playlist-read-private", "playlist-modify-private"]

DW = "Discover Weekly"


class DiscoverEnhancer:
    """DiscoverEnhancer"""

    def __init__(self, archive_name: str = "Discover Weekly Archive") -> None:
        self.archive_name = archive_name
        self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth)
        self.user = self.get_user_id()
        self.playlists = self.get_playlists()
        self.discover = Playlist.from_response(
            self.spotify.playlist(self.playlists[DW])
        )

    def get_playlists(self) -> dict[str, str]:
        """Get current user's playlists.

        Returns
        -------
        dict[str, str]
            Dictionary of playlist names and id pairs.
        """
        res: dict[str, Any] = self.spotify.current_user_playlists()
        return {item["name"]: item["id"] for item in res["items"]}

    def get_user_id(self) -> str:
        """Get user's id."""
        return self.spotify.current_user()["id"]

    def summary(self) -> pd.DataFrame:
        """Return Discover Weekly summary."""
        return self.discover.summary()

    def audio_features(self) -> pd.DataFrame:
        """Return Discover Weekly audio features."""
        return self.discover.audio_features(self.spotify)

    def create_discover_archive(
        self, name: str = "Discover Weekly Archive"
    ) -> Playlist:
        """Create Discover Weekly archive.

        Parameters
        ----------
        name : str, optional
            Name for the archive, by default "Discover Weekly Archive"

        Returns
        -------
        Playlist
            Archive playlist after creation.
        """
        res: dict[str, Any]= self.spotify.user_playlist_create(self.user, name=name, public=False)
        return Playlist.from_response(res)
