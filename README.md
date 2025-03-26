# Dashboard de Métricas Helpdesk

Este é um dashboard interativo que mostra métricas importantes de chamados de helpdesk, incluindo tempos de resposta, tipos de problemas e status dos chamados.

## Funcionalidades

### Métricas e Visualizações
- Total de chamados ativos
- Tempo médio de resposta
- Tempo médio de resolução
- Gráfico de pizza para distribuição de tipos de problemas
- Gráfico de rosca para status dos chamados

### Gerenciamento de Chamados
- Criação de novos chamados
- Edição de chamados existentes
- Exclusão de chamados
- Mudança rápida de status (clique no status para alternar)

### Campos do Chamado
- Título
- Tipo (Hardware, Software, Rede, etc.)
- Descrição detalhada
- Data de abertura (automática)
- Prioridade (Alta, Média, Baixa)
- Status (Aberto, Em Andamento, Resolvido)
- Responsável
- Tempo de resposta
- Tempo de resolução

### Recursos Adicionais
- Busca por texto em chamados
- Filtro por status
- Atualização automática a cada 30 segundos
- Persistência de dados em arquivo JSON
- Interface responsiva e moderna

## Requisitos

- Python 3.8+
- Flask
- Pandas
- Python-dateutil

## Como executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o servidor:
```bash
python app.py
```

3. Acesse o dashboard em seu navegador:
```
http://localhost:5000
```

## Estrutura do Projeto

- `app.py`: Servidor Flask e API REST
- `templates/index.html`: Interface do usuário com Bootstrap e Chart.js
- `requirements.txt`: Dependências do projeto
- `tickets.json`: Banco de dados local para armazenamento dos chamados

## Como Usar

1. **Criar Chamado**:
   - Clique no botão "Novo Chamado"
   - Preencha todos os campos obrigatórios
   - Clique em "Salvar"

2. **Editar Chamado**:
   - Localize o chamado na lista
   - Clique no ícone de lápis
   - Faça as alterações necessárias
   - Clique em "Salvar"

3. **Excluir Chamado**:
   - Localize o chamado na lista
   - Clique no ícone de lixeira
   - Confirme a exclusão

4. **Mudar Status**:
   - Clique no badge de status do chamado
   - O status alternará entre: Aberto → Em Andamento → Resolvido

5. **Buscar/Filtrar**:
   - Use o campo de busca para encontrar chamados por título, tipo ou responsável
   - Use o filtro de status para ver apenas chamados em determinado estado
