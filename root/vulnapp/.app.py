from flask import Flask, request, send_file, abort, render_template
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web_root', 'templates'))

# Base directory for the application
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))  # Path where app.py is located
FILES_DIRECTORY = os.path.join(BASE_DIRECTORY, 'web_root', 'files')  # Path to the files directory
BIN_DIRECTORY = os.path.join(BASE_DIRECTORY, 'bin')  # Path to the bin directory

@app.route('/')
def index():
    hint = "Try looking for 'flag.txt' or 'decoy1.txt' as a file to download!"
    
    # Get list of files from the files directory
    files = os.listdir(FILES_DIRECTORY) + os.listdir(BIN_DIRECTORY)  # Include files from bin
    
    return render_template('index.html', hint=hint, files=files)

@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('file')
    
    if filename is None:
        abort(400, description="Missing 'file' parameter")

    # Construct the path for flag.txt in the base directory
    if filename == 'flag.txt':  # Allow access to flag.txt directly
        flag_path = os.path.join(BASE_DIRECTORY, 'flag.txt')
        if os.path.exists(flag_path):
            return send_file(flag_path)

    # Construct the path for files in the files directory
    file_path_files = os.path.abspath(os.path.join(FILES_DIRECTORY, filename))
    file_path_bin = os.path.abspath(os.path.join(BIN_DIRECTORY, filename))

    print(f"Requested file path (files): {file_path_files}")
    print(f"Requested file path (bin): {file_path_bin}")

    # Validate the file path to restrict access and ensure it's not a directory
    if file_path_files.startswith(FILES_DIRECTORY) and os.path.exists(file_path_files) and not os.path.isdir(file_path_files):
        return send_file(file_path_files)
    elif file_path_bin.startswith(BIN_DIRECTORY) and os.path.exists(file_path_bin) and not os.path.isdir(file_path_bin):
        return send_file(file_path_bin)

    abort(404, description="File not found or access denied")

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)  # You can use 403 for access denied
def access_denied(e):
    return render_template('access_denied.html'), 403

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
