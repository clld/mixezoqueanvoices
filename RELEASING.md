# Releasing clld/papuanvoices

* data is located [here](https://github.com/lexibank/mixezoqueanvoices).  

* create the database (with data repo in `./mixezoqueanvoices-cldf/`)
  ```shell
  clld initdb --cldf ../mixezoqueanvoices-cldf/cldf/cldf-metadata.json --glottolog ../../glottolog/glottolog development.ini
  ```

* run tests
  ```shell
  pytest
  ```

* deploy
  ```
  (appconfig)$ appconfig appdeploy mixezoqueanvoices
  ```
