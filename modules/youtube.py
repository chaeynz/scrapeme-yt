# pylint: disable=missing-docstring, line-too-long
import sys

from pytube import YouTube
from pytube.exceptions import AgeRestrictedError

from modules.logger import log_error
from modules.trace import setup_tracer, INNERTUBE_CLIENT_NAME

def download_youtube(url, path, filename=None):
    yt:YouTube = None
    try:
        yt = YouTube(url=url, use_oauth=True, allow_oauth_cache=True)
        stream = yt.streams.filter(progressive=True).order_by('resolution').first()
        stream.download(output_path=path, filename=filename)
        return yt.video_id
    except AgeRestrictedError as e:
        setup_tracer()
        # Your function call that eventually calls `innertube.player`
        # This is an example. You would integrate your actual call here.
        _ = YouTube(url, use_oauth=True, allow_oauth_cache=True).vid_info
        sys.settrace(None)  # Stop tracing after the function call
        log_error(f"AgeRestrictedError: innertube is using client: {INNERTUBE_CLIENT_NAME} Error Message: {e}")
        raise AgeRestrictedError(e.video_id) from e
