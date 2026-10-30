# Data Sources and API

## Data Source

YouTube Data API v3 is the primary external data source.

Official documentation:
https://developers.google.com/youtube/v3

## API Operations Used

### Search
The search endpoint is used to discover YouTube channels based on a keyword.

### Channels
The channels endpoint retrieves public channel metadata and statistics.

### Videos
The videos endpoint retrieves public video statistics for engagement analysis.

### Comment Threads
The commentThreads endpoint is used to retrieve available public comments for sentiment analysis.

## Credentials

The API key is loaded from a local .env file through python-dotenv.

Never commit API keys or secrets.

## Quota Considerations

YouTube API requests consume quota. Search requests can consume substantially more quota than some read operations. Usage depends on the API endpoint and request parameters.

## Data Availability

Some statistics may be hidden, disabled, unavailable, or restricted. The application should handle missing fields rather than invent values.

## Privacy and Limitations

This project uses public API information. It does not access private creator analytics or private audience demographics through the public API key.
