# Projeto de Web Scraping usando Scrapy

Este é um projeto simples de web scraping utilizando o framework Scrapy para coletar informações de portos brasileiros. O projeto está estruturado de forma que uma única spider (`HarborShips`) realiza o scraping de dois sites diferentes relacionados aos portos de Paranaguá e Santos. Os dados coletados são salvos em um formato JSON, CSV e também em um banco de dados MySQL.


## Estrutura do Projeto

- **`desafio/spiders/harbor_ships.py`**: Contém a spider principal (`HarborShips`) que realiza o web scraping dos sites relacionados aos portos.
- **`desafio/items.py`**: Define a estrutura do item (`Product`) que armazena os dados coletados.
- **`desafio/pipelines.py`**: Implementa pipelines para processar e salvar os dados coletados em JSON, CSV e MySQL.
- **`scrapy.cfg`**: Configuração principal do Scrapy.
- **`requirements.txt`**: Lista de dependências do projeto.

## Web Scraping Assíncrono

A escolha de utilizar uma única spider para realizar o scraping de dois sites diferentes simplifica a estrutura do projeto. A função `start_requests` inicia o scraping para ambos os sites assincronamente, aproveitando o suporte embutido do Scrapy para operações assíncronas.

## Uso de JSON e CSV

Duas pipelines (`JsonWriterPipeline` e `CSVWriterPipeline`) foram implementadas para salvar os dados coletados em formato JSON e CSV, respectivamente. Esses formatos são comumente utilizados para exportar dados tabulares e são facilmente processados por outras ferramentas.

## Uso de MySQL para Salvar Dados

A pipeline `MySqlPipeline` foi implementada para salvar os dados coletados em um banco de dados MySQL. Isso permite uma persistência eficiente dos dados, facilitando consultas futuras e análises mais avançadas.

## Como Executar o Projeto

### Requisitos

- Python 3.6 ou superior
- Scrapy
- MySQL Server
- Bibliotecas adicionais (consulte o arquivo `requirements.txt`)

### Passo a Passo

1. Clone o repositório:

   ```bash
   git clone https://github.com/Pedro-Tuto/Scraping-Harbor-Sites
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco de dados MySQL:

   - Crie um banco de dados chamado `db_merchandise`.
   - Atualize as configurações de conexão no arquivo `mysql_data.py (host, usuário, senha).

4. Execute a spider:

   ```bash
   cd desafio
   scrapy crawl harbor_ships
   ```

   Isso iniciará o processo de scraping e os dados serão salvos nos formatos JSON, CSV e no banco de dados MySQL.

