from __future__ import annotations
from typing import Any, Literal, Optional

import spotipy as sp
import pandas as pd


class Track:
    """Track object."""

    def __init__(self, uid: str, name: str, **kwargs) -> None:
        self.uid = uid
        self.name = name
        self.info = kwargs

    @classmethod
    def from_response(cls, response: dict[str, Any]) -> Track:
        """Create Playlist from `spotipy.Spotify().track` response."""
        res = {} | response
        uid = res.pop("id")
        name = res.pop("name")
        return cls(uid, name, **res)

    @classmethod
    def from_client(cls, uid: str, spotify: sp.Spotify) -> Track:
        """Create Track by calling `.track()` from client."""
        res: dict[str, Any] = spotify.track(uid)
        return cls.from_response(res)

    @property
    def uri(self) -> str:
        """Spotify URI."""
        return f"spotify:track:{self.uid}"

    @property
    def artists(self) -> str:
        """Artist names."""
        return ", ".join([artist["name"] for artist in self.info["artists"]])

    @property
    def album(self) -> str:
        """Album name."""
        return self.info["album"]["name"]

    @property
    def duration(self) -> int:
        """Duration in seconds."""
        return self.info["duration_ms"] // 1000


class Playlist:
    """Playlist object."""

    def __init__(self, uid: str, name: str, tracks: list[Track], **kwargs) -> None:
        self.uid = uid
        self.name = name
        self.tracks = tracks
        self.info = kwargs

    @classmethod
    def from_response(cls, response: dict[str, Any]) -> Playlist:
        """Create Playlist from `spotipy.Spotify().playlist` response."""
        res = {} | response
        uid = res.pop("id")
        tracks = [
            Track.from_response(item["track"] | {"added_at":item["added_at"]}) for item in res.pop("tracks")["items"]
        ]
        name = res.pop("name")
        return cls(uid, name, tracks, **res)

    @classmethod
    def from_client(cls, uid: str, spotify: sp.Spotify) -> Playlist:
        """Create Playlist by calling `.track()` from client."""
        res: dict[str, Any] = spotify.playlist(uid)
        return cls.from_response(res)

    def get_cover_url(self, size: Literal[60, 300, 640]) -> str:
        """Get Spotify cover URL."""
        pos = {
            640: 0,
            300: 1,
            60: 2,
        }

        return self.info["images"][pos[size]]["url"]

    @property
    def track_uids(self) -> list[str]:
        """Track ids for tracks in playlist."""
        return [track.uid for track in self.tracks]

    @property
    def track_names(self) -> list[str]:
        """Track names for tracks in playlist."""
        return [track.name for track in self.tracks]

    @property
    def track_uris(self) -> list[str]:
        """Track uris for tracks in playlist."""
        return [track.uri for track in self.tracks]

    @property
    def track_artists(self) -> list[str]:
        """Track artists for tracks in playlist."""
        return [track.artists for track in self.tracks]

    @property
    def track_albums(self) -> list[str]:
        """Track albums for tracks in playlist."""
        return [track.info["album"]["name"] for track in self.tracks]

    @property
    def track_duration(self) -> list[int]:
        """Track albums for tracks in playlist."""
        return [track.duration for track in self.tracks]

    @property
    def track_cover_urls(self) -> list[str]:
        """Track album cover URLs for tracks in playlist."""
        return [track.info["album"]["images"][2]["url"] for track in self.tracks]
    
    @property
    def track_date_added(self) -> list[str]:
        """Track date added to playlist."""
        return [track.info["added_at"] for track in self.tracks]

    def summary(self) -> pd.DataFrame:
        """Summary Dataframe for playlist.

        Returns
        -------
        pd.DataFrame
            DataFrame with name, artists, album and duration information.
        """
        return pd.DataFrame(
            [
                self.track_cover_urls,
                self.track_names,
                self.track_artists,
                self.track_albums,
                self.track_date_added,
                self.track_duration,
            ],
        ).T.rename(
            index=dict(enumerate(self.track_uids)),
            columns=dict(enumerate(["Cover", "Name", "Artists", "Album", "Date added", "Duration"])),
        )

    def audio_features(self, spotify: sp.Spotify) -> pd.DataFrame:
        """Fetch audio features from Spotify and return as DataFrame.

        Parameters
        ----------
        spotify : spotipy.Spotify
            spotipy client instance.

        Returns
        -------
        pd.DataFrame
            DataFrame with audio features.
        """
        res = pd.DataFrame(spotify.audio_features(self.track_uids)).set_index("id")
        cols = [
            "danceability",
            "energy",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "key",
            "loudness",
            "valence",
            "tempo",
        ]
        return res.loc[:, cols]


class DiscoverWeekly(Playlist):
    """Discover Weekly Playlist."""

    def __init__(self, *args, user: str, spotify: sp.Spotify, **kwargs) -> None:
        self.user = user
        self.spotify = spotify
        super().__init__(*args, **kwargs)

    def create_discover_archive(
        self, public: bool = False, collaborative: bool = False
    ) -> Optional[dict[str, Any]]:
        """Create Discover Weekly archive playlist.

        Parameters
        ----------
        public : bool, optional
            Is the created playlist public, by default False
        collaborative : bool, optional
            Is the created playlist collaborative, by default False
        """
        return self.spotify.user_playlist_create(
            self.user,
            "Discover Weekly Archive",
            public=public,
            collaborative=collaborative,
            description="Discover Weekly Archive Description",
        )

    def update_discover_archive(self) -> None:
        """Update Discover Weekly archive playlist."""
        self.spotify.user_playlist_add_tracks(self.user, self.uid, self.track_uids)
