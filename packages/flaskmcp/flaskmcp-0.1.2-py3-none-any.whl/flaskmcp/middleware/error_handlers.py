from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
import traceback
import sys

def register_error_handlers(app: Flask) -> None:
    """
    Register custom error handlers for the Flask application.
    
    Args:
        app: Flask application
    """
    @app.errorhandler(400)
    def bad_request(e):
        """Handle 400 Bad Request errors."""
        return jsonify({
            "error": "Bad Request",
            "message": str(e),
            "path": request.path
        }), 400
    
    @app.errorhandler(404)
    def not_found(e):
        """Handle 404 Not Found errors."""
        return jsonify({
            "error": "Not Found",
            "message": f"The requested resource was not found: {request.path}",
            "path": request.path
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        """Handle 405 Method Not Allowed errors."""
        return jsonify({
            "error": "Method Not Allowed",
            "message": f"The method {request.method} is not allowed for this resource",
            "path": request.path,
            "allowed_methods": e.valid_methods
        }), 405
    
    @app.errorhandler(500)
    def internal_server_error(e):
        """Handle 500 Internal Server Error errors."""
        # In debug mode, include the traceback
        if app.debug:
            trace = traceback.format_exc()
            return jsonify({
                "error": "Internal Server Error",
                "message": str(e),
                "path": request.path,
                "traceback": trace
            }), 500
        
        # In production, hide the details
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "path": request.path
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle all other HTTP exceptions."""
        response = e.get_response()
        response.data = jsonify({
            "error": e.name,
            "message": e.description,
            "path": request.path,
            "code": e.code
        }).data
        response.content_type = "application/json"
        return response
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle non-HTTP exceptions."""
        # Log the error
        app.logger.error(f"Unhandled exception: {str(e)}")
        app.logger.error(traceback.format_exc())
        
        # In debug mode, include the traceback
        if app.debug:
            trace = traceback.format_exc()
            return jsonify({
                "error": "Unhandled Exception",
                "message": str(e),
                "path": request.path,
                "traceback": trace,
                "type": type(e).__name__
            }), 500
        
        # In production, hide the details
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "path": request.path
        }), 500