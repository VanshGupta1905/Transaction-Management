from flask import Flask,request,jsonify,render_template
import UpiUser as UPIUser
import uuid
app = Flask(__name__)
users = {}

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    upi_id = data['upi_id']
    users[upi_id] = UPIUser.UpiUser(upi_id)
    return jsonify({"message": "User created"}), 201

@app.route('/request_money', methods=['POST'])
def request_money():
    data = request.json
    requester = users.get(data['requester_upi_id'])
    if requester:
        request_data = requester.request_money(
            data['from_upi_id'], 
            data['amount'], 
            data.get('description', '')
        )
        request_data['id'] = str(uuid.uuid4())  # Generate a unique ID for the request
        return jsonify({"message": "Money request sent", "request": request_data}), 200
    return jsonify({"error": "Requester not found"}), 404

@app.route('/pending_requests/<upi_id>', methods=['GET'])
def get_pending_requests(upi_id):
    user = users.get(upi_id)
    if user:
        return jsonify({"pending_requests": user.get_pending_requests()}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/approve_request', methods=['POST'])
def approve_request():
    data = request.json
    user = users.get(data['upi_id'])
    if user and user.approve_request(data['request_id']):
        return jsonify({"message": "Request approved"}), 200
    return jsonify({"error": "Failed to approve request"}), 400

@app.route('/reject_request', methods=['POST'])
def reject_request():
    data = request.json
    user = users.get(data['upi_id'])
    if user and user.reject_request(data['request_id']):
        return jsonify({"message": "Request rejected"}), 200
    return jsonify({"error": "Failed to reject request"}), 400

@app.route('/checkBalance')
def check_balance():
    upi_id = request.args.get('upi_id')
    user = users.get(upi_id)
    if user:
        balance_info = user.request_balance()
        return jsonify(balance_info), 200
    return jsonify({"error": "User not found"}), 404

app.run(debug=True)