# pylint: disable=missing-docstring,line-too-long
from modules.api import app

# REGEX PATTERN for YouTube ID = r'([0-9A-Za-z_-]{11}).*'


if __name__ == "__main__":
    app.run(debug=True)
