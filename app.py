# importing libraries
from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from recommendation_systems import CBR
from config.connection import connect_to_db
from crud_operations import crud

# inial flask object
app = Flask(__name__)

# connect to database and access recommendations collection
db = connect_to_db()

# get recomendation API
@app.route('/nationalId=<nationalId>', methods = ['GET', 'POST']) 
def home(nationalId):
    try:
        # convert to string
        nationalId = str(nationalId)
        
        # get content-based recomendation for user content and other users' content
        users_nationalIDs, users_scores = CBR.get_recomendation(db, nationalId)
        
        # save recommendations in database
        crud.Update_Recom_List(db, nationalId, users_nationalIDs, users_scores)

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
    scheduler.add_job(id='Job 1', name='Update All Recommendations Job', func=lambda: CBR.Update_All_Recommendations(db), trigger='interval', days=7)
    scheduler.start()

    # run server
    app.run(debug = True, use_reloader=False)

