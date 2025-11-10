import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService, mediaService, platformService, postService } from '../services';

const AVAILABLE_PLATFORMS = [
  { id: 'tiktok', name: 'TikTok', icon: '📱', color: '#000000' },
  { id: 'youtube', name: 'YouTube', icon: '▶️', color: '#FF0000' },
  { id: 'instagram', name: 'Instagram', icon: '📷', color: '#E1306C' },
  { id: 'facebook', name: 'Facebook', icon: '👥', color: '#1877F2' },
  { id: 'reddit', name: 'Reddit', icon: '🤖', color: '#FF4500' },
  { id: 'twitter', name: 'X (Twitter)', icon: '🐦', color: '#1DA1F2' },
  { id: 'threads', name: 'Threads', icon: '🧵', color: '#000000' }
];

function Dashboard({ setIsAuthenticated }) {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedMedia, setUploadedMedia] = useState(null);
  const [selectedPlatforms, setSelectedPlatforms] = useState([]);
  const [connectedPlatforms, setConnectedPlatforms] = useState([]);
  const [posts, setPosts] = useState([]);
  const [postForm, setPostForm] = useState({
    title: '',
    description: '',
    tags: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    const currentUser = authService.getCurrentUser();
    setUser(currentUser);
    loadConnectedPlatforms();
    loadPosts();
  }, []);

  const loadConnectedPlatforms = async () => {
    try {
      const platforms = await platformService.list();
      setConnectedPlatforms(platforms.map(p => p.platform));
    } catch (err) {
      console.error('Failed to load platforms:', err);
    }
  };

  const loadPosts = async () => {
    try {
      const postsList = await postService.list();
      setPosts(postsList);
    } catch (err) {
      console.error('Failed to load posts:', err);
    }
  };

  const handleLogout = () => {
    authService.logout();
    setIsAuthenticated(false);
    navigate('/login');
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setUploadedMedia(null);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      setSelectedFile(file);
      setUploadedMedia(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError('');
    
    try {
      const media = await mediaService.upload(selectedFile);
      setUploadedMedia(media);
      setSuccess('Media uploaded successfully!');
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const togglePlatform = (platformId) => {
    setSelectedPlatforms(prev => 
      prev.includes(platformId)
        ? prev.filter(id => id !== platformId)
        : [...prev, platformId]
    );
  };

  const connectPlatform = async (platformId) => {
    // In a real app, this would redirect to OAuth flow
    // For demo, we'll just simulate connection
    setError('');
    setSuccess('');
    
    try {
      await platformService.connect({
        platform: platformId,
        access_token: `demo_token_${platformId}`,
        platform_username: `demo_user_${platformId}`
      });
      setSuccess(`Connected to ${platformId}!`);
      loadConnectedPlatforms();
    } catch (err) {
      setError(`Failed to connect to ${platformId}`);
    }
  };

  const handlePublish = async () => {
    if (!uploadedMedia) {
      setError('Please upload media first');
      return;
    }

    if (selectedPlatforms.length === 0) {
      setError('Please select at least one platform');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const tagsList = postForm.tags ? postForm.tags.split(',').map(t => t.trim()) : [];
      
      await postService.create({
        media_file_id: uploadedMedia.id,
        title: postForm.title,
        description: postForm.description,
        tags: tagsList,
        platforms: selectedPlatforms
      });

      setSuccess('Post is being published to selected platforms!');
      setSelectedFile(null);
      setUploadedMedia(null);
      setSelectedPlatforms([]);
      setPostForm({ title: '', description: '', tags: '' });
      
      // Reload posts
      setTimeout(() => loadPosts(), 2000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Publishing failed');
    } finally {
      setLoading(false);
    }
  };

  const getStatusClass = (status) => {
    const statusMap = {
      'published': 'status-published',
      'failed': 'status-failed',
      'partial': 'status-partial',
      'publishing': 'status-publishing'
    };
    return statusMap[status] || '';
  };

  return (
    <div className="dashboard">
      <header className="header">
        <div className="header-content">
          <h1>🚀 croXpost</h1>
          <div>
            <span style={{ marginRight: '20px' }}>Welcome, {user?.username}!</span>
            <button className="btn-logout" onClick={handleLogout}>Logout</button>
          </div>
        </div>
      </header>

      <div className="dashboard-content">
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <div className="section">
          <h2>📤 Upload Media</h2>
          
          <div 
            className={`upload-area ${isDragging ? 'drag-over' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById('fileInput').click()}
          >
            <input
              id="fileInput"
              type="file"
              accept="video/*,image/*"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
            {selectedFile ? (
              <div>
                <p>📁 {selectedFile.name}</p>
                <p style={{ fontSize: '14px', color: '#666' }}>
                  {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                </p>
                {!uploadedMedia && (
                  <button 
                    className="btn btn-primary" 
                    onClick={(e) => { e.stopPropagation(); handleUpload(); }}
                    disabled={loading}
                    style={{ marginTop: '10px', width: 'auto', padding: '10px 30px' }}
                  >
                    {loading ? 'Uploading...' : 'Upload'}
                  </button>
                )}
              </div>
            ) : (
              <div>
                <p style={{ fontSize: '48px', margin: '0' }}>☁️</p>
                <p>Drag & drop your media here or click to browse</p>
                <p style={{ fontSize: '14px', color: '#666' }}>
                  Supports videos and images up to 500MB
                </p>
              </div>
            )}
          </div>

          {uploadedMedia && (
            <div style={{ marginTop: '20px', textAlign: 'center' }}>
              <p>✅ Media uploaded successfully!</p>
            </div>
          )}
        </div>

        {uploadedMedia && (
          <>
            <div className="section">
              <h2>✏️ Post Details</h2>
              <div className="post-form">
                <div className="form-group">
                  <label>Title</label>
                  <input
                    type="text"
                    value={postForm.title}
                    onChange={(e) => setPostForm({ ...postForm, title: e.target.value })}
                    placeholder="Enter a catchy title"
                  />
                </div>
                <div className="form-group">
                  <label>Description</label>
                  <textarea
                    value={postForm.description}
                    onChange={(e) => setPostForm({ ...postForm, description: e.target.value })}
                    placeholder="Describe your content"
                    rows="4"
                    style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '2px solid #e0e0e0' }}
                  />
                </div>
                <div className="form-group">
                  <label>Tags (comma-separated)</label>
                  <input
                    type="text"
                    value={postForm.tags}
                    onChange={(e) => setPostForm({ ...postForm, tags: e.target.value })}
                    placeholder="viral, trending, funny"
                  />
                </div>
              </div>
            </div>

            <div className="section">
              <h2>🌐 Select Platforms</h2>
              <div className="platforms-grid">
                {AVAILABLE_PLATFORMS.map(platform => {
                  const isConnected = connectedPlatforms.includes(platform.id);
                  const isSelected = selectedPlatforms.includes(platform.id);
                  
                  return (
                    <div
                      key={platform.id}
                      className={`platform-card ${isConnected ? 'connected' : ''} ${isSelected ? 'selected' : ''}`}
                      onClick={() => {
                        if (isConnected) {
                          togglePlatform(platform.id);
                        } else {
                          connectPlatform(platform.id);
                        }
                      }}
                    >
                      <div className="platform-icon">{platform.icon}</div>
                      <div className="platform-name">{platform.name}</div>
                      <div className="platform-status">
                        {isConnected ? (
                          <>
                            <input
                              type="checkbox"
                              checked={isSelected}
                              onChange={() => {}}
                              className="checkbox"
                            />
                            {isSelected ? 'Selected' : 'Connected'}
                          </>
                        ) : (
                          'Click to connect'
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>

              <button
                className="btn btn-primary"
                onClick={handlePublish}
                disabled={loading || selectedPlatforms.length === 0}
                style={{ marginTop: '30px' }}
              >
                {loading ? '🚀 Publishing...' : `🚀 Publish to ${selectedPlatforms.length} Platform${selectedPlatforms.length !== 1 ? 's' : ''}`}
              </button>
            </div>
          </>
        )}

        <div className="section">
          <h2>📊 Recent Posts</h2>
          {posts.length === 0 ? (
            <p style={{ color: '#666', textAlign: 'center', padding: '40px' }}>
              No posts yet. Upload and publish your first content!
            </p>
          ) : (
            <div className="posts-list">
              {posts.map(post => (
                <div key={post.id} className="post-item">
                  <div className="post-header">
                    <div>
                      <strong>{post.title || 'Untitled Post'}</strong>
                      <p style={{ margin: '5px 0', color: '#666', fontSize: '14px' }}>
                        {post.description || 'No description'}
                      </p>
                    </div>
                    <span className={`post-status ${getStatusClass(post.status)}`}>
                      {post.status.toUpperCase()}
                    </span>
                  </div>
                  
                  {post.platform_posts && post.platform_posts.length > 0 && (
                    <div className="platform-results">
                      <strong style={{ fontSize: '14px' }}>Platform Results:</strong>
                      {post.platform_posts.map((pp, idx) => (
                        <div key={idx} className="platform-result">
                          <span className="platform-result-icon">
                            {pp.status === 'success' ? '✅' : pp.status === 'failed' ? '❌' : '⏳'}
                          </span>
                          <span>{pp.platform}: {pp.status}</span>
                          {pp.platform_url && (
                            <a href={pp.platform_url} target="_blank" rel="noopener noreferrer" style={{ marginLeft: '10px' }}>
                              View
                            </a>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
