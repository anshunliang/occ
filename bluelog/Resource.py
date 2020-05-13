import sys
from flask_restful import Api
sys.path.append("F:\LCC")
from bluelog import p,app
p()

api = Api(app)
