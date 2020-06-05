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
--------
If with `mini-conda` and on `linux`:
* Just for the first time:
```bash
conda create --name meli-challenge python=3.8 pip
conda activate meli-challenge

pip install -r requirements.txt
```
--------

3. Run the app:
 > Load the folowing env vars:
```
FLASK_APP='app.__init__.py'
APP_SETTINGS='app.config.DevelopmentConfig'
DATABASE_URL='postgres://melichallenge:melichallenge@127.0.0.1:54320/melichallenge'
```

> Run the app:
```bash
python manage.py run
```
--------
If on `linux`,  just:
```bash
sudo chmod +x run.sh
./run.sh
```
--------
--------


## About the parsing
There is a file to config how the parsing will work.
> parserconfig.ini

`EXTENSION` will set the expected/allowed extension for the file

For extensions like `jsonl` (json line), or any extension that makes the line a little harder to parse, you can use `MODULE` and `METHOD` vars to specify a python module's methods to use when parsing the line.
For `csv` or `txt` formats, where lines are parsed simply by splitting, you should set the `SEPARATOR` value. Please remove `MODULE` & `METHOD` vars or set them with "None".

### Examples


* For **csv**: `parserconfig.ini`
```inifile
[FILE]
ENCODING = utf-8
HEADERS_LINE = true
EXTENSION = csv

[LINE]
SEPARATOR = ,
LINE_FEED = unix
MODULE = None
METHOD = None
```


* For **jsonl**: `parserconfig.ini`
```inifile
[FILE]
ENCODING = utf-8
EXTENSION = jsonl

[LINE]
LINE_FEED = unix
MODULE = json
METHOD = loads
```
