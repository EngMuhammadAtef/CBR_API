def connect_to_db():
    """
        Connect to database on cloud
    """
    # import MongoDB Client
    from pymongo.mongo_client import MongoClient

    # Create a new client and connect to the server from cloud
    # database link from cloud # dataAnalysis:khadiga
    uri = "mongodb+srv://MLrecommendation:atef@cluster0.lr1t0or.mongodb.net/?retryWrites=true&w=majority" 
    client = MongoClient(uri)
    
    # Connect to Database
    db = client['test'] # database name

    return db