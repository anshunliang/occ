#!/usr/bin/env python
from bluelog import create_app


app = create_app()
#login_manager = LoginManager(app)



if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5001)
    app.run(host="127.0.0.1", debug=True)
