# Application Flow

This document describes the user journey and data flow through the croXpost application.

## User Journey

### 1. Registration & Login Flow

```
User -> Frontend (Register Page)
         ↓
         POST /api/auth/register
         {email, username, password, full_name}
         ↓
      Backend API
         ↓
      Validate Input
         ↓
      Hash Password (bcrypt)
         ↓
      Save to Database (Users table)
         ↓
      Generate JWT Tokens
         ↓
      Return {access_token, refresh_token, user}
         ↓
      Frontend stores tokens
         ↓
      Redirect to Dashboard
```

### 2. Platform Connection Flow

```
User -> Dashboard (Select Platform)
         ↓
         Click "Connect to TikTok"
         ↓
      [In production: OAuth Redirect]
      [Demo: Auto-connect with demo token]
         ↓
         POST /api/platforms/connect
         {platform, access_token, refresh_token}
         ↓
      Backend API
         ↓
      Save Platform Account
         {user_id, platform, tokens}
         ↓
      Return Platform Account
         ↓
      Frontend updates UI
         ↓
      Platform shows as "Connected"
```

### 3. Media Upload Flow

```
User -> Dashboard (Upload Area)
         ↓
      Drag & Drop or Click to Select
         ↓
      File Selected
         ↓
      Frontend Validation
         - File type (image/video)
         - File size (< 500MB)
         ↓
         POST /api/media/upload
         FormData with file
         ↓
      Backend API
         ↓
      Validate File
         ↓
      Generate Unique Filename
         ↓
      Save to Filesystem (/app/uploads/)
         ↓
      Save Metadata to Database
         {user_id, filename, size, type}
         ↓
      Return Media Object
         ↓
      Frontend displays success
         ↓
      Show Post Form
```

### 4. Cross-Posting Flow

```
User -> Dashboard (Post Form)
         ↓
      Enter Title, Description, Tags
         ↓
      Select Platforms (checkboxes)
         - TikTok ✓
         - YouTube ✓
         - Instagram ✓
         ↓
      Click "Publish"
         ↓
         POST /api/posts/
         {
           media_file_id,
           title,
           description,
           tags: ["viral", "trending"],
           platforms: ["tiktok", "youtube", "instagram"]
         }
         ↓
      Backend API
         ↓
      Validate User Owns Media
         ↓
      Check Platforms Connected
         ↓
      Create Post Record
         {user_id, media_file_id, status: "publishing"}
         ↓
      Create Platform Post Records
         - TikTok: pending
         - YouTube: pending
         - Instagram: pending
         ↓
      Queue Background Task
         ↓
      Return Post Object
         ↓
      Frontend shows "Publishing..."
         ↓
      [Background Task Starts]
```

### 5. Background Publishing Flow

```
Background Task (Celery/async)
         ↓
      For each platform:
         ↓
      Get Platform Account
         ↓
      Get Platform Publisher
         (TikTokPublisher, YouTubePublisher, etc.)
         ↓
      Call publisher.publish()
         {
           media_path,
           title,
           description,
           tags
         }
         ↓
      [Platform API Call]
         ↓
      Success or Failure
         ↓
      Update Platform Post
         {
           status: "success/failed",
           platform_post_id,
           platform_url,
           error_message (if failed)
         }
         ↓
      Next Platform
         ↓
      All Platforms Done
         ↓
      Update Overall Post Status
         - published (all success)
         - partial (some success)
         - failed (all failed)
         ↓
      Save to Database
```

### 6. Post Tracking Flow

```
User -> Dashboard (Recent Posts)
         ↓
         GET /api/posts/
         ↓
      Backend API
         ↓
      Query Posts by user_id
         ↓
      Include Platform Posts
         ↓
      Return Posts List
         [
           {
             id, title, description, status,
             platform_posts: [
               {platform: "tiktok", status: "success", url: "..."},
               {platform: "youtube", status: "success", url: "..."},
               {platform: "instagram", status: "failed", error: "..."}
             ]
           }
         ]
         ↓
      Frontend displays:
         - Post details
         - Overall status badge
         - Per-platform results
         - Links to published content
```

## Data Flow Diagrams

### Authentication Data Flow

