# Dashboard de Métricas Helpdesk

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap&logoColor=white)
![Licença](https://img.shields.io/badge/Licença-MIT-green)

Dashboard web interativo para gerenciamento de chamados de helpdesk, com métricas em tempo real, gráficos de distribuição e API REST para operações CRUD completas.

O sistema permite registrar, acompanhar e resolver chamados técnicos com controle de prioridade, responsável e tempo de resposta — tudo salvo localmente em JSON, sem necessidade de banco de dados externo.

---

## Funcionalidades

### Métricas e gráficos
- Cards com total de chamados, tempo médio de resposta e tempo médio de resolução
- Gráfico de pizza — distribuição por tipo de problema (Hardware, Software, Rede…)
- Gráfico de rosca — proporção de chamados por status
- Atualização automática a cada 30 segundos sem recarregar a página

### Gerenciamento de chamados
- Criar, editar e excluir chamados via modal
- Alternar status com um clique direto no badge: **Aberto → Em Andamento → Resolvido**
- Busca em tempo real por título, tipo ou responsável
- Filtro por status
- Notificações de feedback (toast) para cada ação realizada
- Mensagem de estado vazio quando nenhum chamado corresponde ao filtro

### Campos de cada chamado

| Campo             | Descrição                                      |
|-------------------|------------------------------------------------|
| Título            | Resumo do problema                             |
| Tipo              | Hardware, Software, Rede, Impressora ou Email  |
| Descrição         | Detalhamento completo do chamado               |
| Data de abertura  | Preenchida automaticamente                     |
| Prioridade        | Alta, Média ou Baixa                           |
| Status            | Aberto, Em Andamento ou Resolvido              |
| Responsável       | Técnico atribuído ao chamado                   |
| Tempo de resposta | Em minutos                                     |
| Tempo de resolução| Em minutos                                     |

---

## Tecnologias

| Camada    | Tecnologia                    |
|-----------|-------------------------------|
| Backend   | Python 3.8+ · Flask 3.0       |
| Frontend  | Bootstrap 5.3 · Chart.js      |
| Ícones    | Bootstrap Icons               |
| Dados     | JSON local (`tickets.json`)   |

---

## Instalação e execução

```bash
# 1. Clone o repositório
git clone https://github.com/NathaliaGF/Helpdesk.git
cd Helpdesk

# 2. (Opcional) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o servidor
python app.py
```

Acesse em: **http://localhost:5000**

> Para habilitar o modo debug (recarregamento automático), defina a variável de ambiente antes de iniciar:
> ```bash
> FLASK_DEBUG=true python app.py
> ```

---

## API REST

| Método   | Rota                      | Descrição                        |
|----------|---------------------------|----------------------------------|
| `GET`    | `/api/tickets`            | Lista todos os chamados          |
| `POST`   | `/api/tickets`            | Cria um novo chamado             |
| `PUT`    | `/api/tickets/<id>`       | Atualiza um chamado existente    |
| `DELETE` | `/api/tickets/<id>`       | Remove um chamado                |
| `GET`    | `/api/metrics`            | Retorna as métricas do dashboard |

**Exemplo — criar chamado:**
```bash
curl -X POST http://localhost:5000/api/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Computador não liga",
    "type": "Hardware",
    "description": "Máquina do setor financeiro não inicializa.",
    "priority": "High",
    "status": "Open",
    "assigned_to": "Técnico 1"
  }'
```

---

## Estrutura do projeto

```
helpdesk/
├── app.py               # Servidor Flask e API REST
├── templates/
│   └── index.html       # Interface com Bootstrap e Chart.js
├── requirements.txt     # Dependências Python
└── README.md
```

> `tickets.json` é gerado automaticamente na primeira execução com 10 chamados de demonstração e está no `.gitignore` — não é versionado.

---

## Como usar

**Criar chamado** — clique em **Novo Chamado**, preencha os campos obrigatórios e salve.

**Editar chamado** — clique no ícone de lápis ✏️ na linha do chamado desejado.

**Excluir chamado** — clique no ícone de lixeira 🗑️ e confirme a exclusão.

**Alternar status** — clique diretamente no badge colorido da coluna Status:
```
Aberto  →  Em Andamento  →  Resolvido  →  Aberto
```

**Buscar / filtrar** — use o campo de texto (busca por título, tipo ou responsável) e o seletor de status para combinar filtros em tempo real.

---

## Roadmap

- [ ] Autenticação de usuários (login/logout)
- [ ] Banco de dados relacional (SQLite → PostgreSQL)
- [ ] Exportação de relatórios em PDF e CSV
- [ ] Histórico de alterações por chamado
- [ ] Notificações por e-mail ao atribuir ou resolver chamados
- [ ] Dashboard com filtro por período de datas

---

## Licença

MIT — livre para uso, modificação e distribuição.
