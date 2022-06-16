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
  

## Para executar
1. Clone esse repositorio
2. Entre no diretório do projeto e execute o comando
	`sudo docker stack deploy -c docker-compose.yaml monitor`

## Design da Solução
Na solução desse problema foi utilizado o Prometheus, Grafana, Docker, Docker-Compose e Python

![Arquitetura do desafio](https://media.discordapp.net/attachments/987084289214668892/987084708515053658/arquitetura-gabriel.png)

pipipi popopo
### Software de simulação do agente
pipipi popopo
