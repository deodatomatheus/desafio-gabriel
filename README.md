# Desafio Técnico - Gabriel
Este é um desafio da equipe de IoT da Gabriel. A tarefa consiste em criar um sistema de monitoramento de dispositivos afim de reportar falhas a equipe de suporte.

## Dependências

Para executar este projeto é necessário instalar algumas dependências, os comandos abaixo são para Ubuntu 20.04

1. **Docker**
    Instale com :
    1. `sudo apt-get update`
    
    2. `sudo apt-get install ca-certificates curl gnupg lsb-release`
    
	3. `sudo mkdir -p /etc/apt/keyrings`
	
	4.  `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo 
gpg --dearmor -o /etc/apt/keyrings/docker.gpg`

	5. `echo  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`

	6.  `sudo apt-get update`
	
	7. `sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin`
	
	Caso queira testar se a instalação foi bem sucedida: 
	* `sudo docker run hello-world`
	
	[Para mais informações sobre a instalação do docker clique aqui](https://docs.docker.com/engine/install/ubuntu/)
2. **Docker Compose**
	Instale com :
	1. `apt-get update -y`
	
	2. `apt-get install docker-compose`

	[Para mais informações sobre a instalação do docker-compose clique aqui](https://linuxhostsupport.com/blog/how-to-install-and-configure-docker-compose-on-ubuntu-20-04/)
  

## Design da Solução
Na solução desse problema foi utilizado o Prometheus, Grafana, Docker, Docker-Compose e Python e Slack

![Arquitetura do desafio](https://media.discordapp.net/attachments/987084289214668892/987339847645663282/arquitetura-gabriel.drawio_3.png)

Os dados são gerados por uma aplicação em python, que é replicadas em vários containers. 

Esses containers estão cadastrados no container do Prometheus, que por sua vez armazena as métricas dos dispositivos monitorados.

A interface de visualização utilizada foi o Grafana, por já possuir suporte ao banco de dados do Prometheus. O grafana está responsável por gerar alertas e enviálos a um canal no Slack.

A stack de containers está em uma mesma rede, que é criada no arquivo do docker-compose.

### Aplicação em python

A aplicaçao consiste em um servidor http para publicar as metricas, e um conjunto de threads que simulam o comportamento das cameras e hds.

É possível passar alguns argumentos para essa aplicação para mudar alguns parametros:

Quantidade de threads de camera: 
    `-c 4`

Quantidade de threads de hd: 
    `-h 1`

Probabilidade da thread entrar em um erro/sair do erro
    `-e 0.05`


### Build da imagem docker
Antes de executar o comando para subir a aplicação, é preciso realizar o build da imagem dos agentes. Realize-o com o seguinte comando: 

`docker build -t python-agent .`

### Arquivos de persistencia de dados do Grafana
Para configurar os arquivos de persistencia do Grafana, execute os seguintes comandos (dentro do diretório do projeto).

`mkdir -p ./etc/grafana/`
`mkdir -p ./data/grafana/`

Em seguida é preciso mudar as permissões dos arquivos:

`sudo chmod -R 777 etc/`
`sudo chmod -R 777 data/`

### Iniciando a aplicação
Para subir os containers, basta executar o comando:
`sudo docker stack deploy -c docker-compose.yaml monitor`

Caso precise encerrar os containers:
`sudo docker stack rm monitor`

As aplicações podem ser acessadas em:
* Grafana: `localhost:80`
* Prometheus: `localhost:9090`
