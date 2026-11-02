# Releasing the Mixezoquean Voices clld app

Install the software
```shell
git clone https://github.com/clld/mixezoqueanvoices
git clone --branch v2.0.1 --depth 1 https://github.com/lexibank/mixezoqueanvoices mixezoqueanvoices-cldf
git clone --branch v5.3 --depth 1 https://github.com/glottolog/glottolog
cd mixezoqueanvoices
pip install -e .[test]
```
Recreate the database (with data repo in `../mixezoqueanvoices-cldf/`)
```shell
pip install -e ../mixezoqueanvoices-cldf
clld initdb --cldf ../mixezoqueanvoices-cldf/cldf/cldf-metadata.json --glottolog ../glottolog development.ini
```
run tests
```shell
pytest
```
deploy
Store the tested requirements:
```shell
pip freeze > requirements.txt
```
Store a db dump:
```shell
pg_dump -xO --compress gzip:9 mixezoqueanvoices > mixezoqueanvoices.sql.gz
```

