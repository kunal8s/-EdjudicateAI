# 🚀 Edjudicate AI - Streamlit Cloud Deployment Guide

## 📋 Prerequisites

Before deploying to Streamlit Cloud, ensure you have:

1. **GitHub Account** - For hosting the repository
2. **Streamlit Cloud Account** - For deployment
3. **Google Gemini API Key** - For AI functionality
4. **Backend Server** (Optional) - For full functionality

## 🎯 Deployment Steps

### Step 1: Prepare Your Repository

1. **Fork/Clone** this repository to your GitHub account
2. **Ensure** all files are committed and pushed to GitHub
3. **Verify** the following files exist in your repository:
   - `streamlit_app.py` - Main Streamlit application
   - `requirements.txt` - Python dependencies
   - `packages.txt` - System dependencies
   - `.streamlit/config.toml` - Streamlit configuration

### Step 2: Set Up Streamlit Cloud

1. **Visit** [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with your GitHub account
3. **Click** "New app"
4. **Select** your repository and branch
5. **Set** the main file path to: `streamlit_app.py`

### Step 3: Configure Environment Variables

In your Streamlit Cloud app settings, add these environment variables:

#### Required Variables

```bash
# Google Gemini API Key (Required)
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

#### Optional Variables

```bash
# Backend API URL (Optional - for full functionality)
API_URL=https://your-backend-url.com
```

### Step 4: Deploy

1. **Click** "Deploy!" in Streamlit Cloud
2. **Wait** for the deployment to complete
3. **Access** your app at the provided URL

## 🔧 Configuration Files

### `streamlit_app.py`

This is the main application file that Streamlit Cloud will run. It includes:

- ✅ Modern dark theme with gradients
- ✅ Neumorphic card design
- ✅ Error handling for connection issues
- ✅ Environment variable support
- ✅ Responsive design

### `requirements.txt`

Contains all Python dependencies needed for the application:

```txt
# Core dependencies
streamlit>=1.47.1
requests>=2.31.0
google-generativeai>=0.8.5
sentence-transformers>=5.0.0
faiss-cpu>=1.11.0.post1
# ... and more
```

### `packages.txt`

System-level dependencies for document processing:

```txt
# For PDF processing
poppler-utils

# For document processing
tesseract-ocr
tesseract-ocr-eng

# For image processing
libgl1-mesa-glx
libglib2.0-0
```

### `.streamlit/config.toml`

Streamlit configuration for deployment:

```toml
[global]
developmentMode = false

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#6366f1"
backgroundColor = "#0f0f23"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#f1f5f9"
```

## 🌐 Backend Deployment (Optional)

For full functionality, you may want to deploy the backend separately:

### Option 1: Heroku

1. **Create** a new Heroku app
2. **Connect** your GitHub repository
3. **Set** buildpack to Python
4. **Add** environment variables
5. **Deploy** using the `Procfile`

### Option 2: Railway

1. **Connect** your GitHub repository to Railway
2. **Set** environment variables
3. **Deploy** automatically

### Option 3: Render

1. **Create** a new Web Service
2. **Connect** your GitHub repository
3. **Set** build command and start command
4. **Deploy**

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: Module not found errors
**Solution**: Ensure all dependencies are in `requirements.txt`

#### 2. API Key Issues

**Problem**: Gemini API not working
**Solution**: Verify `GEMINI_API_KEY` is set correctly in Streamlit Cloud

#### 3. Connection Errors

**Problem**: Can't connect to backend
**Solution**: 
- Ensure backend is deployed and accessible
- Check `API_URL` environment variable
- Verify CORS settings

#### 4. File Upload Issues

**Problem**: Files not uploading
**Solution**:
- Check file size limits
- Verify file types (PDF, DOCX)
- Ensure proper permissions

### Debug Mode

To enable debug mode locally:

```bash
# Set environment variable
export STREAMLIT_SERVER_HEADLESS=false

# Run with debug
streamlit run streamlit_app.py --logger.level=debug
```

## 📊 Monitoring

### Streamlit Cloud Analytics

- **View** app analytics in Streamlit Cloud dashboard
- **Monitor** usage and performance
- **Check** error logs

### Custom Monitoring

Add custom logging to track usage:

```python
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log important events
logger.info("User uploaded documents")
logger.info("AI query processed")
```

## 🔄 Updates and Maintenance

### Updating the App

1. **Make** changes to your local repository
2. **Commit** and push to GitHub
3. **Streamlit Cloud** will automatically redeploy

### Environment Variable Updates

1. **Go** to Streamlit Cloud dashboard
2. **Edit** environment variables
3. **Redeploy** the app

## 📞 Support

For deployment issues:

1. **Check** Streamlit Cloud documentation
2. **Review** error logs in Streamlit Cloud dashboard
3. **Verify** all configuration files are correct
4. **Test** locally before deploying

## 🎉 Success!

Once deployed, your Edjudicate AI app will be available at:
`https://your-app-name.streamlit.app`

The app features:
- ✅ Modern dark theme interface
- ✅ Document upload and processing
- ✅ AI-powered question answering
- ✅ Professional styling and animations
- ✅ Responsive design for all devices

Happy deploying! 🚀
