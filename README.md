# Chatbot Educacional Eliane

Chatbot educacional em Python que responde perguntas de forma clara, didatica
e objetiva sobre um tema escolhido pelo aluno. A logica central usa um **LLM
local** servido pelo [Ollama](https://ollama.com) — **nenhuma chamada de API
externa** e feita. O projeto e inteiramente containerizado com Docker.

## Arquitetura

```
chatboteliane/
├── app/                      # Pacote principal (backend)
│   ├── core/                 # Config e templates de prompt
│   │   ├── config.py
│   │   └── prompts.py
│   ├── llm/                  # Adaptadores de LLM
│   │   ├── base.py           # Interface LLMClient
│   │   └── ollama.py         # Cliente HTTP Ollama
│   ├── services/             # Logica de dominio
│   │   ├── chatbot.py        # Chatbot (usa LLMClient)
│   │   ├── quiz_parser.py    # Parser do formato de quiz
│   │   └── session_store.py  # Sessoes em memoria
│   ├── api/                  # Camada FastAPI
│   │   ├── server.py         # App + lifespan + CORS
│   │   ├── schemas.py        # Pydantic models
│   │   ├── deps.py           # Injecao de dependencia
│   │   └── routes/           # health, themes, sessions, messages, quiz
│   └── cli/                  # Interface no terminal
│       └── terminal.py
├── frontend/                 # Vite + React (opcional)
├── main.py                   # Entry point do terminal
├── Dockerfile.backend
├── docker-compose.yml        # ollama + backend + frontend
├── requirements.txt
├── .env.example
└── README.md
```

Camadas:

1. **core** — configuracao e templates, sem logica.
2. **llm** — adaptadores da engine de LLM. Qualquer engine compativel com a
   interface `LLMClient` pode substituir o Ollama sem mexer em servicos.
3. **services** — `Chatbot`, `SessionStore`, parser de quiz. Regras de dominio.
4. **api** — FastAPI. So orquestra: recebe request, chama servico, devolve DTO.
5. **cli** — reaproveita os mesmos servicos; zero duplicacao com a API.

## Como rodar (Docker)

Pre-requisitos: [Docker](https://docs.docker.com/get-docker/) + Docker Compose.

```bash
cp .env.example .env
docker compose up --build
```

O compose sobe tres servicos:

| Servico       | Porta  | Descricao                              |
|---------------|--------|----------------------------------------|
| `ollama`      | 11434  | Engine do LLM local                    |
| `backend`     | 5000   | API FastAPI (`/api/...`)               |
| `frontend`    | 5173   | UI em Vite + React                     |

Na primeira subida o job `ollama-init` baixa o modelo configurado
(`OLLAMA_MODEL`, padrao `llama3.2:1b` — cerca de 1,3 GB). Aguarde esse job
terminar antes de conversar. Para baixar outro modelo:

```bash
OLLAMA_MODEL=llama3.2:3b docker compose run --rm ollama-init
```

Endpoints uteis:

- API:       http://localhost:5000/api/health
- Swagger:   http://localhost:5000/docs
- Frontend:  http://localhost:5173

## Como rodar no terminal (sem Docker)

1. Instale o Ollama localmente e deixe-o rodando:
   ```bash
   # macOS/Linux: https://ollama.com/download
   ollama serve &
   ollama pull llama3.2:1b
   ```
2. Crie o venv, instale as dependencias e inicie:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   python main.py
   ```

### Comandos do terminal

| Comando    | Descricao                               |
|------------|-----------------------------------------|
| `sair`     | Encerra o chatbot                       |
| `quiz`     | Ativa o modo quiz                       |
| `conversa` | Volta ao modo conversa (dentro do quiz) |
| `ajuda`    | Lista os comandos                       |

## Endpoints da API

| Metodo  | Rota                                     | Descricao                     |
|---------|------------------------------------------|-------------------------------|
| GET     | `/api/health`                            | Liveness + status do Ollama   |
| GET     | `/api/themes`                            | Lista temas pre-definidos     |
| GET     | `/api/sessions`                          | Lista sessoes ativas          |
| POST    | `/api/sessions`                          | Cria sessao (`{"tema": ...}`) |
| GET     | `/api/sessions/{id}`                     | Detalhe + mensagens           |
| DELETE  | `/api/sessions/{id}`                     | Remove a sessao               |
| POST    | `/api/sessions/{id}/messages`            | Envia pergunta ao bot         |
| POST    | `/api/sessions/{id}/quiz`                | Gera uma pergunta de quiz     |

## Variaveis de ambiente

Consulte `.env.example`. Principais:

| Variavel              | Padrao                    | Descricao                       |
|-----------------------|---------------------------|---------------------------------|
| `OLLAMA_URL`          | `http://localhost:11434`  | Endpoint do Ollama              |
| `OLLAMA_MODEL`        | `llama3.2:1b`             | Modelo usado pelo chatbot       |
| `OLLAMA_TEMPERATURE`  | `0.7`                     | Criatividade da geracao         |
| `MAX_RESPONSE_WORDS`  | `150`                     | Limite pedido ao modelo         |
| `MAX_HISTORY_MESSAGES`| `20`                      | Turnos mantidos no contexto     |
| `CORS_ORIGINS`        | `http://localhost:5173`   | Origens permitidas (CSV)        |

## Substituir o LLM local

A engine Ollama pode ser trocada criando uma nova classe que implemente
`app.llm.base.LLMClient` (`chat(...)` e `health()`) e instanciando-a no
`lifespan` em `app/api/server.py`. O resto da aplicacao nao precisa mudar.

## Tecnologias

- **Python 3.11+**
- **FastAPI** — API REST
- **Ollama** — LLM local (inferencia em CPU/GPU)
- **httpx** — cliente HTTP
- **Pydantic v2** — validacao
- **Docker / Docker Compose** — containerizacao
- **Vite + React** — frontend (opcional)
