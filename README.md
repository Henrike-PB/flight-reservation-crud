# Flight Reservation API

API RESTful para gerenciamento de reservas de voos, desenvolvida com **Django**, **Django REST Framework** e **PostgreSQL**.

O sistema permite cadastrar aviões, criar voos, registrar clientes e gerenciar reservas de assentos com validações completas de regra de negócio.

---

## Tecnologias

- Python 3.11
- Django 5.2
- Django REST Framework 3.17
- PostgreSQL 15 (via Docker)
- Docker & Docker Compose

## Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/Henrike-PB/flight-reservation-crud.git
cd flight-reservation-crud
```

### 2. Suba o banco de dados

Certifique-se de ter o Docker instalado e rodando:

```bash
docker-compose up -d
```

Isso cria um container PostgreSQL com as credenciais definidas no `.env`.

### 3. Configure o ambiente Python

```bash
# Crie e ative o ambiente virtual

# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
venv\Scripts\activate     

# Instale as dependências
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

OBS: Verifique o `.env.exemple` para se basear ao criar o `.env`.

```env
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Crie um superusuário

```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor

```bash
python manage.py runserver
```

A API estará em: http://127.0.0.1:8000/api/

O painel Admin em: http://127.0.0.1:8000/admin/

---

## Modelagem de Dados

### Airplane (Avião)

| Campo      | Tipo                  | Descrição                              |
|------------|-----------------------|----------------------------------------|
| id         | BigAutoField (PK)     | Identificador único, gerado automaticamente |
| model      | CharField(100)        | Modelo do avião (único)                |
| capacity   | PositiveIntegerField  | Capacidade máxima de passageiros (≥ 1) |

### Flight (Voo)

| Campo          | Tipo              | Descrição                            |
|----------------|-------------------|--------------------------------------|
| id             | BigAutoField (PK) | Identificador único                  |
| flight_number  | CharField(10)     | Código do voo (único, ex: "AD1234")  |
| origin         | CharField(100)    | Cidade de origem                     |
| destination    | CharField(100)    | Cidade de destino                    |
| departure_time | DateTimeField     | Data e horário de partida            |
| arrival_time   | DateTimeField     | Data e horário de chegada            |
| airplane       | ForeignKey → Airplane | Avião associado ao voo           |

### Client (Cliente)

| Campo     | Tipo              | Descrição                              |
|-----------|-------------------|----------------------------------------|
| id        | BigAutoField (PK) | Identificador único                    |
| user      | OneToOneField → User | Vínculo com o usuário do Django     |
| name      | CharField(100)    | Nome completo                          |
| telephone | CharField(20)     | Telefone de contato                    |
| email     | EmailField        | E-mail (único)                         |

### Reservation (Reserva)

| Campo            | Tipo              | Descrição                                 |
|------------------|-------------------|-------------------------------------------|
| id               | BigAutoField (PK) | Identificador único                       |
| client           | ForeignKey → Client | Cliente que fez a reserva               |
| flight           | ForeignKey → Flight | Voo reservado                           |
| seat             | CharField(5)      | Número do assento (único por voo)         |
| reservation_date | DateTimeField     | Data/hora da reserva (gerada automaticamente) |

**Constraint:** `UniqueConstraint(flight, seat)` — garante que não existam dois passageiros no mesmo assento do mesmo voo.

---

## Endpoints da API

