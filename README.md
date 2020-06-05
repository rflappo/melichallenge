# README for the Mercado Libre (BI) Python code challenge


## Development Setup and Configuration

### Install prerequisites:
Required prerequisites
* [Docker](https://docs.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

Suggested prerequisite
* [Mini Conda](https://docs.conda.io/en/latest/miniconda.html)


### Clone the repo
```bash
git clone https://github.com/rflappo/melichallenge.git
cd melichallenge
```

### Running
1. Build and run the containers, so the db is up & ready.
```bash
docker-compose -f docker-compose.yml up -d --build
docker ps
```

2. Create your dev env. with `python=3.8` and activate it:
> pip install -r requirements.txt

3.  Load the folowing env vars:
```
FLASK_APP='app.__init__.py'
APP_SETTINGS='app.config.DevelopmentConfig'
DATABASE_URL='postgres://melichallenge:melichallenge@127.0.0.1:54320/melichallenge'
```

4. Run the app:
```bash
python manage.py run
```

If with `mini-conda` and on `linux`:
* Just for the first time:
```bash
docker-compose -f docker-compose.yml up -d --build

conda create --name meli-challenge python=3.8 pip
conda activate meli-challenge

pip install -r requirements.txt

sudo chmod +x run.sh
./set-up.sh
```
* To run the app:
```bash
./run.sh
```