```
┌─────────┐      ┌─────────┐      ┌──────────┐      ┌──────────┐
│         │      │         │      │          │      │          │
│ Browser │─────▶│ Frontend│─────▶│  Backend │─────▶│ Database │
│         │      │         │      │   API    │      │          │
└─────────┘      └─────────┘      └──────────┘      └──────────┘
     ▲                │                  │                │
     │                │                  │                │
     │                ▼                  ▼                ▼
     │           Store Token       Hash Password     Save User
     │                                   │
     └───────────────────────────────────┘
                 Return Token
```

### Media Upload Data Flow

```
┌─────────┐      ┌─────────┐      ┌──────────┐      ┌────────────┐
│         │      │         │      │          │      │            │
│ Browser │─────▶│ Frontend│─────▶│  Backend │─────▶│ Filesystem │
│         │      │         │      │   API    │      │            │
└─────────┘      └─────────┘      └──────────┘      └────────────┘
                                        │
                                        ▼
                                   ┌──────────┐
                                   │ Database │
                                   │ (metadata)│
                                   └──────────┘
```

### Cross-Posting Data Flow

```
┌─────────┐      ┌─────────┐      ┌──────────┐      ┌──────────┐
│         │      │         │      │          │      │          │
│ Browser │─────▶│ Frontend│─────▶│  Backend │─────▶│ Database │
│         │      │         │      │   API    │      │          │
└─────────┘      └─────────┘      └──────────┘      └──────────┘
                                        │
                                        ▼
                                   ┌──────────┐
                                   │Background│
                                   │  Tasks   │
                                   └──────────┘
                                        │
                     ┌──────────────────┼──────────────────┐
                     ▼                  ▼                  ▼
                ┌─────────┐        ┌─────────┐       ┌─────────┐
                │ TikTok  │        │ YouTube │       │Instagram│
                │   API   │        │   API   │       │   API   │
                └─────────┘        └─────────┘       └─────────┘
```

## State Management

### Frontend State

```javascript
// Authentication State
{
  isAuthenticated: boolean,
  user: {
    id, email, username, full_name
  },
  tokens: {
    accessToken,
    refreshToken
  }
}

// Media State
{
  selectedFile: File | null,
  uploadedMedia: MediaObject | null,
  uploadProgress: number
}

// Post State
{
  postForm: {
    title, description, tags
  },
  selectedPlatforms: string[],
  posts: PostObject[]
}

// Platform State
{
  connectedPlatforms: string[]
}
```

### Backend State

```python
# Database Session State
- Active connections
- Transaction management
- Connection pooling

# File System State
- Uploaded files in /app/uploads/
- File metadata tracking

# Platform State
- OAuth tokens
- Token expiration
- Platform connections

# Background Task State
- Pending tasks
- Running tasks
- Completed tasks
```

## Error Handling Flow

```
Error Occurs
    │
    ├─ Frontend Error
    │   ├─ Network Error
    │   │   └─ Show error message
    │   │       └─ "Connection failed. Please try again."
    │   │
    │   ├─ Validation Error
    │   │   └─ Highlight field
    │   │       └─ Show specific error
    │   │
    │   └─ 401 Unauthorized
    │       └─ Clear tokens
    │           └─ Redirect to login
    │
    └─ Backend Error
        ├─ Validation Error (400)
        │   └─ Return detailed message
        │
        ├─ Authentication Error (401)
        │   └─ Return "Invalid credentials"
        │
        ├─ Authorization Error (403)
        │   └─ Return "Access denied"
        │
        ├─ Not Found (404)
        │   └─ Return "Resource not found"
        │
        └─ Server Error (500)
            └─ Log error
                └─ Return generic message
```

## Performance Optimization

### Frontend
- Lazy loading of components
- Code splitting by route
- Image/video preview optimization
- Debounced API calls
- Local state caching

### Backend
- Database connection pooling
- Indexed queries
- Async endpoints
- Background task processing
- File streaming

### Database
- Indexed columns (email, username, user_id)
- Foreign key constraints
- Query optimization
- Regular vacuum/analyze

## Security Layers

```
Request Flow with Security:

Browser Request
    ↓
HTTPS/TLS
    ↓
CORS Check
    ↓
JWT Validation
    ↓
User Authorization
    ↓
Input Validation
    ↓
Business Logic
    ↓
Database Query
    ↓
Response
```

---

This flow documentation helps understand how data moves through the application and how different components interact.
