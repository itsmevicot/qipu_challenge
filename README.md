# Desafio Qipu

## Descrição do desafio
O desafio consistiu em dois exercícios:
* Criação de uma [lista encadeada (linked list)](linked_list.py) em Python.
* Criação de um crawler para capturar informações da [AISWEB - Informações Aeronáuticas do Brasil.](https://aisweb.decea.mil.br/)

## Configuração do projeto

### Tecnologias
- Python 3.9
- Django 4.2.6
- Banco de dados PostgreSQL 16.0
- Docker (opcional)
- BeautifulSoup 4.12.2
- Requests 2.31.0

### Passos para execução

1. Clone o repositório.

2. Crie um ambiente virtual:
> python -m venv venv

3. Entre no ambiente (Windows):
> venv\Scripts\activate

4. Instale as dependências do projeto:
> pip install -r requirements.txt

5. Configure o banco de dados do projeto:  

* Nessa etapa, vá até a [raiz do projeto Django](qipu) e localize o arquivo [local_settings_sample.py](qipu/local_settings_sample.py). Utilize-o como base para configurar seu banco PostgreSQL ou verifique as outras opções disponíveis na [documentação do Django](https://docs.djangoproject.com/en/4.2/ref/databases/).
* ATENÇÃO: caso opte por algum outro banco de dados, talvez seja necessário realizar a instalação de outros pacotes.
* Crie um arquivo local_settings.py seguindo o exemplo. Você pode passar a SECRET_KEY do projeto tanto no arquivo local_settings.py quanto nas variáveis de ambiente. Você pode checar o exemplo de arquivo de variáveis de ambiente [aqui](.env_example).
* Caso deseje gerar uma nova SECRET_KEY, você pode utilizar o próprio Django para isso, seguindo os passos:
1. Abra o shell do Django com o comando:
> python manage.py shell

2. Execute o comando:
> from django.core.management.utils import get_random_secret_key

3. Chame a função:
> get_random_secret_key()

4. Copie a saída do comando e cole no arquivo local_settings.py ou nas variáveis de ambiente.

Com o banco configurado, aplique as migrações do projeto:
> python manage.py migrate

Para iniciar o projeto, utilize o seguinte comando:
> python manage.py runserver

### Docker
O projeto inclui um docker-compose.yml, tornando mais prática a inicialização do banco de dados. Para rodar via Docker, utilize:
> docker-compose up -d

Certifique-se de que o arquivo .env e o local_settings.py estejam configurados corretamente antes de iniciar o container, pois eles informarão ao docker-compose as variáveis a serem utilizadas.

### Funcionamento
Ao iniciar o projeto, você poderá acessar a página inicial em http://localhost:8000/. Nela, você encontrará um formulário para inserir o código ICAO de um aeroporto. 
A lista de códigos ICAO completa pode ser encontrada na [Wikipedia](https://pt.wikipedia.org/wiki/Lista_de_aeroportos_do_Brasil_por_c%C3%B3digo_aeroportu%C3%A1rio_ICAO).
Ao submeter o formulário, caso seja um código válido e existente, o scraper irá trazer algumas informações do aeroporto. Caso contrário, um erro é informado ao usuário.
É possível informar mais de um código ICAO por vez, separados por vírgula.

São informados:
* Código ICAO
* Data 
* Dia da semana
* Hora do nascer do sol
* Hora do pôr do sol
* METAR e TAF. Consulte [aqui](https://ajuda.decea.mil.br/base-de-conhecimento/como-decodificar-o-metar-e-o-speci/) para aprender a traduzir essas informações.
* Cartas aeronáuticas com localidade, tipo, carta, amdt, data da efetivação e uso

### Observação
* É normal um aeródromo não ter todas as informações (como não possuir cartas ou METAR/TAF). Nesses casos, o scraper irá retornar apenas as informações disponíveis.
* Para esse projeto, não houve um grande foco no front-end da aplicação, já que não era esse o objetivo.
