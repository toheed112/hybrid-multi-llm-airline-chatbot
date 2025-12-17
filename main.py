# main.py - Entry point: Setup + Launch UI
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    
    # Setup
    from backend.database.populate_db import populate_database
    db = populate_database()
    print(f"DB ready: {db}")
    
    # Test imports
    from backend.tools.policy import lookup_policy
    from backend.graph.workflow import run_graph_v4
    print("Tools and graph loaded!")
    
    # Launch Streamlit UI
    import subprocess
    subprocess.run(["streamlit", "run", "frontend/app.py"])