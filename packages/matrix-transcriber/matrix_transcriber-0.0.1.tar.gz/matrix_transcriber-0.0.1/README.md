# matrix-transcriber

This Matrix bot listens to audio messages and answers with a transcript of their content.

# Installation

The bot uses [Whisper](https://github.com/openai/whisper#setup) to transcribe audio files, which requires `ffmpeg` to be installed.

# Configuration

The following environment variables are used for configuration:

```sh
# Which Whisper model should be used?
WHISPER_MODEL=base

# Which Matrix server should be used to log in to?
MATRIX_SERVER=https://matrix.example.org

# What Matrix account shall the bot use?
MATRIX_USER=@transcription:example.org

# What it its password?
MATRIX_PASSWORD=<Password>

# Which directory should the bot use to store its state in?
STATE_DIR=/var/lib/matrix-transcriber

# Who is allowed to invite the bot into new rooms?
INVITERS="@me:example.org
@friend1:example.org
@friend2:example.com"
# Every invitation of someone else will be declined.
```

# Usage

Execute `main.py` and invite the bot into a room. If someone sends an audio message into the room, it will be transcribed. (If not, check what the script wrote on its output and open an issue)