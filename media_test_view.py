from django.http import HttpResponse
from django.urls import path
from django.conf import settings
import os

def test_media_view(request):
    """A test view to verify media file serving."""
    filepath = os.path.join(settings.MEDIA_ROOT, 'corlee', 'uploads', 'felipe-santana-xJkTCbtuqAY-unsplash.webp')
    
    response = HttpResponse()
    response.write("<html><body>")
    response.write("<h1>Media Path Test</h1>")
    response.write(f"<p>MEDIA_URL: {settings.MEDIA_URL}</p>")
    response.write(f"<p>MEDIA_ROOT: {settings.MEDIA_ROOT}</p>")
    
    if os.path.exists(filepath):
        response.write(f"<p>File exists at: {filepath}</p>")
        file_url = settings.MEDIA_URL + 'corlee/uploads/felipe-santana-xJkTCbtuqAY-unsplash.webp'
        response.write(f"<p>File URL: {file_url}</p>")
        response.write(f"<p>Try accessing: <a href='{file_url}'>{file_url}</a></p>")
        response.write(f"<img src='{file_url}' width='300' />")
    else:
        response.write(f"<p>File does not exist at: {filepath}</p>")
    
    response.write("</body></html>")
    return response

urlpatterns = [
    path('media-test/', test_media_view, name='media-test'),
] 