# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from molbio import test, driver
import traceback

# Initialize Flask app
app = Flask(__name__)

# Enable Cross Origin Resource Sharing (CORS)
CORS(app)

@app.route('/reverse', methods=['POST'])
def process_data():
    """
    Process incoming data, route to be triggered with HTTP POST.
    Expected data: JSON object with a key 'input'.
    """
    try:
        # Extract data from request
        data = request.get_json()
        user_input = data.get('input', '')

        # Log received data and user input
        app.logger.info(f"Received data: {data}")
        app.logger.info(f"User input: {user_input}")

        # Process the user input through molbio.py's driver function
        processed_data = test(user_input)

        # Log the processed data and another informative log
        app.logger.info(f"Processed data: {processed_data}")

        # Return processed data wrapped in a JSON response
        return jsonify({'result': processed_data})

    except Exception as e:
        # Print the stack trace of the exception
        traceback.print_exc()

        # Log the error message
        error_message = f"An error occurred: {str(e)}"
        app.logger.error(error_message)

        # Return error message wrapped in a JSON response with HTTP status code 500
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    # Run the Flask app on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000)
