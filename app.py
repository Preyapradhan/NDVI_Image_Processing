from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from ndvi_processor import process_ndvi_change

app = Flask(__name__)
UPLOAD_FOLDER = 'static/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'tif', 'tiff'}

def clear_output_folder():
    """Clear the contents of the output folder."""
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def allowed_file(filename):
    """Check if the file has one of the allowed extensions."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if all four files are uploaded
        if 'b4_2014' not in request.files or 'b5_2014' not in request.files \
                or 'b4_2019' not in request.files or 'b5_2019' not in request.files:
            return render_template('index.html', error_message='Please upload all four files.')

        b4_2014 = request.files['b4_2014']
        b5_2014 = request.files['b5_2014']
        b4_2019 = request.files['b4_2019']
        b5_2019 = request.files['b5_2019']

        # Check file types
        if not (allowed_file(b4_2014.filename) and allowed_file(b5_2014.filename)
                and allowed_file(b4_2019.filename) and allowed_file(b5_2019.filename)):
            return render_template('index.html', error_message='File type not allowed.')

        try:
            clear_output_folder()

            # Save files with their respective years
            b4_2014_filename = secure_filename(b4_2014.filename)
            b5_2014_filename = secure_filename(b5_2014.filename)
            b4_2019_filename = secure_filename(b4_2019.filename)
            b5_2019_filename = secure_filename(b5_2019.filename)

            b4_2014_path = os.path.join(app.config['UPLOAD_FOLDER'], 'B4_2014.tif')
            b5_2014_path = os.path.join(app.config['UPLOAD_FOLDER'], 'B5_2014.tif')
            b4_2019_path = os.path.join(app.config['UPLOAD_FOLDER'], 'B4_2019.tif')
            b5_2019_path = os.path.join(app.config['UPLOAD_FOLDER'], 'B5_2019.tif')

            b4_2014.save(b4_2014_path)
            b5_2014.save(b5_2014_path)
            b4_2019.save(b4_2019_path)
            b5_2019.save(b5_2019_path)

            ndvi_2014_path = os.path.join(app.config['UPLOAD_FOLDER'], 'NDVI_2014.tif')
            ndvi_2019_path = os.path.join(app.config['UPLOAD_FOLDER'], 'NDVI_2019.tif')
            ndvi_change_path = os.path.join(app.config['UPLOAD_FOLDER'], 'NDVIChange.tif')
            ndvi_change_image = os.path.join(app.config['UPLOAD_FOLDER'], 'NDVIChange.png')

            process_ndvi_change(b4_2014_path, b5_2014_path, b4_2019_path, b5_2019_path,
                                ndvi_2014_path, ndvi_2019_path, ndvi_change_path, ndvi_change_image)

            ndvi_2014_png = url_for('static', filename='output/NDVI_2014.png')
            ndvi_2019_png = url_for('static', filename='output/NDVI_2019.png')
            return render_template('index.html', ndvi_2014_png=ndvi_2014_png, ndvi_2019_png=ndvi_2019_png,
                                   ndvi_2014_year='2014', ndvi_2019_year='2019')

        except Exception as e:
            print('Error processing images:', e)
            return render_template('index.html', error_message='Failed to process images.')

    # Render the index template with the Clear Files button
    return render_template('index.html')

@app.route('/result')
def result():
    ndvi_change_png = url_for('static', filename='output/NDVIChange.png')
    return render_template('result.html', ndvi_change_png=ndvi_change_png)

@app.route('/clear', methods=['POST'])
def clear_files():
    """Route to handle clearing all files in the output folder."""
    clear_output_folder()
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
