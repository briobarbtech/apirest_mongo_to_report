from flask import Flask, request, Response
from flask_pymongo import PyMongo
from bson import json_util, ObjectId
from models.report import Report
from http import HTTPStatus
from models.resources import paginar_10,searchReport

app = Flask(__name__)
### Defino una propiedad que va a decir donde buscar MongoDB. MongoDB siempre trabaja en el puerto 27017
app.config['MONGO_URI']='mongodb://localhost/starwarsdb'
### Le paso la configuración de mi app a PyMongo
mongo = PyMongo(app)



### to get all reports do GET request to http://localhost:5000/report
@app.route('/report/page=<id>', methods=["GET"])
def get_reports(id):
    reports_data = mongo.db.report.find()
    response = {}
    reports_data_list = json_util.loads(json_util.dumps(reports_data))
    reports = paginar_10(reports_data_list, int(id))
    response['results']=reports
    response = json_util.dumps(reports)
    return Response(response, mimetype='application/json'),HTTPStatus.OK

### to get all reports do GET request to http://localhost:5000/report
@app.route('/reports', methods=["GET"])
def get_Allreports():
    reports_data = mongo.db.report.find()
    response = json_util.dumps(reports_data)
    return Response(response, mimetype='application/json'),HTTPStatus.OK

### to report Post request to http://localhost:5000/report
@app.route('/report', methods=["POST"])
def report_sighting():
    report = Report(request.json['name'],request.json['title'],request.json['body'], request.json['date'],request.json['publish'])
    id = mongo.db.report.insert_one({
        "name":report.name,
        "title":report.title,
        "body":report.body,
        "date":report.date,
        "publish":report.publish})
    return {'message':'Creado con éxito'},HTTPStatus.CREATED
### to active again some report to Put http://127.0.0.1:5001/report/<id>
@app.route('/report/publish/<id>', methods=['PUT'])
def activating_report(id):
    reports_data = mongo.db.report.find()
    reports_data_list = json_util.loads(json_util.dumps(reports_data))
    report_to_delete = reports_data_list[int(id)-1]['_id']
    print(type(json_util.dumps(report_to_delete)))
    mongo.db.report.update_one({'_id': ObjectId(report_to_delete)}, update={'$set' :{'publish': True}})
    #mongo.db.report.delete_one({'_id': ObjectId(report_to_delete)})
    return Response({'message':'Activado con éxito'}, mimetype='application/json'),HTTPStatus.OK

### to delete some report to Put http://127.0.0.1:5001/report/<id>
@app.route('/report/<id>', methods=['PUT'])
def delete_report(id):
    reports_data = mongo.db.report.find()
    
    reports_data_list = json_util.loads(json_util.dumps(reports_data))
    report = searchReport(reports_data_list, int(id))
    report_to_delete = report['_id']
    print(type(json_util.dumps(report_to_delete)))
    mongo.db.report.update_one({'_id': ObjectId(report_to_delete)}, update={'$set' :{'publish': False}})
    #mongo.db.report.delete_one({'_id': ObjectId(report_to_delete)})
    return {'message':'Borrado con éxito'},HTTPStatus.OK

@app.errorhandler(404)
### response default for errors
def not_found(error=None):
    message = {'message': 'Resource Not Found: ' + request.url,'status' : 404}
    return message
if __name__ == "__main__":
    app.run(port=5001,debug=True)