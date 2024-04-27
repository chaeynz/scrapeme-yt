# pylint: disable=missing-docstring, line-too-long
from flask import Flask, request, jsonify, send_file, Response
from pytube.exceptions import AgeRestrictedError, PytubeError, RegexMatchError

from modules.youtube import download_youtube
from modules.videos import Videos, ALLOWED_FILE_FORMATS, DOWNLOAD_PATH
from modules.logger import log_error, log_debug

app = Flask(__name__)

videos = Videos()

def handle_download(video_id, file_format) -> Response: 
    try:
        download_youtube(url=f'/{video_id}', path=DOWNLOAD_PATH, filename=f'{video_id}.{file_format}')
    except RegexMatchError as e:
        log_error(f"RegexMatchError: User supplied: \"{video_id}\" Error Message: {e}")
        return jsonify({'status': '400', 'error': 'Bad Request', 'message': 'You supplied a malformed video_id'}), 400
    except AgeRestrictedError as e:
        log_error(f"AgeRestrictedError: {e}")
        return jsonify({'status': '500', 'error': 'Internal Server Error', 'message': 'This video is age-restricted. Usually we handle that, but as you see we were not able to'}), 500
    except PytubeError as e:
        log_error(f"PytubeError: {e}")
        return jsonify({'status': '500', 'error': 'Internal Server Error', 'message': 'An external library was not able to perform an operation'}), 500
    except MemoryError as e:
        log_error(f"MemoryError: {e}")
        return jsonify({'status': '507', 'error': 'Insufficient Storage', 'message': 'Good job guys, you did it.'}), 507
    except IOError as e:
        log_error(f"IOError: {e}")
        return jsonify({'status': '503', 'error': 'Service Unavailable', 'message': 'Our service is not working as expected. We are sorry :('}), 503
    except Exception as e: # pylint: disable=broad-exception-caught
        log_error(f"Exception: {e}")
        return jsonify({'status': '500', 'error': 'Internal Server Error', 'message': 'We do not know'}), 500
    else:
        return None

@app.route('/api/yt', methods=['GET'])
def endpoint_yt():
    pass


@app.route('/api/yt/video/<video_id>', methods=['GET', 'POST'])
def endpoint_video_id(video_id):
    log_debug(f"Endpoint \"/api/yt/video/<video_id>\" accessed: /api/yt/video/{video_id}")

    if not request.data:
        return [video_info for video_info in videos]

    if not request.is_json or request.headers['Content-Type'] != 'application/json':
        return jsonify({'status': '400', 'error': 'Bad Request', 'message': 'Request is not JSON'}), 400
    data = request.get_json()

    try:
        file_format = data['file_format']
    except KeyError:
        return jsonify({'status': '400', 'error': 'Bad Request', 'message': 'The file format was not supplied'}), 400

    if request.method == 'POST':
        response = handle_download(video_id=video_id, file_format=file_format)
        # Check for mp4 vs mp3 in request.json and supply accordingly
        return response if response is not None else jsonify({'status': '200', 'video_id': video_id, 'available_at': [f'/api/yt/video/{video_id}.{file_format}']}), 200

    if request.method == 'GET':
        # Load Meta Information from file
        # Return jsonify(meta information)

        return jsonify({'available_at': '/api/yt/video/'})


@app.route('/api/yt/video/<video_id>.<file_format>', methods=['GET'])
def endpoint_file_download(video_id, file_format):
    log_debug(f"Endpoint \"/api/yt/video/<video_id>.<file_format>\" accessed: /api/yt/video/{video_id}.{file_format}")
    log_debug(f"User will receive {DOWNLOAD_PATH}{video_id}.{file_format}")
    if file_format in ALLOWED_FILE_FORMATS:
        try:
            return send_file(f'{DOWNLOAD_PATH}{video_id}.{file_format}', as_attachment=True)
        except FileNotFoundError:
            response = handle_download(video_id=video_id, file_format=file_format)
            if response is None:
                try:
                    return send_file(f'{DOWNLOAD_PATH}{video_id}.{file_format}', as_attachment=True)
                except FileNotFoundError:
                        return jsonify({'status': '500', 'error': 'Internal Server Error', 'message': 'Something happened'}), 500
            return jsonify({'status': '400', 'error': 'Bad Request', 'message': 'The file does not exist'}), 400
    else:
        return jsonify({'status': '500', 'error': 'Internal Server Error', 'message': 'The supplied file format'})

@app.route('/api/yt/playlist/<playlist_id>', methods=[])
def endpoint_playlist():
    pass
