# HackRx API - Document Q&A System

This is the API version of the EdjudicateAI system, designed to meet the HackRx competition requirements. The API processes documents from URLs and answers questions using AI-powered document analysis.

## 🚀 Features

- **Document Processing**: Supports PDF and DOCX files from URLs
- **AI-Powered Q&A**: Uses Gemini 2.0 Flash for intelligent document analysis
- **Vector Search**: FAISS-based semantic search for relevant document chunks
- **RESTful API**: Standard HTTP endpoints with JSON request/response
- **Authentication**: Bearer token authentication
- **Production Ready**: Configurable for various deployment platforms

## 📋 API Endpoints

### Main Endpoint: `/hackrx/run`

**Method**: `POST`  
**Authentication**: `Bearer <api_key>`  
**Content-Type**: `application/json`

#### Request Format
```json
{
    "documents": "https://example.com/policy.pdf",
    "questions": [
        "What is the grace period for premium payment?",
        "What is the waiting period for pre-existing diseases?",
        "Does this policy cover maternity expenses?"
    ]
}
```

#### Response Format
```json
{
    "answers": [
        "A grace period of thirty days is provided for premium payment...",
        "There is a waiting period of thirty-six months...",
        "Yes, the policy covers maternity expenses..."
    ]
}
```

### Health Check: `/health`

**Method**: `GET`  
**Authentication**: None

Returns API health status.

## 🛠️ Local Development

### Prerequisites

- Python 3.8+
- pip3

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AdjudicateAI/VeriSure-AI-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

4. **Run the API locally**
   ```bash
   python api_app.py
   ```

5. **Test the API**
   ```bash
   python test_api.py
   ```

The API will be available at `http://localhost:8000`

## 🚀 Deployment

### Quick Deployment Script

Use the provided deployment script for easy deployment:

```bash
# Make script executable
chmod +x deploy_api.sh

# Test locally
./deploy_api.sh local

# Deploy to Heroku
GEMINI_API_KEY=your_key ./deploy_api.sh heroku

# Deploy to Railway
./deploy_api.sh railway

# Get Render instructions
./deploy_api.sh render
```

### Manual Deployment

#### Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create and deploy**
   ```bash
   heroku create your-app-name
   heroku config:set GEMINI_API_KEY=your_api_key
   git push heroku main
   ```

#### Railway

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and deploy**
   ```bash
   railway login
   railway up
   ```

#### Render

1. Go to [Render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api_app:app -c gunicorn.conf.py`
   - **Environment Variable**: `GEMINI_API_KEY=your_api_key`
5. Deploy

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `PORT`: Server port (default: 8000)
- `WEB_CONCURRENCY`: Number of worker processes (default: auto)

### API Authentication

The API accepts any Bearer token for authentication. You can modify the `verify_token` function in `api_app.py` to implement specific token validation.

## 📊 Performance

- **Response Time**: < 30 seconds for typical requests
- **Document Size**: Supports documents up to 50MB
- **Concurrent Requests**: Configurable via `WEB_CONCURRENCY`
- **Memory Usage**: Optimized for cloud deployment

## 🧪 Testing

### Test with Sample Data

```bash
python test_api.py
```

### Manual Testing with curl

```bash
curl -X POST "https://your-api-url.com/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
      "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
      "What is the waiting period for pre-existing diseases (PED) to be covered?"
    ]
  }'
```

## 📝 Submission for HackRx

### Webhook URL Format

Your webhook URL should be in the format:
```
https://your-domain.com/hackrx/run
```

### Pre-Submission Checklist

- [ ] API is live and accessible
- [ ] HTTPS enabled
- [ ] Handles POST requests to `/hackrx/run`
- [ ] Returns JSON response in correct format
- [ ] Response time < 30 seconds
- [ ] Tested with sample data
- [ ] Bearer token authentication working

### Example Submission

**Webhook URL**: `https://your-app.herokuapp.com/hackrx/run`

**Description**: `FastAPI + Gemini 2.0 Flash + FAISS vector search with RAG`

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**: Verify your Gemini API key is set correctly
   ```bash
   echo $GEMINI_API_KEY
   ```

3. **Memory Issues**: Reduce `WEB_CONCURRENCY` for smaller instances
   ```bash
   export WEB_CONCURRENCY=1
   ```

4. **Timeout Issues**: Increase timeout in gunicorn.conf.py for large documents

### Logs

Check application logs for detailed error information:

```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# Local
tail -f api.log
```

## 📚 Technical Details

### Architecture

- **FastAPI**: Modern, fast web framework
- **Gemini 2.0 Flash**: Google's latest AI model for text generation
- **FAISS**: Facebook's similarity search library
- **Sentence Transformers**: State-of-the-art sentence embeddings
- **PyMuPDF**: Fast PDF text extraction
- **python-docx**: DOCX file processing

### Document Processing Pipeline

1. **Download**: Fetch document from URL
2. **Extract**: Extract text content (PDF/DOCX)
3. **Chunk**: Split into manageable text chunks
4. **Embed**: Generate vector embeddings
5. **Index**: Build FAISS search index
6. **Query**: Semantic search for relevant chunks
7. **Generate**: AI-powered answer generation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs
3. Test with the provided test script
4. Create an issue in the repository

---

**Happy Hacking! 🚀**

