
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from flask import Flask, flash, url_for, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
#folder path
UPLOAD_FOLDER = os.path.join('static','')

#import cosine similarity file
cos_df= pd.read_csv('data.csv')

# initalize REST API service
app= Flask(__name__, static_folder=os.path.abspath(UPLOAD_FOLDER))
app.config['FOLDER'] = UPLOAD_FOLDER
print(UPLOAD_FOLDER)

# Home page
@app.route('/',methods=['POST','GET'])
def home():
    return render_template("home.html")

#specify allowed extention files 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in 'jpg'


#Estore upload page
@app.route('/one.html', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            return redirect(url_for('recommend',filename=filename))
    return render_template('one.html')
    

#Recommendation page
@app.route('/two.html', methods=['POST','GET'])
def recommend():
    
    query_image =request.args.get('filename')
    print(query_image)
    print(cos_df.shape)
    top_5= cos_df.sort_values(query_image,ascending=False).iloc[1:6]
    top_5= top_5.loc[:,['user_image',query_image]]
    pred_im= list(top_5['user_image'])
    acc_im=list(top_5[query_image])
    print("Select  Image: ",query_image)
    print('--------------')
    print(top_5)
    return render_template('two.html', query_image=query_image, reco_image=pred_im, acc_image=acc_im)

# Run the API
if __name__ == '__main__':
    app.run()
