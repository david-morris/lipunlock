#!/bin/bash
sox -t alsa default -t flac - trim 0 4 | curl -X POST \
--data-binary @/dev/stdin \
--user-agent 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36' \
--header 'Content-Type: audio/x-flac; rate=44100;' \
'https://www.google.com/speech-api/v2/recognize?output=json&lang=en-us&key=AIzaSyCnl6MRydhw_5fLXIdASxkLJzcJh5iX0M4'


