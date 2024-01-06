# importing flask App
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_apscheduler import APScheduler
# import database connection
from config.connection import connect_to_sql, connect_to_mongo
from crud_operations import crud
from pipeline import ETL
# import ML models
from recommendation_systems.hybrid_model import get_recomendation, Update_All_Recommendations
from scripts import OCR_script

# inial flask object
app = Flask(__name__)
CORS(app)

# connect to database
sql_conn = connect_to_sql()
mongo_con = connect_to_mongo()

# get recommendations API
@app.route('/nationalId=<nationalId>')
def recommendations(nationalId: str):
    try:
        # extract, transform and load the new user to warehouse
        ETL.Extract_Transform_Load(mongo_con, nationalId, sql_conn)
        
        # get all content for users
        content_data = crud.get_all_content(sql_conn)

        # get recommended partners for a user with hybrid-model RS
        IDs_scores = get_recomendation(content_data, nationalId)
        
        # format IDs and Scores for JSON
        recommendations_list = []
        for (id, score) in IDs_scores.items():
            recommendations_list.append({'nationalId': id, 'score': score})
        return jsonify(recommendations_list)
    
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
    scheduler.add_job(id='Job 1', name='Update All Recommendations Job', func=lambda: Update_All_Recommendations(crud.get_all_content(sql_conn)), trigger='interval', days=7)
    scheduler.start()

    # run server
    app.run(debug = True, use_reloader=False)