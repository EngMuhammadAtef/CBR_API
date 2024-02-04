# importing flask App
from flask import Flask, jsonify
from flask_cors import CORS
from flask_apscheduler import APScheduler
# import database connection
from config.connection import connect_to_sql
from crud_operations import crud
# import ML models
from recommendation_systems.hybrid_model import get_recomendation, Update_All_Embeddings

# initial flask object
app = Flask(__name__)
CORS(app)

# connect to database
sql_conn = connect_to_sql()

# get recommendations API
@app.route('/nationalId=<nationalId>')
def recommendations(nationalId: str):
    try:
        # get all content for users
        content_data = crud.get_all_content(sql_conn)

        # get recommended partners for a user with hybrid-model RS
        IDs_scores_Prate = get_recomendation(nationalId, content_data)
        
        # format IDs and Scores for JSON
        recommendations_list = []
        for (id, score, rate) in IDs_scores_Prate:
            recommendations_list.append({'nationalId': id, 'score': score, 'predScore': rate})
        return jsonify(recommendations_list)
    
    except Exception as e:
        return jsonify({"error":str(e)})

# run main file [app]
if __name__ == '__main__':
    # Update All Recommendations Job a day
    scheduler = APScheduler()
    scheduler.add_job(id='Job 1', name='Update All Embeddings Job', func=lambda: Update_All_Embeddings(crud.get_all_ratings(sql_conn)), trigger='interval', hours=1)
    scheduler.start()

    # run server
    app.run(debug = True, use_reloader=False)