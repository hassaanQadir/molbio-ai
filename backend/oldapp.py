# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from molbio import test, main

app = Flask(__name__)
CORS(app)

@app.route('/reverse', methods=['POST'])
def process_data():
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        user_input = data['input']
        print(f"User input: {user_input}")
        print("finding a pipette\n")
        # We send it to molbio.py
        processed_data = main(user_input)
        print(f"Processed data: {processed_data}")
        print("growing cells\n")
        return jsonify({'result': processed_data})
    except Exception as e:
        traceback.print_exc()
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return jsonify({'error': error_message}), 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
