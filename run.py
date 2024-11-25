from api.routes import api

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1 and "-d" in sys.argv:
        api.run(host='0.0.0.0', port=5000, debug=True)        
    else:
        from waitress import serve
        print("\n\tServidor de produção iniciado com sucesso em http://localhost:5000")
        serve(api, host='0.0.0.0', port=5000)

