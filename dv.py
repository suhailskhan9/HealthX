from flask import Flask,send_file,render_template
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
fig,ax=plt.subplots(figsize=(15,6))
ax=sns.set_style(style="darkgrid")
df=pd.read_csv("download.csv")
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('visualize.html')
@app.route('/dv1h')
def dv1h():
    return render_template('dv.html')
@app.route('/dv2h')
def dv2h():
    return render_template('dv2.html')
@app.route('/dv3h')
def dv3h():
    return render_template('dv3.html')
@app.route('/dv4h')
def dv4h():
    return render_template('dv4.html')
@app.route('/dv5h')
def dv5h():
    return render_template('dv5.html')



@app.route('/dv1')
def dv1():
    sns.countplot(data=df,y='disease',hue='Gender')
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')

@app.route('/dv2')
def dv2():
    sns.countplot(data=df,y=df['Year'].where(df['status'])=='death',hue='Gender')
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='img/png')

# @app.route('/dv3')
# def dv3():

# @app.route('/dv4')
# def dv4():

# @app.route('/dv5')
# def dv5():

# @app.route('/dv2')
# def dv1():
#     sns.countplot(data=df,y='disease',hue='Gender')
#     canvas=FigureCanvas(fig)
#     img=io.BytesIO()
#     fig.savefig(img)
#     img.seek(0)
#     return send_file(img,mimetype='img/png')
if __name__=="__main__":
    app.run()