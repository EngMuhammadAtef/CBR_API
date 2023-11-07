from flask import Flask, jsonify, request
import CBR

app = Flask(__name__)


@app.route('/nationalId=<nationalId>', methods = ['GET', 'POST']) 
def home(nationalId):
    try:
        if request.method == 'GET':
            users_id, users_scores = CBR.get_recomendation(str(nationalId))
            res = []
            for (id, score) in zip(users_id, users_scores):
                res.append({'nationalId': id, 'score': score})
            return jsonify(res)
    
    except:
        return jsonify()


if __name__ == '__main__':
    app.run(debug = True)