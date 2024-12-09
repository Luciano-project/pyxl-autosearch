from api.routes import api
import os
from dotenv import load_dotenv
import sys

load_dotenv()
 
if __name__ == '__main__':
    if (len(sys.argv) > 1 and "-d" in sys.argv) or os.getenv("DEBUG") == "True":
        api.run(host='0.0.0.0', port=5000, debug=True)        
    else:
        from waitress import serve
        print("\n\tProductions server initalized on: http://localhost:5000")
        serve(api, host='0.0.0.0', port=5000)

