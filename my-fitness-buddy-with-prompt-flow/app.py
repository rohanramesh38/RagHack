from flask import Flask, render_template, request, jsonify
import requests
import json
app = Flask(__name__)

global_chat_history=[]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/message', methods=['POST'])
def get_message():
    user_message = request.json['message']
    api_endpoint = request.json['api_endpoint']
    api_key = request.json['api_key']

    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}",
        "azureml-model-deployment": "rag-hack-propmtflow-fitness-app",
        "accept":"*/*"
        
    }

    payload = json.dumps({
    "query": user_message,
    "chat_history": global_chat_history
    })


    response = requests.request("POST", api_endpoint, headers=headers, data=payload)


    if response.status_code == 200:
        print(response.json())
        response=response.json()
        print(response)

        global_chat_history.append({
        "inputs":{"query":user_message},
        "outputs":response
        })
        return response
    else:
        return jsonify({"error": f"Azure request failed with status code {response.status_code}", "details": response.text}), response.status_code
    
    


if __name__ == '__main__':
    app.run(debug=True)
