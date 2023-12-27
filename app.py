# importing libraries
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_apscheduler import APScheduler
# importing models
from scripts import OCR_script
from recommendation_systems.hybrid_model import get_recomendation, Update_All_Recommendations
from config.connection import connect_to_db

# inial flask object
app = Flask(__name__)
CORS(app)

# connect to database
db = connect_to_db()

# get recommendations API
@app.route('/nationalId=<nationalId>')
def recommendations(nationalId):
    try:
        # get recommended partners for a user with hybrid-model RS
        IDs_scores = get_recomendation(db, str(nationalId))
        
        # format IDs and Scores for API
        res = []
        for (id, score) in IDs_scores.items():
            res.append({'nationalId': id, 'score': score})
        return jsonify(res)
    
    except Exception as e:
        return jsonify({"error":str(e)})

# extract nationalId API
@app.route('/extract_nationalId', methods=['POST'])
def get_nationalId():
    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({'status':False, 'message': 'image is required'}), 400
        
        # Check if the file is empty
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status':False,'message': 'image is required'}), 400

        # extract nationalId from image
        nationalId = OCR_script.extract_nationalId(file)
        if len(nationalId)>=10:
            return jsonify({'status':True, 'nationalId': nationalId})
        return jsonify({'status':False, 'message':"couldn't extract nationalId"}), 400
    
    except Exception as e:
        return jsonify({'status':False, 'message':str(e)})


# run main file [app]
if __name__ == '__main__':
    # Update All Recommendations Job every 7 days
    scheduler = APScheduler()
    scheduler.add_job(id='Job 1', name='Update All Recommendations Job', func=lambda: Update_All_Recommendations(db), trigger='interval', days=7)
    scheduler.start()

    # run server
    app.run(debug = True, use_reloader=False)

