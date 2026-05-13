from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import FileResponse, HttpResponse
from pathlib import Path
import mimetypes

@require_http_methods(["GET"])
def serve_frontend(request, path=''):
    """Serve React frontend for SPA routing and static assets"""
    base_dir = Path(__file__).resolve().parent.parent
    dist_dir = base_dir / 'frontend-app' / 'dist'
    staticfiles_dir = base_dir / 'staticfiles'
    
    # Get the requested path
    request_path = request.path.lstrip('/')
    
    # Try to serve from staticfiles (for assets collected by Django)
    requested_file = staticfiles_dir / request_path
    if requested_file.exists() and requested_file.is_file():
        # Guess the content type
        content_type, _ = mimetypes.guess_type(str(requested_file))
        with open(requested_file, 'rb') as f:
            return FileResponse(f, content_type=content_type)
    
    # Try to serve from dist directory directly (for development)
    if request_path.startswith('assets/'):
        requested_file = dist_dir / request_path.replace('assets/', '')
        if requested_file.exists() and requested_file.is_file():
            content_type, _ = mimetypes.guess_type(str(requested_file))
            with open(requested_file, 'rb') as f:
                return FileResponse(f, content_type=content_type)
    
    # Serve the index.html for SPA routing
    index_file = dist_dir / 'index.html'
    if index_file.exists():
        with open(index_file, 'r') as f:
            return HttpResponse(f.read(), content_type='text/html')
    
    # Fallback: create a minimal index.html if dist doesn't exist yet
    return HttpResponse('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Todos App</title>
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f5f5f5; }
            .container { text-align: center; }
            h1 { color: #333; }
            p { color: #666; }
            .warning { background-color: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 5px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Todos App</h1>
            <p>Frontend is loading...</p>
            <div class="warning">
                <p><strong>Note:</strong> Run `npm run build` in the frontend-app directory to build the frontend.</p>
            </div>
        </div>
    </body>
    </html>
    ''', content_type='text/html')


