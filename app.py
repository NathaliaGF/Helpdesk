from flask import Flask, jsonify, render_template, request
import json
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)

# Arquivo para armazenar os tickets
TICKETS_FILE = 'tickets.json'

def load_tickets():
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tickets(tickets):
    with open(TICKETS_FILE, 'w') as f:
        json.dump(tickets, f, indent=2)

# Gerar alguns tickets iniciais se o arquivo não existir
if not os.path.exists(TICKETS_FILE):
    initial_tickets = []
    problems = ['Hardware', 'Software', 'Network', 'Printer', 'Email']
    
    for i in range(10):
        created_date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S')
        ticket = {
            'id': i + 1,
            'type': random.choice(problems),
            'title': f'Problema #{i+1}',
            'description': f'Descrição do problema #{i+1}',
            'created_date': created_date,
            'response_time': random.randint(5, 120),
            'resolution_time': random.randint(30, 480),
            'priority': random.choice(['High', 'Medium', 'Low']),
            'status': random.choice(['Open', 'In Progress', 'Resolved']),
            'assigned_to': f'Técnico {random.randint(1,5)}'
        }
        initial_tickets.append(ticket)
    save_tickets(initial_tickets)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    tickets = load_tickets()
    return jsonify(tickets)

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    tickets = load_tickets()
    new_ticket = request.json
    
    # Gerar novo ID
    max_id = max([t['id'] for t in tickets], default=0)
    new_ticket['id'] = max_id + 1
    
    # Adicionar data de criação
    new_ticket['created_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    tickets.append(new_ticket)
    save_tickets(tickets)
    return jsonify(new_ticket), 201

@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    tickets = load_tickets()
    ticket = next((t for t in tickets if t['id'] == ticket_id), None)
    
    if ticket is None:
        return jsonify({'error': 'Ticket not found'}), 404
    
    update_data = request.json
    ticket.update(update_data)
    save_tickets(tickets)
    return jsonify(ticket)

@app.route('/api/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    tickets = load_tickets()
    tickets = [t for t in tickets if t['id'] != ticket_id]
    save_tickets(tickets)
    return '', 204

@app.route('/api/metrics')
def get_metrics():
    tickets = load_tickets()
    
    total_tickets = len(tickets)
    avg_response_time = sum(ticket['response_time'] for ticket in tickets) / total_tickets if total_tickets > 0 else 0
    avg_resolution_time = sum(ticket['resolution_time'] for ticket in tickets) / total_tickets if total_tickets > 0 else 0
    
    problem_types = {}
    status_count = {}
    
    for ticket in tickets:
        problem_types[ticket['type']] = problem_types.get(ticket['type'], 0) + 1
        status_count[ticket['status']] = status_count.get(ticket['status'], 0) + 1
    
    return jsonify({
        'total_tickets': total_tickets,
        'avg_response_time': round(avg_response_time, 2),
        'avg_resolution_time': round(avg_resolution_time, 2),
        'problem_types': problem_types,
        'status_count': status_count
    })

if __name__ == '__main__':
    app.run(debug=True)
