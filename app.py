from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder="static")



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        method = request.form['method']
        if file:
            # Read the contents of the file
            file_contents = file.read().decode('utf-8')
            return render_template('index.html', text=file_contents, method=method)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



