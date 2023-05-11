# DED-dices
Um site de RPG de mesa para um TCC.

Esse site fazerá todas as operações que um RPG de mesa tem, como criar fichas, fazer testes, criar mapas, etc...

Para rodar esse site no seu PC faça os seguintes passos:

* 1 - Instale o python 3.8
  Na instalação, marque o checkbox de adicionar as variaveis do ambiente
  
* 2 - abra o CMD e digite "python --version"
  Isso é para verificar se o python está instalado corretamente no seu PC, caso não funcione reinstale o python e adicione ele as variaveis do ambiente.
  
* 3 - instale o Xamp
  Ele que vai rodar o servidor do banco de dados
  
* 4 - inicie o servidor
  Abra o Xamp e clique em iniciar mySQL
  
  nota: Se não funcionar abra o gerenciador de tarefas e encerre o processo do mySQL workbanch e tente novamente.
  
* 5 - crie o banco de dados com o nome "ded_banch"
  clique no "admin" do mySQL e você será redirecionado para uma página html, lá você clica no botão de criar um novo banco de dados e coloque o nome "ded_banch"
  
* 6 - com o CMD vá até o diretório onde você instalou o site, vá até onde ta o arquivo chamado "requirements.txt"
  Para ir no diretório com o CMD use o comando "cd" juntamente com o nome da pasta que deseja ir
  EX: cd downloads/sites/ded
  
* 7 - com o cmd no diretório do "requirements.txt" digite os seguintes comandos:
  "pip install virtualenv"
  "virtualenv env"
  "cd env/scripts"
  "activate"
  "cd ../.."
  "pip install -r requirements.txt"
  "python manage.py migrate"
  
  ele irá baixar todos os requisitos para o site funcionar e irá migrar todo o banco de dados.
  
* 8 - rode o servidor
  no CMD rode o seguinte comando:
  "python manage.py runserver"
  
  e depois abra o seu navegador e pesquise por:
  "localhost:8000"
  
  e pronto! o site já estará rodando na sua máquina!
  
  *Para desligar o servidor vá no CMD e aperte Ctrl+C
  