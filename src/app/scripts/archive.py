
from typing import Any, Optional
from .data import Playlist, Track


class DiscoverArchive(Playlist):
    
    def __init__(self, uid: str, name: str, tracks: list[Track], **kwargs) -> None:
        self.uid = uid
        

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
        self.spotify.user_playlist_add_tracks(
            self.user, self.discover.uid, self.discover
        )
