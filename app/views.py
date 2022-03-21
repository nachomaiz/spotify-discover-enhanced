import pandas as pd


def render_playlist(summary: pd.DataFrame) -> str:
    """Render Spotify Playlist in HTML from Playlist summary."""

    # Convert Duration into seconds.
    summary["Duration"] = summary["Duration"].apply(seconds_to_mm_ss)

    # Album Cover
    summary["Cover"] = summary["Cover"].apply(
        html_img_url, args=(60, 60), loading="lazy"
    )

    # Generate combined Track Column
    summary["Track"] = summary["Name"] + "<br/>" + summary["Artists"]
    summary = summary.loc[:, ["Cover", "Track", "Album", "Duration"]]

    # Set numerical index before rendering
    summary = summary.reset_index(drop=True)
    summary.index += 1

    return summary.style.format({}).to_html(
        border=0, table_attributes='class="playlist"'
    )


def html_img_url(url: str, width: int, height: int, **kwargs: dict) -> str:
    """Convert an image URL to HTML."""
    html_kwargs = "".join([f'{k}="{v}" ' for k, v in kwargs.items()])
    return f'<img src="{url}" width="{width}" height="{height}" {html_kwargs}></img>'


def seconds_to_mm_ss(seconds: int) -> str:
    """Convert seconds to minutes and seconds in mm:ss format."""
    return pd.to_datetime(seconds, unit="s").strftime("%M:%S")
