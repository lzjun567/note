Flask之Hello world 详解
========================
以下讲解假设你对python有基本了解,熟悉wsgi,以及了解某种python web framework.  

    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        return "HELLO WROLD"
    
    if __name__ == '__main__':
        app.run(debug=True)

