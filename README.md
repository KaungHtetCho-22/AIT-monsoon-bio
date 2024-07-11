# Audio Analysis Server

This repo is the process of sending audio files to a server for analysis, saving the results as JSON, and sending them back to the monsoon web client.

## Overview

1. Audio files are sent from the ftp server to the gpu-server.
2. The gpu-server analyzes the audio files.
3. Analysis results are saved as JSON.
4. JSON results are sent back to the monsoon endpoint one time a day.
