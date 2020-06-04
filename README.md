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
```

### Running
If with `mini-conda` and on `linux`:
* Just for the first time:
```bash
sudo chmod +x set-up.sh && sudo chmod +x run.sh
./set-up.sh
```
* To run the app:
```bash
./run.sh
```

If `NOT` ( with `mini-conda` and on `linux`):

* Build and run the containers, so the db is up & ready.
```bash
docker-compose -f docker-compose.yml up -d --build
docker ps
```

* Create your dev env. with `python=3.8` and:
> pip install -r requirements.txt

*  Load the folowing env vars:
```
FLASK_APP='app.__init__.py'
APP_SETTINGS='app.config.DevelopmentConfig'
DATABASE_URL='postgres://melichallenge:melichallenge@127.0.0.1:54320/melichallenge'
```

* Activate your dev env.
* Run the app:
```bash
python manage.py run
```