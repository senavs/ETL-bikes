# ROX Challenge
Esse é um teste com o objetivo de conhecer um pouco mais sobre a sua forma de trabalhar com dados e a resolução de problemas que envolvem engenharia de dados.


## Desafio 

### O problema
O presente problema se refere aos dados de uma empresa que produz bicicletas.

### Objetivos
O objetivo deste desafio é compreender os seus conhecimentos e experiência analisando os seguintes aspectos:
  - Fazer a modelagem conceitual dos dados;
  - Criação da infraestrutura necessária;
  - Criação de todos os artefatos necessários para carregar os arquivos para o banco criado;
  - Desenvolvimento de SCRIPT para análise de dados;
  - Criar um relatório em qualquer ferramenta de visualização de dados (opcional).

Com base na solução implantada responda aos seguintes questionamentos:
  - Escreva uma query que retorna a quantidade de linhas na tabela Sales.SalesOrderDetail pelo campo SalesOrderID, desde que tenham pelo menos três linhas de detalhes.
  - Escreva uma query que ligue as tabelas Sales.SalesOrderDetail, Sales.SpecialOfferProduct e Production.Product e retorne os 3 produtos (Name) mais vendidos (pela soma de OrderQty), agrupados pelo número de dias para manufatura (DaysToManufacture).
  - Escreva uma query ligando as tabelas Person.Person, Sales.Customer e Sales.SalesOrderHeader de forma a obter uma lista de nomes de clientes e uma contagem de pedidos efetuados.
  - Escreva uma query usando as tabelas Sales.SalesOrderHeader, Sales.SalesOrderDetail e Production.Product, de forma a obter a soma total de produtos (OrderQty) por ProductID e OrderDate.
  - Escreva uma query mostrando os campos SalesOrderID, OrderDate e TotalDue da tabelaSales.SalesOrderHeader. Obtenha apenas as linhas onde a ordem tenha sido feita durante o mês de setembro/2011 e o total devido esteja acima de 1.000. Ordene pelo total devido decrescente.


## Minha solução

### Requisitos
Para replicar a solução, é necessário ter instalado as seguintes ferramentas e bibliotecas:
  - Git
    - Repositório [ETL-Bikes](https://github.com/senavs/ETL-bikes) clonado. 
  - Kubernetes
    - Cluster configurado com [minikube](https://minikube.sigs.k8s.io/docs/) ou com Masters e Nodes reais.
    - [kubectl](https://kubernetes.io/docs/tasks/tools/).
  - Python 3.8 (ou superior)
    - Interpretador [Python](https://www.python.org/)

### Modelo conceitual
![modelo conceitual do banco de dados](https://github.com/senavs/ETL-bikes/blob/master/database/conceptual/conceptual.png)

### Modelo físico
![modelo físco do banco de dados](https://github.com/senavs/ETL-bikes/blob/master/database/MER/physical.png)

### Instalação das dependências Python.
Obrigatoriamente, para executar os scripts da aplicação, as bibliotecas `numpy`, `pandas`, `sqlalchemy` e `pymysql` devem ser instaladas.

```sh
pip install numpy==1.20.0 pandas==1.2.3 SQLAlchemy==1.4.1 PyMySQL==1.0.2
```

Caso queria rodar os scripts no jupyter notebook, instalar também o `jupyter`.
```sh
pip install jupyter
```

### Cluster
Antes de rodar os scripts de criação das tabelas é necessário criar os componentes do cluster. Qualquer arquitetura cloud que aceite kubernetes pode ser utilizada.

Após clonar o repositório, acessar o terminal e entrar na pasta `ETL-Bikes/kubernetes`
```sh
cd ETL-Bikes/kubernetes
```

Criar o `namespace` padrão da solução.
```sh
kubectl create namespace rox
```

Com isso, basta criar todos os componentes (`configmap`, `secrets`, `deployment` e `services`) para realizar o deploy.
```sh
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Para verificar se todos os componentes foram criados com sucesso, utilize o seguinte comando:
```sh
watch kubectl get all -n rox
```

### Criação das tabelas e ETL
Defina a variável de ambiente `DATABASE_URI` com o IP e porta do seu cluster, para que os scripts de criação/ETL consigam acessar o banco de dados.

```sh
# linux/mac
export DATABASE_URI='mysql+pymysql://root:toor@192.168.99.100:30000/BIKES'

# windows
set DATABASE_URI='mysql+pymysql://root:toor@192.168.99.100:30000/BIKES'
```

Caso esteja utilizando o minekube, você conseguirá `service IP` com o seguinte comando:
```sh
minikube service list
```

**NOTA**: O IP e porta `192.168.99.100:30000` podem variar de acordo com as configurações do cluster. Por padrão, o arquivo `service.yaml` define a porta `30000` como nodePort.

Após configurar criar o container do banco de dados e definição da variável de ambiente, acessar a pasta `ETL-Bikes/scripts` e executar os seguintes comandos Python:
```sh
cd ETL-Bikes/scripts
```

```sh
python3 create.py
python3 etl.py
```

### Análises
