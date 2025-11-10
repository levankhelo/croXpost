# croXpost - Cross-Platform Content Publisher

A comprehensive cross-posting application that allows users to publish content across multiple social media platforms simultaneously.

## Features

- 🔐 **User Authentication**: Secure JWT-based authentication system
- 📤 **Media Upload**: Support for images and videos up to 500MB
- 🌐 **Multi-Platform Support**: 
  - TikTok
  - YouTube
  - Instagram
  - Facebook
  - Reddit
  - X (Twitter)
  - Threads
- 💰 **Monetization Automation**: Enable monetization features for each platform
- 📊 **Post Tracking**: Track publishing status across all platforms
- 🎨 **Modern UI**: Clean, responsive React-based interface
- 🐳 **Containerized**: Docker Compose setup for easy deployment

## Architecture

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Authentication**: JWT tokens
- **File Storage**: Local filesystem with configurable upload directory
- **Task Queue**: Redis + Celery (for background processing)

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Styling**: Custom CSS with modern design

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15
- **Cache/Queue**: Redis 7

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 2GB of available RAM
- Ports 3000, 8000, 5432, 6379 available

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/levankhelo/croXpost.git
   cd croXpost
   ```

2. **Configure environment variables**
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env with your API keys

   # Frontend
   cp frontend/.env.example frontend/.env
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Initialize the database**
   ```bash
   # In a new terminal
   docker-compose exec backend python init_db.py
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs

## Usage

### 1. Register an Account
- Navigate to http://localhost:3000
- Click "Register" and create your account
- You'll be automatically logged in

### 2. Connect Social Media Platforms
- In the dashboard, you'll see all available platforms
- Click on each platform to connect (demo mode connects automatically)
- In production, each platform will redirect to OAuth flow

### 3. Upload and Publish Content
- Drag & drop or click to upload media (image or video)
- Add title, description, and tags
- Select target platforms
- Click "Publish" to cross-post to all selected platforms

### 4. Track Your Posts
- View all your posts in the "Recent Posts" section
- See status for each platform
- Monitor success/failure of each publication

## API Documentation

Once the backend is running, visit http://localhost:8000/api/docs for interactive API documentation.

### Key Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

#### Media
- `POST /api/media/upload` - Upload media file
- `GET /api/media/` - List user's media
- `DELETE /api/media/{id}` - Delete media

#### Platforms
- `GET /api/platforms/` - List connected platforms
- `POST /api/platforms/connect` - Connect platform
- `POST /api/platforms/{id}/monetization` - Enable monetization

#### Posts
- `POST /api/posts/` - Create and publish post
- `GET /api/posts/` - List posts
- `GET /api/posts/{id}` - Get post details

## Platform Integration

### Setting Up Platform APIs

Each platform requires API credentials. Update `backend/.env` with your credentials:

#### TikTok
1. Create app at https://developers.tiktok.com/
2. Get Client ID and Secret
3. Update `TIKTOK_CLIENT_ID` and `TIKTOK_CLIENT_SECRET`

#### YouTube
1. Create project at https://console.cloud.google.com/
2. Enable YouTube Data API v3
3. Create OAuth 2.0 credentials
4. Update `YOUTUBE_CLIENT_ID` and `YOUTUBE_CLIENT_SECRET`

#### Instagram
1. Create app at https://developers.facebook.com/
2. Add Instagram Graph API
3. Update `INSTAGRAM_CLIENT_ID` and `INSTAGRAM_CLIENT_SECRET`

#### Facebook
1. Create app at https://developers.facebook.com/
2. Update `FACEBOOK_APP_ID` and `FACEBOOK_APP_SECRET`

#### Reddit
1. Create app at https://www.reddit.com/prefs/apps
2. Update `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`

#### Twitter/X
1. Create app at https://developer.twitter.com/
2. Get API keys and bearer token
3. Update `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_BEARER_TOKEN`

#### Threads
1. Integration coming soon (API in development by Meta)

## Development

### Running Without Docker

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

### Project Structure

```
croXpost/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Core configuration
│   │   ├── models/        # Database models
│   │   ├── services/      # Business logic
│   │   │   └── platforms/ # Platform integrations
│   │   └── main.py        # FastAPI app
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── pages/         # React pages
│   │   ├── services/      # API services
│   │   ├── App.js
│   │   └── index.js
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## Security Considerations

- Change `SECRET_KEY` in production
- Use HTTPS in production
- Store API keys securely (use environment variables)
- Implement rate limiting for production
- Enable CORS only for trusted domains
- Regularly update dependencies

## Monetization Features

The platform includes automated monetization activation for:
- **YouTube**: Partner Program enrollment
- **TikTok**: Creator Fund
- **Instagram**: Badges and IGTV ads
- **Facebook**: In-stream ads
- **Twitter**: Subscriptions and tips

Note: Platform-specific requirements apply (follower count, watch hours, etc.)

## Troubleshooting

### Database Connection Issues
```bash
docker-compose down -v
docker-compose up --build
docker-compose exec backend python init_db.py
```

### Port Already in Use
Change ports in `docker-compose.yml`:
```yaml
ports:
  - "3001:3000"  # Frontend
  - "8001:8000"  # Backend
```

### File Upload Issues
Check upload directory permissions:
```bash
docker-compose exec backend mkdir -p /app/uploads
docker-compose exec backend chmod 777 /app/uploads
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- GitHub Issues: https://github.com/levankhelo/croXpost/issues
- Documentation: See `/api/docs` endpoint

## Roadmap

- [ ] Complete OAuth flows for all platforms
- [ ] Real-time publishing status updates
- [ ] Scheduled posting
- [ ] Analytics dashboard
- [ ] Content calendar
- [ ] Team collaboration features
- [ ] Mobile app
- [ ] AI-powered content optimization
- [ ] Hashtag suggestions
- [ ] Cross-platform analytics

## Acknowledgments

Built with modern web technologies and best practices for production-ready applications
