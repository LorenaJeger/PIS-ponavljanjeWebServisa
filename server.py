
from flask import Flask,request,make_response,jsonify
from pony import orm

DB = orm.Database()

app = Flask(__name__)

class Stvar(DB.Entity):
   
   stvar = orm.Required(str,unique=True)
   namjena = orm.Required(str)
   cijena = orm.Optional(float)

DB.bind(provider="sqlite", filename="database.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)


def add_stvar(json_request):
    try:
        stvar = json_request["stvar"]
        namjena = json_request["namjena"]
        try:
            cijena = json_request["cijena"]
        except ValueError:
            cijena = None
        with orm.db_session:
            Stvar(stvar=stvar,namjena=namjena,cijena=cijena)
            response = {"response":"Success"}
            return response
    except Exception as e:
        return {"response":"Fail","error":str(e)}
    

def get_stvari():
    try:
        with orm.db_session:
            db_querry = orm.select(x for x in Stvar)[:]
            results_list = []
            for r in db_querry:
                results_list.append(r.to_dict())
            response = {"response":"Success", "data":results_list}
            return response
    except Exception as e:
        return {"response":"Fail", "error":str(e)}



def get_stvar(querry_string):
    try:
        with orm.db_session:
            result = orm.select(x for x in Stvar if x.stvar == querry_string["stvar"])[:][0]
            result = result.to_dict()
            response = {"response":"Success","data":result}
            return response
    except Exception as e:
        return {"response": "Fail", "error":str(e)}
    


def patch_stvar(querry_string, json_request):
    try:
        with orm.db_session:
            to_update = orm.select(x for x in Stvar if x.stvar == querry_string["stvar"])[:][0]
            to_update.set(**json_request)
            response= {"response":"Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error":str(e)}

 
def delete_stvar(querry_string):
    try:
        with orm.db_session:
            to_delete = orm.select(x for x in Stvar if x.stvar== querry_string["stvar"])[:][0]
            to_delete.delete()
            response= {"response":"Success"}
            return response
    except Exception as e:
        return {"response": "Fail", "error":str(e)}




@app.route("/stvar/dodaj", methods=["POST"])
def dodaj_stvar():
    try:
        json_request= request.json
    except Exception as e:
        response = {"response":str(e)}
        return make_response(jsonify(response),400)

    response = add_stvar(json_request)

    if response["response"] == "Success":
        return make_response(jsonify(response),200)
    return make_response(jsonify(response),400)
  


@app.route("/stvar/vrati", methods=["GET"])
def vrati_stvar():
    if request.args:
        response = get_stvar(request.args)
        if response["response"]== "Success":
            return make_response(jsonify(response),200)
        return make_response(jsonify(response),400)
    else:
        response = get_stvari()
        if response["response"] == "Success":
            return make_response(jsonify(response),200)
        return make_response(jsonify(response),400)
    

@app.route("/stvar/obrisi", methods=["DELETE"])
def obrisi_stvar():
    if request.args:
        response = delete_stvar(request.args)
        if response["response"]== "Success":
            return make_response(jsonify(response),200)
        return make_response(jsonify(response),400)
    else:
        response={"response": "Querry string missing"}
        return make_response(jsonify(response),400)
    

@app.route("/stvar/izmjeni", methods=["PATCH"])
def izmjeni_stvar():
    try:
        json_request= request.json
    except Exception as e:
        response= {"response":e}
        return make_response(jsonify(response), 400)
    if request.args:
        response= patch_stvar(request.args, json_request)
        if response["response"]== "Success":
            return make_response(jsonify(response),200)
        return make_response(jsonify(response),400)
    else:
        response={"response": "Querry string missing"}
        return make_response(jsonify(response),400)



if __name__ == "__main__":
    app.run(port=8080)






