import os
import requests
from flask import Flask, Response, request

app = Flask(__name__)
SERVICES = {'courses': os.getenv('COURSE_SERVICE_URL', 'http://localhost:5001'), 'students': os.getenv('STUDENT_SERVICE_URL', 'http://localhost:5002')}
@app.route('/api/<service>/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@app.route('/api/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy(service, path):
    upstream = SERVICES.get(service)
    if not upstream: return {'error': 'Unknown service'}, 404
    target = f'{upstream}/api/{service}/' + path
    try:
        result = requests.request(request.method, target, params=request.args, data=request.get_data(), headers={'Content-Type': request.content_type or 'application/json'}, timeout=5)
    except requests.ConnectionError: return {'error': f'{service.title()} Service is unavailable'}, 503
    return Response(result.content, status=result.status_code, content_type=result.headers.get('Content-Type'))
if __name__ == '__main__': app.run(port=5000, debug=True)
