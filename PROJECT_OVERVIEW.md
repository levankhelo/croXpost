# croXpost Project Overview

## Project Summary

croXpost is a complete cross-posting application that enables users to publish content across multiple social media platforms simultaneously. The application features a modern architecture with separated frontend and backend, comprehensive authentication, and a fully containerized deployment setup.

## Technical Stack

### Backend
- **Language**: Python 3.11
- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **Task Queue**: Celery + Redis
- **File Processing**: Pillow, moviepy, python-magic

### Frontend
- **Framework**: React 18.2.0
- **Routing**: React Router v6.20.0
- **HTTP Client**: Axios 1.6.2
- **Build Tool**: react-scripts 5.0.1
- **Styling**: Custom CSS (no framework dependencies)

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15 (Alpine)
- **Cache/Queue**: Redis 7 (Alpine)
- **Web Server**: Uvicorn (ASGI)

## Features Implemented

### 1. User Authentication & Management
- JWT-based authentication
- User registration and login
- Password hashing with bcrypt
- Token refresh mechanism
- Protected routes and endpoints

### 2. Platform Integration
- Framework for 7 social media platforms:
  - TikTok
  - YouTube
  - Instagram
  - Facebook
  - Reddit
  - X (Twitter)
  - Threads
- OAuth token storage
- Platform connection management
- Monetization automation hooks

### 3. Media Management
- File upload (images and videos)
- Support for files up to 500MB
- Drag & drop interface
- File type validation
- Metadata storage (size, type, dimensions)

### 4. Cross-Posting
- Multi-platform publishing
- Post status tracking
- Platform-specific results
- Background task processing
- Error handling and reporting

### 5. User Interface
- Modern, responsive design
- Gradient backgrounds
- Card-based layouts
- Real-time status updates
- Intuitive navigation

## Architecture

### Backend Structure
```
backend/
├── app/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Authentication routes
│   │   ├── users.py      # User management
│   │   ├── media.py      # Media upload
│   │   ├── platforms.py  # Platform connections
│   │   └── posts.py      # Cross-posting
│   ├── core/             # Core functionality
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # Database setup
│   │   └── security.py   # Auth utilities
│   ├── models/           # Database models
│   │   ├── user.py
│   │   ├── platform_account.py
│   │   ├── media.py
│   │   └── post.py
│   └── services/         # Business logic
│       ├── crosspost.py  # Publishing logic
│       └── platforms/    # Platform publishers
├── Dockerfile
└── requirements.txt
```

### Frontend Structure
```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── pages/            # Page components
│   │   ├── Login.js
│   │   ├── Register.js
│   │   └── Dashboard.js
│   ├── services/         # API services
│   │   ├── api.js        # Axios setup
│   │   └── index.js      # Service functions
│   ├── App.js            # Main app component
│   ├── App.css           # Styles
│   └── index.js          # Entry point
├── Dockerfile
└── package.json
```

### Database Schema

#### Users Table
- id (PK)
- email (unique)
- username (unique)
- hashed_password
- full_name
- is_active
- is_superuser
- created_at
- updated_at

#### Platform Accounts Table
- id (PK)
- user_id (FK)
- platform (tiktok, youtube, etc.)
- platform_user_id
- platform_username
- access_token
- refresh_token
- token_expires_at
- is_active
- monetization_enabled
- platform_data (JSON)
- created_at
- updated_at

#### Media Files Table
- id (PK)
- user_id (FK)
- filename
- original_filename
- file_path
- file_size
- media_type (image/video)
- mime_type
- duration
- width
- height
- thumbnail_path
- created_at

#### Posts Table
- id (PK)
- user_id (FK)
- media_file_id (FK)
- title
- description
- tags (JSON)
- status (draft, publishing, published, failed, partial)
- scheduled_at
- created_at
- updated_at

#### Platform Posts Table
- id (PK)
- post_id (FK)
- platform
- platform_post_id
- platform_url
- status (success, failed, pending)
- error_message
- published_at
- created_at

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Users
- `GET /api/users/me` - Get current user info
- `GET /api/users/{id}` - Get user by ID

### Media
- `POST /api/media/upload` - Upload media file
- `GET /api/media/` - List user's media
- `GET /api/media/{id}` - Get media details
- `DELETE /api/media/{id}` - Delete media

