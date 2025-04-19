# GRRIF Tools

A set of tools for Cool Cats™.

GRRIF Tools allows you to archive GRRIF radio's play history to a SQLite database or text files, compute statistics (top artists and tracks), stream the radio live in your console, and scrobble tracks to Last.fm.

## Features

- **Archive play history**: Save GRRIF's played tracks to a SQLite database or text files.
- **Statistics**: View top artists and tracks over custom date ranges.
- **Live streaming**: Listen to GRRIF radio directly in your terminal.
- **Last.fm scrobbling**: Automatically scrobble tracks while streaming or in standalone mode.
- **TUI interface**: User-friendly terminal interface for all features.

## Installation

```bash
pip install grrif-tools
```

## Usage

GRRIF Tools can be used in two ways:

### 1. Terminal User Interface (TUI)

For a user-friendly interface, simply run:

```bash
grrif_tools --tui
```

Navigate through the menu with arrow keys and select options with Enter. The TUI provides access to all features with an intuitive interface.

### 2. Command Line Interface (CLI)

```
usage: grrif_tools [-h] [--tui] {archive,stats,play,scrobble} ...

GRRIF Tools v0.9.1: A set of tools for Cool Cats™. Allows you to archive GRRIF's play history, view stats,
stream the radio, and scrobble to Last.fm.

positional arguments:
  {archive,stats,scrobble,play}
    archive             Archive GRRIF's play history.
    stats               Get statistics from the play history.
    scrobble            Scrobble to Last.fm.
    play                Stream GRRIF radio in the console.

options:
  -h, --help            show this help message and exit
  --tui                 Launch the terminal user interface
```

#### Archive

Archive GRRIF's play history to a database, text files, or print to stdout:

```bash
# Archive to SQLite database
grrif_tools archive db [from_date] [to_date]

# Archive to text files
grrif_tools archive txt [from_date] [to_date]

# Print to stdout
grrif_tools archive print [from_date] [to_date]
```

Dates should be in YYYY-MM-DD format. If omitted, defaults to 2021-01-01 and today.

#### Statistics

View statistics about most played artists or tracks:

```bash
# View top 10 artists
grrif_tools stats artists top10 [from_date] [to_date]

# View top 25 tracks
grrif_tools stats tracks top25 [from_date] [to_date]

# View top 100 artists
grrif_tools stats artists top100 [from_date] [to_date]
```

#### Streaming

Listen to GRRIF radio in your terminal:

```bash
# Stream with high quality MP3
grrif_tools play mp3_high

# Stream with low quality MP3
grrif_tools play mp3_low

# Stream with high quality AAC
grrif_tools play aac_high
```

The console will display the currently playing track and scrobble it to Last.fm if credentials are configured.

#### Last.fm Scrobbling

GRRIF Tools provides a simple way to set up Last.fm scrobbling:

```bash
# Authenticate with Last.fm (interactive)
grrif_tools scrobble authenticate API_KEY API_SECRET

# Manually set Last.fm credentials (if you already have a session key)
grrif_tools scrobble settings API_KEY API_SECRET SESSION_KEY

# Start scrobbling
grrif_tools scrobble start
```

The `authenticate` command handles the full Last.fm authentication flow:
1. Requests a token from Last.fm
2. Opens your browser to authorize the application
3. Waits for your confirmation
4. Retrieves and saves your session key automatically

Scrobbling will automatically track what's playing on GRRIF and send it to your Last.fm account.

## Last.fm Authentication

To use the scrobbling feature, you'll need a Last.fm API account:

1. Create an API account at https://www.last.fm/api/account/create
2. Get your API key and secret
3. Run the authentication command:
   ```bash
   grrif_tools scrobble authenticate YOUR_API_KEY YOUR_API_SECRET
   ```
4. Follow the prompts to authorize the application in your browser
5. Once authorized, your session key will be saved automatically

If you prefer to handle the authentication process manually, you can still use the traditional method:
1. Get a token from https://www.last.fm/api/auth with your API key
2. Authorize the token by visiting https://www.last.fm/api/auth?api_key=YOUR_API_KEY&token=YOUR_TOKEN
3. Create an MD5 hash of "api_key[your api key]methodauth.getSessiontoken[your token][your api secret]"
4. Send a request to https://ws.audioscrobbler.com/2.0/?method=auth.getSession&api_key=YOUR_API_KEY&token=YOUR_TOKEN&api_sig=YOUR_MD5_HASH
5. Set the obtained session key with `grrif_tools scrobble settings API_KEY API_SECRET SESSION_KEY`

## Data Storage

All data is stored in your home directory under `~/grrif_data/`:

- SQLite database: `~/grrif_data/grrif_data.db`
- Text files: `~/grrif_data/plays/YYYY/MM/DD.txt`
- Configuration: `~/grrif_data/config.json`
- Temporary buffer file: `~/grrif_data/buferr.mp3`

## Examples

### Archiving the last week of plays

```bash
# Get today's date
today=$(date +%Y-%m-%d)
# Get date from a week ago
last_week=$(date -d "7 days ago" +%Y-%m-%d)
# Archive to database
grrif_tools archive db $last_week $today
```

### Finding your favorite artists from the last month

```bash
# Get today's date
today=$(date +%Y-%m-%d)
# Get date from a month ago
last_month=$(date -d "30 days ago" +%Y-%m-%d)
# Show top 25 artists
grrif_tools stats artists top25 $last_month $today
```

### Setting up scrobbling and leaving it running

```bash
# Start in a screen session
screen -S grrif-scrobble
# Start scrobbling (after authentication)
grrif_tools scrobble start
# Detach with Ctrl+A then D
```

## Notes

This package is unofficial and meant as a fun tool for GRRIF radio fans. Please be considerate and don't overload GRRIF's website with requests.

## Development

If you want to contribute to the development:

1. Clone the repository: `git clone https://github.com/fetzu/grrif-tools.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
4. Install in development mode: `pip install -e .`
5. Run linting: `pylint grrif_tools`
6. Submit a PR with your changes

## License

MIT License
