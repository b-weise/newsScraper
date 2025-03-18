# NewsScraper

#### Simple News Scraping CLI Tool

NewsScraper is a small command-line tool designed to extract news articles based on keyword searches.

#### Selection Criteria

Articles are selected if the given search string appears in either the *title* or *body*.

#### Extracted Data

The scraper retrieves the following article details:

- *Article URL*
- *Publication Date*
- *Title*
- *Author*
- *Main Image URL*
- *Description* / *Body*

Currently, NewsScraper only supports data extraction from [P12](https://www.pagina12.com.ar).  
However, it was built with modularity in mind, (hopefully) making it easier to extend support to other sources.

---

### Usage

NewsScraper's usage is well described in the *argparse* help message:

```commandline
$ python cli.py -h
usage: cli.py [-h] [-o [OUTPUT]] [-I] [-R] [-H] [-t [TIMEOUT]] [-n [NAV_TIMEOUT]] [-c [CHUNK_SIZE]] keyword

P12 articles scraper.

positional arguments:
  keyword               Keyword to search for.

options:
  -h, --help            Show this help message and exit.
  -o [OUTPUT], --output [OUTPUT]
                        Path to the SQLite database where the output is stored.
  -I, --case_sensitive  Perform a case-sensitive search.
  -R, --disable_throttling
                        Disable request throttling.
  -H, --headfull        Launch a headful browser.
  -t [TIMEOUT], --timeout [TIMEOUT]
                        Default timeout in seconds.
  -n [NAV_TIMEOUT], --nav_timeout [NAV_TIMEOUT]
                        Default navigation timeout in seconds.
  -c [CHUNK_SIZE], --chunk_size [CHUNK_SIZE]
                        Default throttling chunk size.
```

A basic session would look like this:

``` commandline
$ python cli.py "Genética" -I
New user-agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.
P12 robots.txt has been loaded
Candidate articles found: 10
Scraping: https://www.pagina12.com.ar/514200-tolerancia-cero-eliminar-el-alcohol-en-sangre-lleva-su-tiemp
Scraping: https://www.pagina12.com.ar/776575-las-universidades-siguen-en-lucha-hoy-realizan-109-clases-pu
Scraping: https://www.pagina12.com.ar/525264-estados-unidos-desarrollan-un-collar-inteligente-que-podria-
Scraping: https://www.pagina12.com.ar/560581-inter-miami-anuncio-una-coleccion-limitada-de-camisetas-en-c
Scraping: https://www.pagina12.com.ar/792470-cientificos-rusos-hallan-a-la-bebe-mamut-mejor-conservada-de
Scraping: https://www.pagina12.com.ar/297460-nobel-de-quimica-que-camino-abren-las-tijeras-moleculares
Scraping: https://www.pagina12.com.ar/313843-2020-el-ano-que-la-pandemia-lo-fue-todo-y-la-nueva-politica-
Scraping: https://www.pagina12.com.ar/195478-agendapsi
Scraping: https://www.pagina12.com.ar/309722-coronavirus-un-proyecto-cientifico-argentino-fue-premiado-po
Scraping: https://www.pagina12.com.ar/505770-un-estudio-identifico-las-variantes-geneticas-que-predispone
Matched: https://www.pagina12.com.ar/505770-un-estudio-identifico-las-variantes-geneticas-que-predispone
Matched: https://www.pagina12.com.ar/195478-agendapsi
Matching articles found: 2
```

The results can then be found in the database file as well. In this case, in the default filepath: `p12_scraper.db`.

---

### Implementation Details

This repo's commits aim to follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary) guidelines,
including [Semantic Versioning](https://semver.org/), with some additional types borrowed from [here](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13#types).

*Publication Date* is extracted in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format.  
Plain text fields (excluding URLs) are sanitized by removing:

- Surrounding whitespace
- Blank lines
- [Non-breaking spaces](https://en.wikipedia.org/wiki/Non-breaking_space)

#### Basic Block Prevention Measures

To minimize the risk of being blocked, the scraper includes:

- *User-Agent* spoofing
- Request throttling
- Compliance with the site's `robots.txt`

The scraper follows general guidelines as outlined by [Google](https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt#create_rules).  
A collection of common `robots.txt` directives can be found [here](https://en.wikipedia.org/wiki/Robots.txt#Examples).

#### Concurrency

Parallelization is used in two areas:

- Scraping multiple articles simultaneously using separate browser tabs.
- Extracting different parts of an article concurrently.

#### Dependencies

The required dependencies as listed in `requirements.txt`:

```
pandas
playwright
psycopg2-binary
pytest
pytest-asyncio
sqlalchemy
```

---

### Project Structure

Here’s an overview of the most relevant project files:

### `website_handler.py`

Handles core website interactions, including:

- `robots.txt` compliance
- *User-Agent* handling
- Browser tab management

To generate a realistic *User-Agent*, the scraper retrieves a list from [useragents.me](https://www.useragents.me/) and
selects one randomly.  
Currently, this process runs once per execution.

### `base_news_scraper.py`

Defines generic scraping logic and provides a structure for specific implementations.

- Implements common functionality such as text sanitization and request throttling.
- Wraps **WebsiteHandler** interactions, abstracting them from subclasses.
- Acts as a base class and a "pseudo-interface" by defining abstract methods that subclasses must implement.

### `p12_scraper.py`

Implements the **BaseNewsScraper** interface with logic specific to [P12](https://www.pagina12.com.ar).

The most notable method here is **search**, which:

1. Builds the search URL using the site's internal search engine.
2. Scrapes the search results.
3. Performs a case-configurable string search to identify strict matches.

### `base_storage_manager.py`

Defines an interface for storage management.

At this stage, it only specifies abstract methods, as there isn’t enough shared logic to justify an implementation.

### `db_manager.py`

Implements **BaseStorageManager**. Handles basic *SQLite* database interactions.

Currently, *SQLite* is the only supported storage option.  
A "CSVManager" alternative would be suitable to improve (and challenge) modularity.

### Additional Files

Other noteworthy files include:

`cli.py` – The main entry point of the application, handling command-line interaction.

`db_tables.py` – Defines database tables using *SQLAlchemy*.

---

### Known Issues & Limitations

This project is a work in progress, and several areas still need improvement:

- Currently, a fresh *User-Agent* list is retrieved on every execution.
  - A better approach would be storing them with timestamps and refreshing periodically (e.g., once a week).

- Right now, only articles from the first page of search results are retrieved.
  - Pagination should be implemented to fetch results from multiple pages.

- Requests are currently throttled in batches, waiting only for part scrapers to complete.
  - A more robust implementation should also introduce a timed delay.

- Some articles are compilations of previous news and often lack a body.
  - These are currently ignored but should be scraped properly.

- *SOCI@S* articles are partially scraped but often discarded due to the second, stricter search.
  - A better strategy is needed to handle them.

- No formal tests have been implemented for CLI interactions yet.
