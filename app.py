import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = 'accounts_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'accounts': [], 'settings': {'tax_rate': 40}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    data = load_data()
    return jsonify(data['accounts'])

@app.route('/api/accounts', methods=['POST'])
def add_account():
    data = load_data()
    new_account = request.json
    new_account['id'] = len(data['accounts']) + 1
    data['accounts'].append(new_account)
    save_data(data)
    return jsonify(new_account), 201

@app.route('/api/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    data = load_data()
    data['accounts'] = [a for a in data['accounts'] if a['id'] != account_id]
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    data = load_data()
    accounts = data['accounts']
    tax_rate = data['settings']['tax_rate']
    
    total_invested = sum(float(a.get('invested', 0)) for a in accounts)
    total_withdrawn = sum(float(a.get('withdrawn', 0)) for a in accounts)
    total_passed = len([a for a in accounts if a.get('status') == 'passed'])
    total_suspended = len([a for a in accounts if a.get('status') == 'suspended'])
    total_accounts = len(accounts)
    
    pass_rate = (total_passed / total_accounts * 100) if total_accounts > 0 else 0
    gross_profit = total_withdrawn - total_invested
    taxes = gross_profit * (tax_rate / 100)
    net_profit = gross_profit - taxes
    roi = (gross_profit / total_invested * 100) if total_invested > 0 else 0
    
    return jsonify({
        'total_invested': round(total_invested, 2),
        'total_withdrawn': round(total_withdrawn, 2),
        'gross_profit': round(gross_profit, 2),
        'taxes': round(taxes, 2),
        'net_profit': round(net_profit, 2),
        'roi': round(roi, 2),
        'pass_rate': round(pass_rate, 2),
        'total_passed': total_passed,
        'total_suspended': total_suspended,
        'total_accounts': total_accounts
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
