#! /usr/bin/env python
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

html = """
    <html>
    <body>
        <form method="post" action="application.py">
        <p>
            Age:<input type="text" name="age">
        </p>
        <p>
        Hobbies:
        <input name="hobbies" type="checkbox" value="software">Software
        <input name="hobbies" type="checkbox" value="tunning">Auto Tunning
        </p>
        <p>
        <input type="submit" value="Submit">
        </p>
    <p>
    Age:%s<br>
    Hobbies:%s
    </p>
    </body>
    </html>
    """

def application(environ, start_response):
    #response_body = "the request method was %s" % environ['REQUEST_METHOD']
    #response_body = response_body*1000
    #status = '200 OK'
    #response_headers = [('Content-Type', 'text/plain'),
    #                    ('Content-Length', str(len(response_body)))]

    #start_response(status, response_headers)
    #return [response_body]
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except:
        request_body_size = 0 

    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)

    age = d.get('age', [''])[0]
    hobbies = d.get('hobbies',[])

    age = escape(age)
    hobbies = [escape(hobby) for hobby in hobbies]

    response_body = html % (age or 'Empty',','.join(hobbies or ['No Hobbies']))
    status = '200 OK'
    response_headers = [('Content-Type','text/html'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]



class AppClass:

    def __call__(self, environ, start_reponse):
        status = "200 OK"
        response_header = [('Content_Type','text/plain'),]
        start_reponse(status, response_header)
        return ["hello world ok!"]

class Upperware(object):
    def __init__(self, app):
        self.wrapped_app = app
    def __call__(self,environ, start_response):
        for data in self.wrapped_app(environ, start_response):
            return data.upper()
        
httpd= make_server('localhost',
                    8051,
                    Upperware(AppClass()),
                    )

#httpd.handle_request()
httpd.serve_forever()
