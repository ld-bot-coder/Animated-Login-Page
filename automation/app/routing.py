from flask import Blueprint, request, jsonify, render_template
from app.pipeline import SearchPipeline
import logging

api_bp = Blueprint('api', __name__)
web_bp = Blueprint('web', __name__)

pipeline = SearchPipeline() # Singleton-ish for the worker, though standard Flask is sync.
                            # For true scale, this should be inside a queue worker, but for MVP it's direct.

@web_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@api_bp.route('/search', methods=['POST'])
def search_endpoint():
    """
    Unified Search Endpoint
    Payload: { "query": "Why is the sky blue?", "deep_mode": false }
    """
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' field"}), 400
        
    query = data['query']
    deep_mode = data.get('deep_mode', False)
    
    try:
        result = pipeline.run(query, deep_mode=deep_mode)
        return jsonify(result)
    except Exception as e:
        logging.error(f"Pipeline error: {e}", exc_info=True)
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "app": "GenSpark-Engine"}), 200
