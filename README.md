# 🔎 Achados e Perdidos

Mini aplicação web desenvolvida com **Python, Flask e SQLite** para criar um mural de objetos perdidos e encontrados.

## Funcionalidades

- Cadastrar item perdido ou encontrado
- Informar nome, descrição, local e contato
- Upload de imagem
- Visualizar todos os itens cadastrados
- Filtrar por **Todos**, **Perdidos** ou **Encontrados**
- Buscar por palavra-chave
- Marcar itens como **Resolvidos/Devolvidos**
- Mensagens de feedback para as ações do usuário
- Banco de dados SQLite criado automaticamente

## Tecnologias

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript

## Como executar

### 1. Clone o repositório

```bash
git clone URL_DO_SEU_REPOSITORIO
cd achados-perdidos
```

### 2. Crie um ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute

```bash
python app.py
```

Depois, abra no navegador:

```text
http://127.0.0.1:5000
```

O arquivo `achados.db` será criado automaticamente na primeira execução.

## Estrutura

```text
achados-perdidos/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   └── cadastrar.html
└── static/
    ├── style.css
    ├── script.js
    └── uploads/
```

## Observação

Este projeto foi feito como um mini app acadêmico de Achados e Perdidos. Para uso real em produção, seria recomendado adicionar autenticação, validação mais avançada dos arquivos e proteção adicional dos dados de contato.
