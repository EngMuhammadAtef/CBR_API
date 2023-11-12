# importing libraries
from flask import Flask, jsonify
from flask_apscheduler import APScheduler
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
    
    except:
        return jsonify()


# run main file [app]
if __name__ == '__main__':
    # Update All Recommendations Job every 7 days
    scheduler = APScheduler()
    scheduler.add_job(id='Job 1', name='Update All Recommendations Job', func=lambda: Update_All_Recommendations(db), trigger='interval', days=7)
    scheduler.start()

    # run server
    app.run(debug = True, use_reloader=False)

