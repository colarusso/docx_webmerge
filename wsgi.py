import sys

path = 'docxmerge/' # path to docxmerge.py
if path not in sys.path:
    sys.path.append(path)

from cgi import parse_qs, escape
import docxmerge

def application(environ, start_response):
    if environ.get('PATH_INFO') == '/':
        status = '200 OK'

        # h/t http://wsgi.tutorial.codepoint.net/parsing-the-request-get
        d = parse_qs(environ['QUERY_STRING'])

        # Or if you want POST: comment out above, uncomment below. h/t http://wsgi.tutorial.codepoint.net/parsing-the-request-post
        #try:
        #    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        #except (ValueError):
        #    request_body_size = 0
        #request_body = environ['wsgi.input'].read(request_body_size)
        #d = parse_qs(request_body)

        docx_uri = d.get('docx_uri', [''])[0] # Returns the first value
        json_doc = d.get('json_doc', [''])[0] # Returns the first value
        filename = d.get('name', [''])[0] # Returns the first value

        # Always escape user input to avoid script injection
        docx_uri = escape(docx_uri)
        json_doc = escape(json_doc)
        filename = escape(filename)

        location, content = docxmerge.docx_run(docx_uri,json_doc,filename)
    else:
        status = '404 NOT FOUND'
        content = 'Page not found.'

    if location == '':
        response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
        start_response(status, response_headers)
        yield content.encode('utf8')
    else:
        start_response('302 Found', [('Location',location)])