| Recurso      | Método | Endpoint                    | Descrição                     | Permissão              |
|-------------|--------|-----------------------------|-------------------------------|------------------------|
| Aviões      | GET    | `/api/airplanes/`           | Listar todos os aviões        | Público                |
| Aviões      | POST   | `/api/airplanes/`           | Cadastrar avião               | Admin                  |
| Aviões      | GET    | `/api/airplanes/{id}/`      | Detalhar avião                | Público                |
| Aviões      | PUT    | `/api/airplanes/{id}/`      | Atualizar avião               | Admin                  |
| Aviões      | DELETE | `/api/airplanes/{id}/`      | Remover avião                 | Admin                  |
| Voos        | GET    | `/api/flights/`             | Listar todos os voos          | Público                |
| Voos        | POST   | `/api/flights/`             | Criar voo                     | Admin                  |
| Voos        | GET    | `/api/flights/{id}/`        | Detalhar voo                  | Público                |
| Voos        | PUT    | `/api/flights/{id}/`        | Atualizar voo                 | Admin                  |
| Voos        | DELETE | `/api/flights/{id}/`        | Remover voo                   | Admin                  |
| Clientes    | GET    | `/api/clients/`             | Listar clientes               | Autenticado (filtrado) |
| Clientes    | POST   | `/api/clients/`             | Cadastrar cliente             | Autenticado            |
| Clientes    | GET    | `/api/clients/{id}/`        | Detalhar cliente              | Autenticado            |
| Clientes    | PUT    | `/api/clients/{id}/`        | Atualizar cliente             | Autenticado            |
| Clientes    | DELETE | `/api/clients/{id}/`        | Remover cliente               | Autenticado            |
| Reservas    | GET    | `/api/reservations/`        | Listar reservas               | Autenticado (filtrado) |
| Reservas    | POST   | `/api/reservations/`        | Criar reserva                 | Autenticado            |
| Reservas    | GET    | `/api/reservations/{id}/`   | Detalhar reserva              | Autenticado            |
| Reservas    | PUT    | `/api/reservations/{id}/`   | Atualizar reserva             | Autenticado            |
| Reservas    | DELETE | `/api/reservations/{id}/`   | Cancelar reserva              | Autenticado            |

**Autenticação:** A API utiliza autenticação por sessão do Django. Para testar via navegador, faça login em `/admin/` e depois acesse os endpoints da API. Para ferramentas como Postman ou cURL, utilize Basic Auth.

---

## Como testar a API

Após rodar o servidor, crie um superusuário e use os exemplos abaixo. Todos os comandos usam `curl` com Basic Auth (`-u admin:suasenha`).

---

### Aviões

**Criar avião** (Admin):
```bash
curl -u admin:suasenha -X POST http://127.0.0.1:8000/api/airplanes/ \
  -H "Content-Type: application/json" \
  -d '{"model": "Boeing 737-800", "capacity": 180}'
```
Resposta (201 Created):
```json
{
    "id": 1,
    "model": "Boeing 737-800",
    "capacity": 180
}
```

**Listar aviões** (Público):
```bash
curl http://127.0.0.1:8000/api/airplanes/
```
Resposta (200 OK):
```json
[
    {
        "id": 1,
        "model": "Boeing 737-800",
        "capacity": 180
    }
]
```

---

### Voos

**Criar voo** (Admin):
```bash
curl -u admin:suasenha -X POST http://127.0.0.1:8000/api/flights/ \
  -H "Content-Type: application/json" \
  -d '{
    "flight_number": "AD1234",
    "origin": "Porto Alegre",
    "destination": "São Paulo",
    "departure_time": "2026-12-01T10:00:00Z",
    "arrival_time": "2026-12-01T12:00:00Z",
    "airplane": 1
  }'
```
Resposta (201 Created):
```json
{
    "id": 1,
    "airplane_detail": {
        "id": 1,
        "model": "Boeing 737-800",
        "capacity": 180
    },
    "flight_number": "AD1234",
    "origin": "Porto Alegre",
    "destination": "São Paulo",
    "departure_time": "2026-12-01T07:00:00-03:00",
    "arrival_time": "2026-12-01T09:00:00-03:00",
    "airplane": 1
}
```

**Criar voo com origem = destino** (deve falhar):
```bash
curl -u admin:suasenha -X POST http://127.0.0.1:8000/api/flights/ \
  -H "Content-Type: application/json" \
  -d '{
    "flight_number": "AD9999",
    "origin": "São Paulo",
    "destination": "São Paulo",
    "departure_time": "2026-12-01T10:00:00Z",
    "arrival_time": "2026-12-01T12:00:00Z",
    "airplane": 1
  }'
```
Resposta (400 Bad Request):
```json
{
    "destination": ["A origem e o destino não podem ser iguais."]
}
```

---

### Clientes

**Criar cliente** (Autenticado):
```bash
curl -u admin:suasenha -X POST http://127.0.0.1:8000/api/clients/ \
  -H "Content-Type: application/json" \
  -d '{"user": 1, "name": "Henrike", "telephone": "51999999999", "email": "henrike@email.com"}'
```
Resposta (201 Created):
```json
{
    "id": 1,
    "name": "Henrike",
    "telephone": "51999999999",
    "email": "henrike@email.com",
    "user": 1
}
```

---

### Reservas

