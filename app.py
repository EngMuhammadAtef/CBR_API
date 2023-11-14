# importing libraries
from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler

from models.OCR_script import get_nationalId
from recommendation_systems.CBR import get_recomendation, Update_All_Recommendations
from config.connection import connect_to_db


# inial flask object
app = Flask(__name__)

# connect to database
db = connect_to_db()


# get recomendation API
@app.route('/nationalId=<nationalId>') 
def home(nationalId):
    try:
        # get content-based recomendation for user content and other users' content
        users_nationalIDs, users_scores = get_recomendation(db, str(nationalId))
        
        # format IDs and Scores for API Server
        res = []
        for (id, score) in zip(users_nationalIDs, users_scores):
            res.append({'nationalId': id, 'score': score})
        return jsonify(res)
    
    except Exception as e:
        return jsonify({"error":str(e)})


# extract nationalId API
@app.route('/extract_nationalId', methods=['POST'])
def extract_nationalId():
    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return jsonify({'error': 'Empty file name'}), 400

        # extract nationalId from image
        nationalId = get_nationalId(file)
        return jsonify({'nationalId': nationalId})
    
    except Exception as e:
        return jsonify({"error":str(e)})


# run main file [app]
if __name__ == '__main__':
    # Update All Recommendations Job every 7 days
    scheduler = APScheduler()
    scheduler.add_job(id='Job 1', name='Update All Recommendations Job', func=lambda: Update_All_Recommendations(db), trigger='interval', days=7)
    scheduler.start()

    # run server
    app.run(debug = True, use_reloader=False)