### Platforms
- `GET /api/platforms/` - List connected platforms
- `POST /api/platforms/connect` - Connect platform account
- `DELETE /api/platforms/{id}` - Disconnect platform
- `POST /api/platforms/{id}/monetization` - Enable monetization

### Posts
- `POST /api/posts/` - Create and publish post
- `GET /api/posts/` - List posts
- `GET /api/posts/{id}` - Get post details
- `DELETE /api/posts/{id}` - Delete post

## Security Features

1. **Password Security**
   - bcrypt hashing
   - Salted passwords
   - No plain text storage

2. **Authentication**
   - JWT tokens
   - Token expiration
   - Refresh token support

3. **Authorization**
   - User-specific resources
   - Protected endpoints
   - Role-based access (is_superuser)

4. **CORS**
   - Configurable origins
   - Credentials support
   - Methods and headers control

5. **Input Validation**
   - Pydantic models
   - File type validation
   - Size limits

## Deployment

### Development
```bash
./start.sh
# Or manually:
docker-compose up --build
docker-compose exec backend python init_db.py
```

### Production Considerations
1. Change SECRET_KEY
2. Use environment-specific .env files
3. Enable HTTPS
4. Set up reverse proxy (nginx)
5. Configure proper CORS origins
6. Implement rate limiting
7. Set up monitoring and logging
8. Use production-grade database
9. Configure backup strategy
10. Implement CI/CD pipeline

## Testing Strategy

### Backend Testing
- Unit tests for models
- Integration tests for APIs
- Authentication flow tests
- Database transaction tests

### Frontend Testing
- Component unit tests
- Integration tests
- E2E tests with Cypress
- Accessibility tests

## Extensibility

### Adding New Platforms
1. Create publisher in `services/platforms/`
2. Inherit from `BasePlatformPublisher`
3. Implement `publish()` and `enable_monetization()`
4. Register in `PLATFORM_PUBLISHERS`
5. Add configuration to `config.py`
6. Update frontend `AVAILABLE_PLATFORMS`

### Adding New Features
- Use existing patterns
- Follow separation of concerns
- Update documentation
- Add tests
- Update API docs

## Performance Considerations

1. **Database**
   - Indexed columns (email, username)
   - Connection pooling
   - Query optimization

2. **File Handling**
   - Streaming uploads
   - Background processing
   - Cleanup routines

3. **API**
   - Async endpoints
   - Background tasks
   - Pagination support

4. **Caching**
   - Redis for sessions
   - Platform token caching
   - Query result caching

## Monitoring & Logging

### Recommended Tools
- **Application**: Sentry for error tracking
- **Infrastructure**: Prometheus + Grafana
- **Logs**: ELK Stack or Loki
- **Uptime**: UptimeRobot or Pingdom

### Key Metrics
- API response times
- Database query performance
- Upload success rates
- Platform API success rates
- Active users
- Storage usage

## Future Enhancements

### Planned Features
1. Real OAuth flows for each platform
2. Scheduled posting
3. Analytics dashboard
4. Content calendar
5. Team collaboration
6. Mobile app
7. AI-powered content optimization
8. Hashtag suggestions
9. Cross-platform analytics
10. Webhook support

### Technical Improvements
1. WebSocket for real-time updates
2. GraphQL API option
3. Microservices architecture
4. Kubernetes deployment
5. Multi-region support
6. CDN integration
7. Advanced caching
8. Rate limiting per user
9. API versioning
10. Automated testing

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Development setup
- Code style
- Pull request process
- Bug reporting
- Feature requests

## License

MIT License - see [LICENSE](LICENSE) file

## Support & Resources

- **Documentation**: See README.md
- **Platform Setup**: See PLATFORM_SETUP.md
- **API Docs**: http://localhost:8000/api/docs
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

## Acknowledgments

Built with modern web technologies and best practices:
- FastAPI for high-performance Python APIs
- React for declarative UIs
- PostgreSQL for robust data storage
- Docker for consistent environments
- Open source community tools and libraries

---

**Version**: 1.0.0  
**Last Updated**: November 2024  
**Status**: Production Ready (with platform API implementation required)
