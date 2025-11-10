# Platform API Setup Guide

This guide helps you set up API credentials for each supported platform.

## Overview

croXpost supports the following platforms:
- TikTok
- YouTube
- Instagram
- Facebook
- Reddit
- X (Twitter)
- Threads

Each platform requires API credentials to enable posting functionality.

## TikTok

### Requirements
- TikTok Developer Account
- Registered Application

### Setup Steps
1. Visit https://developers.tiktok.com/
2. Sign in with your TikTok account
3. Create a new app
4. Navigate to "Manage apps" → Your app → "Basic Information"
5. Copy your Client Key (Client ID) and Client Secret
6. Add redirect URI: `http://localhost:8000/api/platforms/tiktok/callback`

### Environment Variables
```env
TIKTOK_CLIENT_ID=your_client_key
TIKTOK_CLIENT_SECRET=your_client_secret
```

### OAuth Scopes Needed
- `user.info.basic`
- `video.upload`
- `video.publish`

## YouTube

### Requirements
- Google Cloud Project
- YouTube Data API v3 enabled

### Setup Steps
1. Visit https://console.cloud.google.com/
2. Create a new project or select existing
3. Enable YouTube Data API v3
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Select "Web application"
6. Add redirect URI: `http://localhost:8000/api/platforms/youtube/callback`
7. Copy Client ID and Client Secret

### Environment Variables
```env
YOUTUBE_CLIENT_ID=your_client_id.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=your_client_secret
```

### OAuth Scopes Needed
- `https://www.googleapis.com/auth/youtube.upload`
- `https://www.googleapis.com/auth/youtube`

## Instagram

### Requirements
- Facebook Developer Account
- Instagram Business or Creator Account
- Facebook Page connected to Instagram

### Setup Steps
1. Visit https://developers.facebook.com/
2. Create a new app or select existing
3. Add "Instagram Graph API" product
4. Configure Instagram Graph API settings
5. Get App ID and App Secret from app settings
6. Add redirect URI: `http://localhost:8000/api/platforms/instagram/callback`

### Environment Variables
```env
INSTAGRAM_CLIENT_ID=your_app_id
INSTAGRAM_CLIENT_SECRET=your_app_secret
```

### OAuth Scopes Needed
- `instagram_basic`
- `instagram_content_publish`
- `pages_read_engagement`

## Facebook

### Requirements
- Facebook Developer Account
- Facebook Page

### Setup Steps
1. Visit https://developers.facebook.com/
2. Create a new app (Business type)
3. Add "Facebook Login" product
4. Get App ID and App Secret
5. Configure OAuth redirect URI: `http://localhost:8000/api/platforms/facebook/callback`

### Environment Variables
```env
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
```

### OAuth Scopes Needed
- `pages_manage_posts`
- `pages_read_engagement`
- `publish_video`

## Reddit

### Requirements
- Reddit Account
- Reddit Application

### Setup Steps
1. Visit https://www.reddit.com/prefs/apps
2. Click "create application"
3. Select "web app"
4. Set redirect URI: `http://localhost:8000/api/platforms/reddit/callback`
5. Copy Client ID (under app name) and Secret

### Environment Variables
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
```

### OAuth Scopes Needed
- `identity`
- `submit`

## X (Twitter)

### Requirements
- Twitter Developer Account (approved)
- Twitter App with OAuth 2.0

### Setup Steps
1. Visit https://developer.twitter.com/en/portal/dashboard
2. Create a new project and app
3. Enable OAuth 2.0
4. Add redirect URI: `http://localhost:8000/api/platforms/twitter/callback`
5. Copy API Key, API Secret, and Bearer Token

### Environment Variables
```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

### OAuth Scopes Needed
- `tweet.read`
- `tweet.write`
- `users.read`
- `offline.access`

## Threads

### Requirements
- Meta/Facebook Developer Account
- Threads API Access (when available)

### Setup Steps
Threads API is currently in development by Meta. This integration is a placeholder for when the API becomes publicly available.

### Environment Variables
```env
THREADS_CLIENT_ID=your_client_id
THREADS_CLIENT_SECRET=your_client_secret
```

## Testing Your Setup

After configuring your API credentials:

1. Update `backend/.env` with your credentials
2. Restart the backend: `docker-compose restart backend`
3. Login to croXpost
4. Try connecting each platform from the dashboard
5. Test posting to verify the integration works

## Common Issues

### Invalid Redirect URI
Make sure your redirect URIs match exactly in both your platform app settings and croXpost configuration.

### Scope/Permission Errors
Ensure you've requested all necessary OAuth scopes for each platform.

### Rate Limiting
Most platforms have rate limits. Implement appropriate delays and error handling in production.

### Expired Tokens
Implement token refresh logic for long-term use. The base publisher class includes a `refresh_access_token()` method for this purpose.

## Security Best Practices

1. **Never commit credentials**: Always use environment variables
2. **Use HTTPS in production**: Redirect URIs should use HTTPS
3. **Rotate secrets regularly**: Change API secrets periodically
4. **Limit scope access**: Only request necessary OAuth scopes
5. **Monitor API usage**: Set up alerts for unusual activity

## Need Help?

- Check platform-specific documentation
- Review error messages carefully
- Test with platform API explorers first
- Open an issue on GitHub with details
