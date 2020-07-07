#!/usr/bin/env python3
import os
import json
import refpull
from flask import Flask, flash, request, redirect, url_for, \
        send_from_directory, render_template 
from werkzeug.utils import secure_filename


app = Flask(__name__)


UPLOAD_FOLDER      = os.path.join(os.getcwd(), "uploads")
ALLOWED_EXTENSIONS = ['.pdf']


app.config['UPLOAD_FOLDER']      = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
app.config['SECRET_KEY']         = "blahwhatever"


def allowed_file(filename):
    # Allow only files with .pdf extension
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        fhandle = request.files.get('file', '') 
        if not fhandle:
            flash('No file part')
            return redirect(request.url)

        if not fhandle.filename:
            flash('No selected file')
            return redirect(request.url)

        if allowed_file(fhandle.filename):
            filename = secure_filename(fhandle.filename)

            # Save the uploaded file to the upload folder
            local_fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            fhandle.save(local_fullpath)
            flash('File successfully uploaded')

            # Get refpull to do something we want it to do
            # raw_text = refpull.pdf_to_text(local_fullpath)
            # ref_text = refpull.pull_ref_text(raw_text)
            # reflist = refpull.text_to_list(ref_text)
            reflist = refpull.pdf_to_reflist(local_fullpath)

            # return render_template('results.html')
            return json.dumps(reflist)

            #return redirect(url_for('uploaded_file', filename=filename))

    return render_template('index.html') 


def main():
    app.run()


if __name__ == '__main__':
    main()
