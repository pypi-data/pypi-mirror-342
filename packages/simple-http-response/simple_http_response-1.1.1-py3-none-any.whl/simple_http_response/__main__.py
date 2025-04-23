from waitress import serve

from simple_http_response import app


def main():
    """Serve the Flask application using Waitress."""
    host, port = app.config['HOST'], app.config['PORT']
    serve(app, host=host, port=port)


if __name__ == '__main__':
    main()
