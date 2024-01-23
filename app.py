from flask import Flask,request, jsonify
from flask_cors import CORS
from flask import *
from flask import jsonify
import base64

import json

app = Flask(__name__)
CORS(app)

from Oraidex_models.response import generate_response


def check_valid_address(address):
    if address == None or address.startswith("orai") == False:
        return False
    return True


@app.route("/")
def home():
  return jsonify({"output": "Hello, cross-origin-world!"})

@app.route("/swapNative",methods=["POST"])
def swap_token():
    # native sang cw20
    user_address = request.json['user_address']
    user_input = request.json['user_input']

    try: 
        if check_valid_address(user_address) == False:
            return jsonify({"output": "Invalid address"})
    except: 
        print("An exception occurred")

    inputamount = "1000000"
   
    Pair_contract = "orai1agqfdtyd9lr0ntmfjtzl4f6gyswpeq4z4mdnq4npdxdc99tcw35qesmr9v"
    
    msg = {"msg":{"swap": {
        "offer_asset": {
          "info": {
            "native_token": {
              "denom": "orai"
            }
          },
          "amount": str(inputamount)
          }
        }}
      }
    
    Response = {
        "Action": "Excute",
        "Parameters":msg,
        "inputamout": str(inputamount),
        "Pair_contract": str(Pair_contract),
        "output": "Swap native token to Oraichain"
    }

    data = jsonify(Response)
    return data


@app.route("/chatoraidex",methods=["POST"])
def chatbot_with_trading():
    user_address = request.json['user_address']
    user_input = request.json['user_input']
   
    if check_valid_address(user_address) == False:
      return jsonify({"output": "Invalid address"})    
    else:
      response = generate_response(user_input)
      return {"output": response,"status": "oraidex"}

 



if __name__ == "__main__":
    app.run(debug=True)