# Decisões Técnicas

Documento que explica as escolhas de arquitetura e tecnologia feitas neste projeto, com o raciocínio por trás de cada uma.

---

## 1. Por que Docker para o banco de dados?

Optei por usar Docker Compose para rodar o PostgreSQL ao invés de instalar o banco diretamente na máquina. Isso traz dois benefícios principais: qualquer pessoa que for avaliar ou rodar o projeto só precisa ter o Docker instalado — um único `docker-compose up -d` já sobe o banco configurado, sem precisar instalar PostgreSQL, criar databases ou configurar usuários manualmente. Além disso, garante que todos rodam exatamente a mesma versão (PostgreSQL 15) com as mesmas configurações, eliminando o clássico "na minha máquina funciona".

## 2. Por que PostgreSQL e não SQLite?

O desafio pedia explicitamente Django + PostgreSQL. Mas, mesmo sem essa exigência, PostgreSQL seria a escolha certa para um sistema de reservas. O SQLite não lida bem com acessos simultâneos (problema real quando múltiplos usuários tentam reservar assentos ao mesmo tempo), enquanto o PostgreSQL suporta concorrência nativamente. Além disso, constraints como `UniqueConstraint` se comportam de forma mais confiável no PostgreSQL.

## 3. Por que API REST (DRF) ao invés de templates Django?

Escolhi construir uma API RESTful com Django REST Framework ao invés de usar o sistema de templates do Django. Uma API desacopla o backend do frontend, o mesmo backend pode servir um site, um app mobile ou ser consumido por outro sistema. Isso reflete melhor a realidade de projetos profissionais, onde o frontend geralmente é separado (React, Vue, mobile). O DRF também oferece ferramentas como Serializers com validação, ViewSets que geram CRUD automaticamente, e uma interface navegável que facilita testes.

## 4. Por que ModelViewSet e DefaultRouter?

Ao invés de escrever views individuais para cada operação (listar, criar, editar, deletar), utilizei `ModelViewSet` do DRF, que gera automaticamente todas essas operações a partir do model e do serializer. Combinado com o `DefaultRouter`, as rotas também são geradas automaticamente. Isso segue o princípio DRY (Don't Repeat Yourself), ou seja, menos código repetido significa menos chance de bugs e manutenção mais simples.

## 5. Por que separar validações no Serializer e não no Model?

As validações de regra de negócio (origem ≠ destino, assento dentro da capacidade, voo lotado) ficam nos Serializers e não nos Models. Essa é uma decisão intencional: os Models definem a **estrutura** dos dados e constraints de banco (como `UniqueConstraint`), enquanto os Serializers lidam com a **lógica de negócio** que depende do contexto da requisição. Isso mantém cada camada com uma responsabilidade clara e facilita a manutenção.

## 6. Por que usar variáveis de ambiente (.env)?

As credenciais do banco (nome, usuário, senha, host, porta) ficam em um arquivo `.env` que não é commitado no repositório (está no `.gitignore`). Isso é uma prática de segurança: credenciais nunca devem estar hardcoded no código-fonte. O arquivo `.env.example` serve como referência para quem for configurar o projeto, sem expor dados sensíveis.

## 7. Por que controle de permissões por tipo de usuário?

O sistema diferencia três níveis de acesso: anônimo (pode ver aviões e voos), autenticado (pode gerenciar suas reservas e perfil) e administrador (acesso total). Essa separação foi feita com `get_permissions()` nos ViewSets, permitindo regras diferentes para leitura e escrita no mesmo endpoint. Em um sistema de reservas real, faz sentido que qualquer pessoa possa consultar voos disponíveis, mas apenas usuários autenticados possam fazer reservas.

## 8. Por que campos read_only separados no ReservationSerializer?

No serializer de Reservas, usei campos separados para leitura e escrita: `flight_detail` e `client_detail` (read-only, retornam dados completos) versus `flight` e `client` (write-only, recebem apenas o ID). Isso resolve um problema comum em APIs: na hora de criar, o cliente envia apenas os IDs; na hora de ler, a resposta vem com todos os dados expandidos, sem precisar de requisições adicionais.
