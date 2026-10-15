#!/usr/bin/env python3
"""Small local proxy for the YouTube Data API. Keep API credentials server-side."""
import json, os, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API_KEY = os.environ.get('YOUTUBE_API_KEY', '').strip()
CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID', '').strip()

class Handler(BaseHTTPRequestHandler):
    def send_bytes(self, code, body, content_type):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == '/':
            self.send_bytes(200, (ROOT / 'index.html').read_bytes(), 'text/html; charset=utf-8')
            return
        if path == '/api/count':
            if not API_KEY or not CHANNEL_ID:
                self.send_bytes(503, json.dumps({'error':'Set YOUTUBE_API_KEY and YOUTUBE_CHANNEL_ID environment variables.'}).encode(), 'application/json')
                return
            params = urllib.parse.urlencode({'part':'snippet,statistics','id':CHANNEL_ID,'key':API_KEY})
            url = 'https://www.googleapis.com/youtube/v3/channels?' + params
            try:
                req = urllib.request.Request(url, headers={'User-Agent':'subscriber-counter-prototype/1.0'})
                with urllib.request.urlopen(req, timeout=12) as response:
                    payload = json.loads(response.read().decode('utf-8'))
                items = payload.get('items', [])
                if not items:
                    raise ValueError('No channel found. Check YOUTUBE_CHANNEL_ID and public visibility.')
                item = items[0]
                stats = item.get('statistics', {})
                if stats.get('hiddenSubscriberCount'):
                    raise ValueError('This channel hides its subscriber count.')
                result = {'title':item.get('snippet',{}).get('title','YouTube Channel'), 'subscriberCount':int(stats['subscriberCount'])}
                self.send_bytes(200, json.dumps(result).encode(), 'application/json; charset=utf-8')
            except Exception as exc:
                message = str(exc)
                self.send_bytes(502, json.dumps({'error':message[:300]}).encode(), 'application/json; charset=utf-8')
            return
        self.send_bytes(404, b'Not found', 'text/plain; charset=utf-8')

    def log_message(self, fmt, *args):
        # Avoid logging URLs containing credentials; API key is never included in request path to this server.
        print('%s - %s' % (self.address_string(), fmt % args))

if __name__ == '__main__':
    port = int(os.environ.get('PORT','8000'))
    print(f'Serving subscriber counter on 0.0.0.0:{port}')
    ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
