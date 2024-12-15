from flask import Flask,request
from flask_cors import CORS
from easytext.identify_en import identify_complex_conponent_en_bf
from utils.para import get_para_structure
from easytext.simplify_en import get_simplify
app = Flask(__name__)
CORS(app)
def s2toint(s2):
    num = int(s2)
    if (num <= 1000):
        s2 = 4
    elif (num <= 2500):
        s2 = 3
    elif (num <= 3300):
        s2 = 2
    else:
        s2 = 1
    return s2
@app.route('/',methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        s1 = request.args.get('s1')
        s2 = request.args.get('s2')
        s2=s2toint(s2)
        data = get_para_structure(s1)
        for i in range(len(data)):
            data[i][0] = identify_complex_conponent_en_bf(data[i][0], s2)

    return data

@app.route('/router2', methods=['GET', 'POST'])
def simplify():
    if request.method == 'GET':
        s1 = request.args.get('s1')
        s2 = request.args.get('s2')
        s3 = request.args.get('s3')
        s2 = s2toint(s2)
        s3=int(s3)
        if(s3==2):
            if(s2!=1):
                s2=s2-1
        data = get_para_structure(s1)
        for i in range(len(data)):
            data[i] = get_simplify(data[i], s2)

    return data


if __name__ == '__main__':
    app.run(debug=True)