**Criar reserva** (Autenticado):
```bash
curl -u admin:suasenha -X POST http://127.0.0.1:8000/api/reservations/ \
  -H "Content-Type: application/json" \
  -d '{"client": 1, "flight": 1, "seat": "12"}'
```
Resposta (201 Created):
```json
{
    "id": 1,
    "client": 1,
    "flight": 1,
    "seat": "12",
    "reservation_date": "2026-04-06T02:46:30.995903-03:00",
    "flight_detail": {
        "id": 1,
        "airplane_detail": {
            "id": 1,
            "model": "Boeing 737-800",
            "capacity": 180
        },
        "flight_number": "AD1234",
        "origin": "Porto Alegre",
        "destination": "São Paulo",
        "departure_time": "2026-12-01T07:00:00-03:00",
        "arrival_time": "2026-12-01T09:00:00-03:00",
        "airplane": 1
    },
    "client_detail": {
        "id": 1,
        "name": "Henrike",
        "telephone": "51999999999",
        "email": "henrike@email.com",
        "user": 1
    }
}
```

**Assento duplicado** (deve falhar):
```bash
curl -u admin:suasenha -X POST http://127.0.0.1:8000/api/reservations/ \
  -H "Content-Type: application/json" \
  -d '{"client": 1, "flight": 1, "seat": "12"}'
```
Resposta (400 Bad Request):
```json
{
    "non_field_errors": ["Os campos flight, seat devem criar um set único."]
}
```

**Assento excede capacidade** (deve falhar):
```bash
curl -u admin:suasenha -X POST http://127.0.0.1:8000/api/reservations/ \
  -H "Content-Type: application/json" \
  -d '{"client": 1, "flight": 1, "seat": "200"}'
```
Resposta (400 Bad Request):
```json
{
    "seat": ["Este avião tem apenas 180 assentos. Assento 200 é inválido."]
}
```

**Acesso sem autenticação** (deve falhar):
```bash
curl http://127.0.0.1:8000/api/reservations/
```
Resposta (403 Forbidden):
```json
{
    "detail": "As credenciais de autenticação não foram fornecidas."
}
```

---

## Regras de negócio implementadas

- Aviões devem ter capacidade mínima de 1 passageiro.
- Voos não podem ter origem e destino iguais.
- Data de partida não pode ser no passado.
- Data de chegada deve ser posterior à de partida.
- Cada assento é único por voo (não é possível reservar o mesmo assento duas vezes).
- O número do assento não pode exceder a capacidade do avião.
- O voo não pode receber reservas além da sua capacidade.
- Usuários comuns só veem suas próprias reservas e dados de cliente.
- Apenas administradores podem cadastrar/editar/remover aviões e voos.

## Regras de permissão

| Recurso   | Leitura           | Escrita (CRUD)      |
|-----------|-------------------|---------------------|
| Aviões    | Público           | Apenas Admin        |
| Voos      | Público           | Apenas Admin        |
| Clientes  | Autenticado (próprio) | Autenticado     |
| Reservas  | Autenticado (próprio) | Autenticado     |

---

## Estrutura do projeto

```
flight-reservation-crud/
├── setup/                  # Configurações do Django (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── flights/                # App principal
│   ├── models.py           # Modelos: Airplane, Flight, Client, Reservation
│   ├── serializers.py      # Serializers com validações de regra de negócio
│   ├── views.py            # ViewSets com controle de permissão
│   ├── urls.py             # Rotas da API (DefaultRouter)
│   ├── admin.py            # Configuração do painel Admin
│   └── migrations/         # Migrações do banco de dados
├── desafio_logica_01.py    # Desafio de lógicac escolhido
├── QUESTIONARIO.md         # Respostas ao questionário
├── requirements.txt        # Dependências do projeto
├── docker-compose.yml      # Container PostgreSQL
├── manage.py
└── .env                    # Variáveis de ambiente
```

## Desafio de Lógica

O desafio de lógica escolhido está na raiz do repositório:

```bash
python desafio_logica_01.py
```

[Acessar Script](desafio_logica_01.py)


## Questionário

As respostas ao questionário estão em [QUESTIONARIO.md](QUESTIONARIO.md).

## Decisões Técnicas

As justificativas das escolhas de arquitetura e tecnologia estão em [DECISOES_TECNICAS.md](DECISOES_TECNICAS.md).
