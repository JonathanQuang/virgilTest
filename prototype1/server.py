from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import virgilFlaskLib
import virgilServerClient

app = Flask(__name__)

@app.route('/')
def route():
    return render_template("index.html")


@app.route('/message', methods=['POST'])
def messageOriginal():
    print(request.form['message'])
    vFL = virgilFlaskLib.VirgilFlaskLib()
    print(vFL.get_private_key())
    print(vFL.get_public_key())
    print(vFL.generate_JWT_for_user(request.form['message']))
   # print(vFL.publish_card())
    return jsonify(publc_key = str(vFL.get_public_key()), 
                    private_key = str(vFL.get_private_key),
                    messageJWT = str(vFL.generate_JWT_for_user(request.form['message']))                
                    )

@app.route('/send', methods=['POST'])
def message():
    print(request.form['message'])
    msg = request.form['message']
    vFL = virgilServerClient.VirgilServerClient()
    jwt_from_server_to_client = vFL.authenticated_query_to_server(msg)
    token_from_server = vFL.get_token_from_server(jwt_from_server_to_client)
    vFL.publish_card(request.form['message'])

    return jsonify(error_msg = "error",
                    jwt_server_to_client = str(jwt_from_server_to_client),
                    jwt_from_client_to_server = token_from_server
                    )
    


if __name__ == '__main__':
    
    app.run(debug=True)


