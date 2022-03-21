# pylint: disable = missing-class-docstring
# pylint: disable = missing-function-docstring


from typing import Any
import unittest
import unittest.mock

import json

from app.models import Playlist, Track

with open("samples/track.json", encoding="utf-8") as f:
    sample_track: dict[str, Any] = json.load(f)

with open("samples/playlist.json", encoding="utf-8") as f:
    sample_playlist: dict[str, Any] = json.load(f)


class TestTrackInit(unittest.TestCase):
    def test_from_response(self):
        self.assertIsInstance(Track.from_response(sample_track), Track)

    def test_from_client(self):
        with unittest.mock.patch("spotipy.client.Spotify") as mock_Spotify:
            instance = mock_Spotify.return_value
            instance.track.return_value = sample_track
            track = Track.from_client(sample_track["id"], mock_Spotify)
            mock_Spotify.track.assert_called_once_with(sample_track["id"])
            self.assertIsInstance(track, Track)


class TestTrackProperties(unittest.TestCase):
    def setUp(self):
        self.track = Track.from_response(sample_track)

    def test_uri(self):
        self.assertEqual(self.track.uri, f"spotify:track:{self.track.uid}")

    def test_artists(self):
        self.assertEqual(self.track.artists, "Maxxi Soundsystem, Name One")

    def test_album(self):
        self.assertEqual(self.track.album, "Medicine EP")

    def test_duration(self):
        self.assertEqual(self.track.duration, 417)


class TestPlaylistInit(unittest.TestCase):
    def test_from_response(self):
        self.assertIsInstance(Playlist.from_response(sample_playlist), Playlist)

    def test_from_client(self):
        with unittest.mock.patch("spotipy.client.Spotify") as mock_Spotify:
            instance = mock_Spotify.return_value
            instance.playlist.return_value = sample_playlist
            playlist = Playlist.from_client(sample_playlist["id"], mock_Spotify)
            mock_Spotify.playlist.assert_called_once_with(sample_playlist["id"])
            self.assertIsInstance(playlist, Playlist)


class TestPlaylistProperties(unittest.TestCase):
    def setUp(self):
        self.playlist = Playlist.from_response(sample_playlist)

    def test_track_uri(self):
        self.assertEqual(
            self.playlist.track_uris[0], f"spotify:track:{self.playlist.track_uids[0]}"
        )

    def test_track_artists(self):
        self.assertEqual(self.playlist.track_artists[0], "Maxxi Soundsystem, Name One")

    def test_track_album(self):
        self.assertEqual(self.playlist.track_albums[0], "Medicine EP")

    def test_track_duration(self):
        self.assertEqual(self.playlist.track_duration[0], 417)


if __name__ == "__main__":
    unittest.main()
