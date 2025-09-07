# Healthcare Multi-Agent Symptom Checker

A sophisticated web application that uses multiple AI agents to analyze symptoms and provide medical insights. Built with Python Flask backend and modern web technologies.

## 🎯 Problem Statement

Many people experience symptoms but struggle to understand what they might indicate or when to seek medical help. Traditional symptom checkers often provide generic advice without considering the complexity of symptom interactions or the urgency of different conditions.

HealthCheck AI addresses this challenge by using a sophisticated multi-agent system that analyzes symptoms from multiple perspectives, providing more accurate and actionable health insights.

## 🤖 Multi-Agent Workflow

Our system employs three specialized AI agents working in coordination:

### 1. Symptom Analyzer Agent
- **Purpose**: Parses and normalizes user input from free-text descriptions
- **Capabilities**:
  - Natural language processing of symptom descriptions
  - Symptom normalization and standardization
  - Severity detection from user language
  - Duration and onset pattern extraction
  - Confidence scoring for analysis quality

### 2. Condition Mapper Agent
- **Purpose**: Maps normalized symptoms to potential medical conditions
- **Capabilities**:
  - Rule-based condition matching using medical knowledge base
  - AI-enhanced analysis via Groq API (when available)
  - Confidence scoring and condition ranking
  - Fallback to rule-based analysis if API unavailable

### 3. Medical Advisor Agent
- **Purpose**: Provides medical advice and detects emergency situations
- **Capabilities**:
  - Emergency symptom detection and alerts
  - Treatment and medicine recommendations
  - Self-care guidance
  - "When to seek help" recommendations
  - Red flag identification for serious conditions
 
### 4. MultiAgentOrchestrator:
- **Purpose**: Coordinates the workflow between all agents to produce cohesive symptom analysis results.
- **Capabilities**:
  - Manages the interaction between AnalyzerAgent, ConditionMapperAgent, and AdvisorAgent
  - Ensures agents operate independently but collaborate for final output
  - Handles data passing and aggregation of results from all agents
  - Provides a single interface (process_symptoms) for the Flask app or API endpoints
  - Maintains agent status for debugging and health checks

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - Web framework for API development
- **LangChain** - Agent orchestration and workflow management
- **python-dotenv** - Environment variable management
- **requests** - HTTP client for API calls

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS Grid and Flexbox
- **JavaScript (ES6+)** - Interactive functionality
- **Font Awesome** - Icons and visual elements
- **Google Fonts (Inter)** - Typography

### AI & APIs
- **Groq API** - LLM enhancement for symptom analysis
- **Mixtral-8x7B** - High-performance language model
- **JSON Knowledge Base** - Comprehensive medical condition database

### Infrastructure
- **Environment Variables** - Secure configuration management
- **RESTful API** - Clean API design for frontend-backend communication
- **Responsive Design** - Mobile-first approach

## 🧠 LLM Selection: Groq API with Mixtral-8x7B

We selected Groq's Mixtral-8x7B model for several key reasons:

- **⚡ Speed**: Ultra-fast inference for real-time symptom analysis
- **🎯 Accuracy**: Exceptional performance in medical text understanding
- **💰 Cost-Effective**: Efficient pricing model for educational applications
- **🔄 Reliability**: Consistent performance with medical terminology
- **🛡️ Fallback**: Graceful degradation to rule-based analysis when unavailable

## 📊 Knowledge Base

Our comprehensive medical knowledge base includes:

- **22+ Medical Conditions** - From common colds to emergency conditions
- **150+ Symptoms** - Mapped and normalized symptom database
- **100+ Treatment Options** - OTC, prescription, and natural remedies
- **12 Emergency Indicators** - Critical symptoms requiring immediate attention

### Condition Categories:
- **Mild**: Common cold, tension headache, allergic rhinitis
- **Moderate**: Flu, migraine, UTI, bronchitis, anxiety, depression
- **Serious**: Hypertension, diabetes, asthma, pneumonia
- **Emergency**: Heart attack, stroke, appendicitis, severe allergic reactions

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd c_n_project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Getting a Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

**Note**: The application works without the Groq API key, falling back to rule-based analysis.

## 🖥️ Usage

### Web Interface

1. **Enter Symptoms**: Describe your symptoms in natural language
2. **Optional Information**: Add age and chronic conditions for better analysis
3. **Get Analysis**: Receive comprehensive symptom analysis
4. **Review Results**: 
   - Parsed and normalized symptoms
   - Potential medical conditions with confidence scores
   - Treatment recommendations
   - Emergency alerts (if applicable)
   - When to seek medical help

### API Endpoints

#### Analyze Symptoms
```bash
POST /api/analyze
Content-Type: application/json

{
  "symptoms": "I have a severe headache and feel nauseous",
  "age": 35,
  "chronic_conditions": "hypertension"
}
```

#### Check System Status
```bash
GET /api/status
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for LLM enhancement | None (optional) |
| `FLASK_ENV` | Flask environment | development |
| `FLASK_DEBUG` | Enable debug mode | True |
| `PORT` | Server port | 5000 |

### Knowledge Base Customization

Edit `knowledge_base.json` to:
- Add new medical conditions
- Update symptom mappings
- Modify treatment recommendations
- Add emergency symptoms

## 🧪 Testing

### Manual Testing
1. Test with various symptom descriptions
2. Verify emergency detection works
3. Test responsive design on different devices

### Example Test Cases
- **Emergency**: "severe chest pain and difficulty breathing"
- **Common**: "runny nose, sneezing, and mild headache"
- **Complex**: "fatigue, joint pain, and skin rash for 2 weeks"

## 🚀 Deployment

### Local Development
```bash
python app.py
```


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes only. See LICENSE file for details.

## ⚠️ Medical Disclaimer

**IMPORTANT**: This application is for educational and demonstration purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read here.

### In Case of Emergency
**If you have a medical emergency, call 108/112 immediately!**

## 📞 Support

For technical support or questions:
- Create an issue in the repository
- Check the documentation
- Review the FAQ section

## 🔄 Version History

- **v1.0.0** - Initial release with multi-agent system
- **v1.1.0** - Added Groq API integration
- **v1.2.0** - Enhanced UI and mobile responsiveness
- **v1.3.0** - Improved emergency detection

## 🙏 Acknowledgments

- Medical knowledge base compiled from reputable medical sources
- UI/UX inspired by modern healthcare applications
- Community feedback and testing contributions

---

**Built with ❤️ for educational purposes**
