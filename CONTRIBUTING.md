# Contributing to croXpost

Thank you for your interest in contributing to croXpost! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/croXpost.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Add some feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### Running Locally

```bash
# Using Docker (recommended)
./start.sh

# Or manually
docker-compose up --build
```

### Running Without Docker

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
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

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions and classes
- Run black for formatting: `black app/`
- Run flake8 for linting: `flake8 app/`

### JavaScript (Frontend)
- Use ES6+ features
- Use functional components with hooks
- Follow React best practices
- Keep components focused and reusable

## Adding a New Platform

To add support for a new social media platform:

1. Create a new publisher in `backend/app/services/platforms/`:

```python
from typing import Dict, Optional, List
from app.services.platforms.base import BasePlatformPublisher

class YourPlatformPublisher(BasePlatformPublisher):
    def publish(self, media_path, title=None, description=None, tags=None):
        # Implement platform-specific publishing logic
        pass
    
    def enable_monetization(self):
        # Implement monetization logic
        pass
```

2. Register the publisher in `backend/app/services/crosspost.py`:

```python
from app.services.platforms.yourplatform import YourPlatformPublisher

PLATFORM_PUBLISHERS = {
    # ... existing platforms
    "yourplatform": YourPlatformPublisher,
}
```

3. Add platform config in `backend/app/core/config.py`:

```python
YOURPLATFORM_CLIENT_ID: str = ""
YOURPLATFORM_CLIENT_SECRET: str = ""
```

4. Add the platform to frontend `AVAILABLE_PLATFORMS` in `Dashboard.js`:

```javascript
{ id: 'yourplatform', name: 'Your Platform', icon: '🆕', color: '#000000' }
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Pull Request Guidelines

- Keep PRs focused on a single feature or bug fix
- Include tests for new functionality
- Update documentation as needed
- Ensure all tests pass
- Follow the existing code style
- Write clear commit messages

## Feature Requests

To request a new feature:
1. Check existing issues to avoid duplicates
2. Create a new issue with the "feature request" label
3. Describe the feature and its use case
4. Provide examples if possible

## Bug Reports

To report a bug:
1. Check existing issues to avoid duplicates
2. Create a new issue with the "bug" label
3. Include steps to reproduce
4. Include expected vs actual behavior
5. Include environment details (OS, Docker version, etc.)

## Questions?

- Open an issue with the "question" label
- Check the README for common setup issues

Thank you for contributing!
