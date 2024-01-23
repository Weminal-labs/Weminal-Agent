from flask import Flask,request, jsonify
from flask_cors import CORS
from flask import *
from flask import jsonify
import base64

import json
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
  return jsonify({"output": "Hello, cross-origin-world!"})

@app.route("/swapNative",methods=["POST"])
def swap_token():
    # native sang cw20
    user_address = request.json['user_address']
    user_input = request.json['user_input']

    try: 
        if user_address == None or user_address.startswith("orai") == False:
          return { "Action": "error",
          "Comment": "Invalid address"}
    except: 
        print("An exception occurred")

    inputamount = "1000000"
    # b = base64.b64encode(bytes(str(), 'utf-8')) # bytes
    # base64_str = b.decode('utf-8') # convert bytes to string
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
        "Comment": "Swap native token to Oraichain"
    }

    data = jsonify(Response)
    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80,debug=True)