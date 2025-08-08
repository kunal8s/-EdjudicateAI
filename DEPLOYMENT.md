# 🚀 EdjudicateAI Deployment Guide

This guide will help you deploy your EdjudicateAI application to the cloud so it can be accessed by users worldwide.

## 📋 Prerequisites

1. **Google Gemini API Key**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **GitHub Account**: For version control and deployment
3. **Streamlit Cloud Account**: Free hosting platform

## 🎯 Deployment Options

### Option 1: Streamlit Cloud (Recommended - Easiest)

#### Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/EdjudicateAI.git
   git push -u origin main
   ```

2. **Ensure these files are in your repository**:
   - `streamlit_app.py` (main application)
   - `requirements_deploy.txt` (dependencies)
   - `.streamlit/config.toml` (configuration)
   - `README.md` (documentation)

#### Step 2: Deploy to Streamlit Cloud

1. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
2. **Sign in with your GitHub account**
3. **Click "New app"**
4. **Configure your app**:
   - **Repository**: Select your EdjudicateAI repository
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL**: Choose a custom subdomain (optional)

5. **Add your API key**:
   - Click on your deployed app
   - Go to "Settings" → "Secrets"
   - Add your Gemini API key:
   ```toml
   GEMINI_API_KEY = "your-actual-gemini-api-key-here"
   ```

6. **Deploy**: Click "Deploy" and wait for the build to complete

#### Step 3: Test Your Deployment

1. **Visit your app URL** (e.g., `https://your-app-name.streamlit.app`)
2. **Upload a test PDF/DOCX file**
3. **Ask a question** to verify everything works

### Option 2: Railway (Alternative)

#### Step 1: Prepare for Railway

1. **Create a `railway.toml` file**:
   ```toml
   [build]
   builder = "nixpacks"
   
   [deploy]
   startCommand = "streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0"
   healthcheckPath = "/"
   healthcheckTimeout = 300
   ```

2. **Create a `Procfile`**:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

#### Step 2: Deploy to Railway

1. **Go to [Railway](https://railway.app/)**
2. **Connect your GitHub repository**
3. **Add environment variables**:
   - `GEMINI_API_KEY`: Your Gemini API key
4. **Deploy**

### Option 3: Heroku (Legacy)

#### Step 1: Prepare for Heroku

1. **Create a `Procfile`**:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `setup.sh`**:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   enableXsrfProtection = false\n\
   " > ~/.streamlit/config.toml
   ```

#### Step 2: Deploy to Heroku

1. **Install Heroku CLI**
2. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```
3. **Set environment variables**:
   ```bash
   heroku config:set GEMINI_API_KEY=your-api-key
   ```
4. **Deploy**:
   ```bash
   git push heroku main
   ```

## 🔧 Configuration

### Environment Variables

Set these in your deployment platform:

- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Custom Domain (Optional)

1. **Buy a domain** (e.g., from Namecheap, GoDaddy)
2. **Configure DNS** to point to your deployment URL
3. **Add custom domain** in your deployment platform settings

## 📊 Monitoring & Analytics

### Streamlit Cloud Analytics

- **Built-in analytics** in Streamlit Cloud dashboard
- **Usage statistics** and performance metrics
- **Error logs** and debugging information

### Custom Monitoring

Add these to your app for better monitoring:

```python
# Add to streamlit_app.py
import time

# Performance monitoring
start_time = time.time()
# ... your processing code ...
processing_time = time.time() - start_time
st.metric("Processing Time", f"{processing_time:.2f}s")
```

## 🔒 Security Considerations

### API Key Security

- ✅ **Never commit API keys** to your repository
- ✅ **Use environment variables** for sensitive data
- ✅ **Rotate API keys** regularly
- ❌ **Don't hardcode** API keys in your code

### File Upload Security

- ✅ **Validate file types** (PDF, DOCX only)
- ✅ **Limit file sizes** (50MB max)
- ✅ **Sanitize file names**
- ❌ **Don't trust user input**

### Data Privacy

- ✅ **Temporary file storage** (files are deleted after processing)
- ✅ **Session-based data** (data is isolated per session)
- ✅ **No persistent storage** of user documents

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check `requirements_deploy.txt` for missing dependencies
   - Verify Python version compatibility
   - Check for syntax errors in your code

2. **API Key Issues**:
   - Verify API key is correctly set in environment variables
   - Check API key permissions and quotas
   - Test API key locally first

3. **Memory Issues**:
   - Large files may cause memory problems
   - Consider chunking large documents
   - Monitor memory usage in deployment logs

4. **Performance Issues**:
   - Optimize embedding model loading with `@st.cache_resource`
   - Consider using smaller models for faster processing
   - Implement request queuing for high traffic

### Debug Commands

```bash
# Check deployment logs
streamlit logs

# Test locally with production settings
streamlit run streamlit_app.py --server.headless=true

# Check environment variables
echo $GEMINI_API_KEY
```

## 📈 Scaling Considerations

### For High Traffic

1. **Upgrade deployment plan** (Streamlit Cloud Pro, Railway Pro, etc.)
2. **Implement caching** for frequently accessed data
3. **Use CDN** for static assets
4. **Consider microservices** architecture

### Cost Optimization

1. **Monitor API usage** and costs
2. **Implement rate limiting**
3. **Use efficient models** (smaller embedding models)
4. **Cache results** to reduce API calls

## 🎉 Success!

Once deployed, your app will be accessible to users worldwide. Share your app URL and start helping people understand their insurance policies!

### Next Steps

1. **Add analytics** to track usage
2. **Implement user feedback** system
3. **Add more document types** support
4. **Create mobile app** version
5. **Add multi-language** support

---

**Need help?** Check the [Streamlit documentation](https://docs.streamlit.io/) or [community forums](https://discuss.streamlit.io/).
