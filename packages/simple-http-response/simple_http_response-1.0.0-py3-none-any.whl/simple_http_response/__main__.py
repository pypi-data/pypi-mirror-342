from simple_http_response import create_app
from waitress import serve


def main():
    """Serve the Flask application using Waitress."""
    app = create_app()
    host, port = app.config['HOST'], app.config['PORT']
    serve(app, host=host, port=port)


if __name__ == '__main__':
    main()