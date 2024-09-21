from flask import Flask, request, send_file, abort, render_template
import os

app = Flask(__name__)

# Directory to serve files from
BASE_DIRECTORY = './files'

@app.route('/')
def index():
    hint = "Try looking for 'flag.txt' as a file to download!"
    
    # Get list of files from the 'files' directory
    files = os.listdir(BASE_DIRECTORY)
    
    return render_template('index.html', hint=hint, files=files)

@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('file')
    
    if filename is None:
        abort(400, description="Missing 'file' parameter")
    
    # Construct the absolute path
    file_path = os.path.abspath(os.path.join(BASE_DIRECTORY, filename))
    
    print(f"Requested file path: {file_path}")

    # Serve the file if it exists
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        abort(404, description="File not found")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
