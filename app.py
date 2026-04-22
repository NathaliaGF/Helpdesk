from flask import Flask, jsonify, render_template, request
import json
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)

TICKETS_FILE = 'tickets.json'

# Valores válidos para cada campo controlado
VALID_TYPES      = {'Hardware', 'Software', 'Network', 'Printer', 'Email'}
VALID_PRIORITIES = {'High', 'Medium', 'Low'}
VALID_STATUSES   = {'Open', 'In Progress', 'Resolved'}
REQUIRED_FIELDS  = ['title', 'type', 'description', 'priority', 'status', 'assigned_to']


# ── Persistência ──────────────────────────────────────────────────────────────

def load_tickets() -> list:
    if os.path.exists(TICKETS_FILE):
        try:
            with open(TICKETS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_tickets(tickets: list) -> None:
    with open(TICKETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)


def next_id(tickets: list) -> int:
    return max((t['id'] for t in tickets), default=0) + 1


# ── Dados iniciais de demonstração ────────────────────────────────────────────

if not os.path.exists(TICKETS_FILE):
    problems = list(VALID_TYPES)
    demo = []
    for i in range(10):
        created = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S')
        demo.append({
            'id': i + 1,
            'type': random.choice(problems),
            'title': f'Problema #{i + 1}',
            'description': f'Descrição do problema #{i + 1}',
            'created_date': created,
            'response_time': random.randint(5, 120),
            'resolution_time': random.randint(30, 480),
            'priority': random.choice(list(VALID_PRIORITIES)),
            'status': random.choice(list(VALID_STATUSES)),
            'assigned_to': f'Técnico {random.randint(1, 5)}',
        })
    save_tickets(demo)


# ── Validação ─────────────────────────────────────────────────────────────────

def validate_ticket(data: dict, require_all: bool = True):
    """Retorna (dados_limpos, mensagem_erro). mensagem_erro é None em caso de sucesso."""
    if require_all:
        missing = [f for f in REQUIRED_FIELDS if not str(data.get(f, '')).strip()]
        if missing:
            return None, f"Campos obrigatórios ausentes: {', '.join(missing)}"

    cleaned = {}

    if 'title' in data:
        title = str(data['title']).strip()
        if not title:
            return None, "Título não pode ser vazio."
        cleaned['title'] = title[:200]

    if 'type' in data:
        if data['type'] not in VALID_TYPES:
            return None, f"Tipo inválido. Valores aceitos: {', '.join(VALID_TYPES)}"
        cleaned['type'] = data['type']

    if 'description' in data:
        cleaned['description'] = str(data['description']).strip()[:2000]

    if 'priority' in data:
        if data['priority'] not in VALID_PRIORITIES:
            return None, f"Prioridade inválida. Valores aceitos: {', '.join(VALID_PRIORITIES)}"
        cleaned['priority'] = data['priority']

    if 'status' in data:
        if data['status'] not in VALID_STATUSES:
            return None, f"Status inválido. Valores aceitos: {', '.join(VALID_STATUSES)}"
        cleaned['status'] = data['status']

    if 'assigned_to' in data:
        cleaned['assigned_to'] = str(data['assigned_to']).strip()[:100]

    for field in ('response_time', 'resolution_time'):
        if field in data:
            try:
                cleaned[field] = max(0, int(data[field]))
            except (ValueError, TypeError):
                return None, f"'{field}' deve ser um número inteiro."

    return cleaned, None


# ── Rotas ─────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    return jsonify(load_tickets())


@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'JSON inválido ou ausente.'}), 400

    cleaned, error = validate_ticket(data, require_all=True)
    if error:
        return jsonify({'error': error}), 422

    tickets = load_tickets()
    cleaned['id'] = next_id(tickets)
    cleaned['created_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cleaned.setdefault('response_time', 0)
    cleaned.setdefault('resolution_time', 0)

    tickets.append(cleaned)
    save_tickets(tickets)
    return jsonify(cleaned), 201


@app.route('/api/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'JSON inválido ou ausente.'}), 400

    tickets = load_tickets()
    ticket = next((t for t in tickets if t['id'] == ticket_id), None)
    if ticket is None:
        return jsonify({'error': 'Chamado não encontrado.'}), 404

    cleaned, error = validate_ticket(data, require_all=False)
    if error:
        return jsonify({'error': error}), 422

    ticket.update(cleaned)
    save_tickets(tickets)
    return jsonify(ticket)


@app.route('/api/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    tickets = load_tickets()
    new_list = [t for t in tickets if t['id'] != ticket_id]
    if len(new_list) == len(tickets):
        return jsonify({'error': 'Chamado não encontrado.'}), 404
    save_tickets(new_list)
    return '', 204


@app.route('/api/metrics')
def get_metrics():
    tickets = load_tickets()
    total = len(tickets)

    avg_response   = round(sum(t.get('response_time', 0)   for t in tickets) / total, 2) if total else 0
    avg_resolution = round(sum(t.get('resolution_time', 0) for t in tickets) / total, 2) if total else 0

    problem_types: dict = {}
    status_count:  dict = {}
    for t in tickets:
        problem_types[t['type']]  = problem_types.get(t['type'], 0) + 1
        status_count[t['status']] = status_count.get(t['status'], 0) + 1

    return jsonify({
        'total_tickets':       total,
        'avg_response_time':   avg_response,
        'avg_resolution_time': avg_resolution,
        'problem_types':       problem_types,
        'status_count':        status_count,
    })


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Use a variável de ambiente FLASK_DEBUG=true para habilitar o modo debug.
    # Nunca exponha debug=True direto em produção.
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug)
