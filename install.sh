#!/bin/bash
sudo apy -y update
sudo apt -y install git

password="$(cat pass.txt)"

echo "Senha git: $password"


git config --global user.email "matheuscarvalhocogo@gmail.com"
git config --global user.name "Matheus Cogo"

echo "Instalando backend em flask..."

flask="$(echo "https://matheuscogo:$password@github.com/matheuscogo/sistematcc.flask.git")"

echo "Clonando projeto flask do repostório..."
echo "Repostório: $flask"

git clone "$flask"

cd ./sistematcc.flask

echo "Instalando dependencias do python"
sudo apy -y update
sudo apt -y install python
sudo apt -y install python3
sudo apt -y install python3-pip
sudo apt -y install python3-venv 

python3 -m venv .venv

source .venv/bin/activate

pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt

cd ..

echo "Instalando frontend em react..."

react="$(echo https://matheuscogo:$password@github.com/matheuscogo/vult.git)"

echo "Clonando projeto react do repostório..."
echo "Repostório: $react"

git clone "$react"

cd ./vult

echo "Instalando dependencias do react"
sudo apy -y update
sudo apt -y install nodejs

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm

nvm install
npm install --global yarn
yarn

echo "Instalando sensores..."

sensors="$(echo "https://matheuscogo:$password@github.com/matheuscogo/sistematcc.sensors.git")"

echo "Clonando projeto react do repostório..."
echo "Repostório: $sensors"

git clone "$sensors"

cd ./sistematcc.sensors

echo "Instalando dependencias do python"
sudo apy -y update
sudo apt -y install python
sudo apt -y install python3
sudo apt -y install python3-pip
sudo apt -y install python3-venv 

python3 -m venv .venv

source .venv/bin/activate

pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt

cd ..


code /home/matheuscogo/projects/sistematcc.flask 
code /home/matheuscogo/projects/sistematcc.sensores 
code /home/matheuscogo/projects/sistematcc.react 
