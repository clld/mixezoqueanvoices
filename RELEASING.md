# Releasing the Mixezoquean Voices clld app

* Install the software
  ```shell
  git clone --depth 1 https://github.com/clld/mixezoqueanvoices
  cd mixezoqueanvoices
  pip install -e .[test]
  ```
* Data is located [here](https://github.com/lexibank/mixezoqueanvoices)
* Recreate the database (with data repo in `../mixezoqueanvoices-cldf/`)
  ```shell
  pip install -e ../mixezoqueanvoices-cldf
  clld initdb --cldf ../mixezoqueanvoices-cldf/cldf/cldf-metadata.json --glottolog ../../glottolog/glottolog development.ini
  ```
* run tests
  ```shell
  pytest
  ```
* deploy
* Store the tested requirements:
  ```shell
  pip freeze > requirements.txt
  ```
* Store a db dump:
  ```shell
  pg_dump -xO mixezoqueanvoices > mixezoqueanvoices.sql
  zip mixezoqueanvoices.sql.zip mixezoqueanvoices.sql
  rm mixezoqueanvoices.sql
  ```

