# Audio Analysis Server

This repository contains the process for analyzing audio files on a server, saving the results as JSON, and sending them back to the Monsoon web client.

## Overview

The system processes audio files recorded continuously by devices and uploaded to an FTP server. At a specified time each day (e.g., 23:00:00), the following process occurs:

1. Audio files are transferred from the FTP server to the GPU server.
2. The GPU server analyzes the audio files.
3. Analysis results are saved as JSON files.
4. JSON results are sent to the Monsoon endpoint (not yet implemented).

## Directory Structure

### FTP Server

Audio files are saved on the FTP server with the following structure:

- Device_id/
- Date/
- audio_files/ 

### GPU Server

The `continuous_audio_processing.py` script reads files from the FTP server, processes them on the GPU server, and saves the results

- Device_id/
- Date/
- audio_files.json/ 

can be found at `sample_json`

## Scripts

1. `continuous_audio_processing.py`: Processes audio files and generates individual JSON results.
2. `json_schema.py`: Combines daily JSON results and applies necessary modifications.

## Future Implementation

- Sending the final JSON results to the Monsoon endpoint (not yet tested).

## Notes

- The audio file transfer and processing schedule can be adapted according to specific needs.
- The current setup includes mocked-up data for 5 sites.