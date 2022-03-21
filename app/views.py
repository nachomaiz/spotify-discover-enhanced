import pandas as pd


def render_playlist(summary: pd.DataFrame) -> str:
    """Render Spotify Playlist in HTML from Playlist summary."""
    
    table = summary.copy()

    # Convert Duration into seconds.
    table["Duration"] = table["Duration"].apply(seconds_to_mm_ss)

    # Album Cover
    table["Cover"] = table["Cover"].apply(
        html_img_url, args=(60, 60), loading="lazy"
    )

    # Generate combined Track Column
    table["Track"] = table["Name"] + "<br/>" + table["Artists"]
    table = table.loc[:, ["Cover", "Track", "Album", "Duration"]]

    # Set numerical index before rendering
    table = table.reset_index(drop=True)
    table.index += 1

    return table.style.format({}).to_html(
        border=0, table_attributes='class="playlist"'
    )


def html_img_url(url: str, width: int, height: int, **kwargs: dict) -> str:
    """Convert an image URL to HTML."""
    html_kwargs = "".join([f'{k}="{v}" ' for k, v in kwargs.items()])
    return f'<img src="{url}" width="{width}" height="{height}" {html_kwargs}></img>'


def seconds_to_mm_ss(seconds: int) -> str:
    """Convert seconds to minutes and seconds in mm:ss format."""
    return pd.to_datetime(seconds, unit="s").strftime("%M:%S")
