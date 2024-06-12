# Releasing clld/mixezoqueanvoices

* dataset is located [here](https://github.com/lexibank/mixezoqueanvoices).  

* create the database (with data repo in `./mixezoqueanvoices-data/`)
  ```
  clld initdb --cldf ./mixezoqueanvoices-data/cldf/cldf-metadata.json --glottolog <local-glottolog-repo> development.ini
  ```

* run tests
  ```
  pytest
  ```

* deploy
  ```
  (appconfig)$ fab deploy:production
  ```
