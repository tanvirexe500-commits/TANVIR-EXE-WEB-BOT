# FREE UID WEBSITE

A Flask-based web application for managing free UIDs with Discord integration and automated monitoring.

## Features

- **Free UID Management**: Add UIDs with 2-day validity
- **Discord Integration**: Automated notifications via Discord bot
- **Remote Control**: System enabled/disabled via Pastebin
- **Health Monitoring**: Comprehensive uptime and service health checks
- **Database Storage**: SQLite database for UID tracking

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd FREE-UID-WEBSITE
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python bot.py
```

Visit `http://localhost:5001` to access the application.

## Deployment Options

### 1. Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

### 2. Heroku

```bash
# Install Heroku CLI
# Login and create app
heroku create your-app-name

# Set environment variables
heroku config:set DISCORD_BOT_TOKEN="your-token"
heroku config:set DISCORD_CHANNEL_ID="your-channel-id"

# Deploy
git push heroku main
```

### 3. VPS/Cloud Server

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# Set up Python environment
pip3 install -r requirements.txt

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5001 --workers 4 wsgi:app
```

### 4. PythonAnywhere

1. Upload files to PythonAnywhere
2. Set up virtual environment
3. Install requirements
4. Configure web app with WSGI file
5. Set environment variables

## Configuration

### Environment Variables

Create a `.env` file with the following:

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///free_uids.db

DISCORD_BOT_TOKEN=your-discord-bot-token
DISCORD_CHANNEL_ID=your-discord-channel-id

UID_API_URL=http://46.250.239.109:6020
PASTEBIN_URL=https://pastebin.com/raw/jj1pZfNu

HOST=0.0.0.0
PORT=5001
DEBUG=False
```

### Discord Bot Setup

1. Create a Discord bot at [Discord Developer Portal](https://discord.com/developers/applications)
2. Get bot token and channel ID
3. Add bot to your server
4. Update `.env` with credentials

## API Endpoints

- `GET /` - Main application page
- `POST /free_add` - Add new UID (2-day validity)
- `GET /health` - Basic health check
- `GET /uptime` - Comprehensive service monitoring

## Monitoring

The `/uptime` endpoint provides detailed health information:

```json
{
  "status": "healthy|degraded|error",
  "timestamp": "2024-01-01T12:00:00",
  "services": {
    "database": {"status": "online", "uid_count": 123},
    "api_service": {"status": "online"},
    "pastebin": {"status": "online"},
    "discord_bot": {"status": "online"}
  }
}
```

## Security Notes

- Keep Discord bot token secure
- Use environment variables for sensitive data
- Regularly update dependencies
- Monitor logs for unusual activity

## Troubleshooting

### Common Issues

1. **Port already in use**: Change port in `.env` file
2. **Discord bot not working**: Verify token and permissions
3. **Database errors**: Check file permissions
4. **External API failures**: Verify network connectivity

### Logs

Check application logs for debugging:
```bash
# Docker logs
docker-compose logs web

# Application logs
tail -f app.log
```

## File Structure

```
FREE-UID-WEBSITE/
|-- bot.py              # Main Flask application
|-- config.py           # Configuration management
|-- wsgi.py            # WSGI entry point
|-- requirements.txt    # Python dependencies
|-- .env               # Environment variables
|-- .gitignore         # Git ignore file
|-- Dockerfile         # Docker configuration
|-- docker-compose.yml # Docker Compose setup
|-- nginx.conf         # Nginx configuration
|-- Procfile           # Heroku deployment
|-- templates/         # HTML templates
|-- free_uids.db       # SQLite database
|-- README.md          # This file
```

## Support

For issues and support:
1. Check the troubleshooting section
2. Review logs for error messages
3. Verify all environment variables are set
4. Ensure all external services are accessible

## License

This project is for educational purposes. Use responsibly and comply with Discord's terms of service.
