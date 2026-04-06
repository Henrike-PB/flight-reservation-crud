# Questionário — Teste DEV aDoc

## 1. Quais linguagens de programação você conhece?

Minha linguagem principal é **Python**, com a qual tenho o contato mais direto, desde cursos livres e conteúdos online até o programa Geração Caldeira (trilha de programação Python voltada para análise de dados), passando por estudos pessoais de engenharia de dados. Também tive contato com **JavaScript** e **PHP** durante um curso de desenvolvimento web full stack no IOS, embora não tenha exercitado essas duas recentemente. Na faculdade de ADS, além de um pouco de **Java**, estou vendo **R** e Python na disciplina de Ciência de Dados e Big Data.

## 2. Você já usou git?

Sim, uso git no dia a dia. Utilizo para versionamento de todos os meus projetos pessoais e acadêmicos, incluindo este.

## 3. Como você explicaria para uma pessoa leiga o que é um banco de dados?

Um banco de dados é como um grande arquivo (aqueles armários de metal) organizado em gavetas e pastas cada gaveta guarda um tipo de informação (clientes, produtos, pedido) e cada pasta dentro da gaveta é um registro individual e a diferença de uma planilha comum é que o banco de dados consegue relacionar as informações entre as gavetas de forma automática e muito rápida, por exemplo, saber instantaneamente todos os pedidos de um determinado cliente, mesmo havendo milhões de registros.

## 4. O que é uma variável na programação?

Uma Variável é como um espaço reservado onde iremos atribuir um valor (o dado, podendo ser um número, um texto, etc) e poder utilizar esse mesmo valor em determinados pontos de um código, podendo ser um valor fixo ou não.


## 5. Analisando o seu código, escolha um princípio de programação que melhor te define.

**DRY (Don't Repeat Yourself)** Busquei evitar repetição utilizando os recursos que o Django e o DRF oferecem: `ModelViewSet` para gerar automaticamente todas as operações CRUD sem reescrever a lógica em cada view, `ModelSerializer` para derivar a serialização direto dos models, e o `DefaultRouter` para gerar as rotas automaticamente a partir dos viewsets registrados, cada decisão buscou escrever menos código e reaproveitar ao máximo o que o framework já oferece.

## 6. Conte um problema que já resolveu com programação e qual foi o maior desafio envolvido.

Criei uma mini projeto pessoal de finanças para meu uso exclusivo. Sentia a necessidade de ter um lugar onde pudesse visualizar de forma geral todo o meu controle de gastos, entender para onde o dinheiro estava indo e ter mais margem para economizar e guardar mais. Esse projeto vem me ajudando bastante no dia a dia.

O maior desafio foi definir uma regra de negócio que realmente funcionasse para mim, já que eu era ao mesmo tempo o desenvolvedor e o único usuário final. Tive dificuldade em abstrair minhas próprias necessidades, mas o processo me ensinou muito sobre como pensar em requisitos antes de sair codando.
