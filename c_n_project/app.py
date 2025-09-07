from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from dotenv import load_dotenv
from agents import MultiAgentOrchestrator
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

orchestrator = MultiAgentOrchestrator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_symptoms():
    try:
        symptoms = request.form.get('symptoms', '').strip()
        age = request.form.get('age', '').strip()
        chronic_conditions = request.form.get('chronic_conditions', '').strip()
        
        if not symptoms:
            return render_template('result.html', 
                                 error="Please enter your symptoms to continue.",
                                 results=None)
        
        age_int = None
        if age:
            try:
                age_int = int(age)
                if age_int < 0 or age_int > 150:
                    raise ValueError("Invalid age range")
            except ValueError:
                return render_template('result.html', 
                                     error="Please enter a valid age (0-150).",
                                     results=None)
        
        results = orchestrator.process_symptoms(
            user_input=symptoms,
            age=age_int,
            chronic_conditions=chronic_conditions if chronic_conditions else None
        )
        
        if not results.get('processing_success', False):
            return render_template('result.html', 
                                 error=f"Analysis failed: {results.get('error_message', 'Unknown error')}",
                                 results=None)
        
        return render_template('result.html', error=None, results=results)
        
    except Exception as e:
        app.logger.error(f"Error in analyze_symptoms: {e}")
        return render_template('result.html', 
                             error="An unexpected error occurred. Please try again.",
                             results=None)

@app.route('/api/analyze', methods=['POST'])
def api_analyze_symptoms():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        symptoms = data.get('symptoms', '').strip()
        age = data.get('age')
        chronic_conditions = data.get('chronic_conditions', '').strip()
        
        if not symptoms:
            return jsonify({
                'success': False,
                'error': 'Symptoms are required'
            }), 400
        
        age_int = None
        if age:
            try:
                age_int = int(age)
                if age_int < 0 or age_int > 150:
                    raise ValueError("Invalid age range")
            except (ValueError, TypeError):
                return jsonify({
                    'success': False,
                    'error': 'Please provide a valid age (0-150)'
                }), 400
        
        results = orchestrator.process_symptoms(
            user_input=symptoms,
            age=age_int,
            chronic_conditions=chronic_conditions if chronic_conditions else None
        )
        
        if not results.get('processing_success', False):
            return jsonify({
                'success': False,
                'error': results.get('error_message', 'Analysis failed')
            }), 500
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        app.logger.error(f"Error in API analyze_symptoms: {e}")
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred'
        }), 500

@app.route('/api/status')
def api_status():
    try:
        agent_status = orchestrator.get_agent_status()
        return jsonify({
            'success': True,
            'status': 'healthy',
            'agents': agent_status,
            'groq_api_available': agent_status['mapper_agent']['groq_available']
        })
    except Exception as e:
        app.logger.error(f"Error in status check: {e}")
        return jsonify({
            'success': False,
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', 
                         error_code=404,
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', 
                         error_code=500,
                         error_message="Internal server error"), 500

@app.template_filter('format_list')
def format_list(value):
    if isinstance(value, list):
        return ', '.join(str(item) for item in value)
    return str(value)

@app.template_filter('format_confidence')
def format_confidence(value):
    try:
        return f"{float(value) * 100:.1f}%"
    except (ValueError, TypeError):
        return "N/A"

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    print("=" * 50)
    print("Healthcare Multi-Agent Symptom Checker")
    print("=" * 50)
    print(f"Starting server on port {port}")
    print(f"Debug mode: {debug_mode}")
    print(f"Groq API available: {bool(os.getenv('GROQ_API_KEY'))}")
    print("=" * 50)
    
    app.run(host='127.0.0.1', port=5000, debug=debug_mode)
