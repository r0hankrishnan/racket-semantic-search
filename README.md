# Tennis Racket Semantic Search

This project explores how semantic search techniques can help users find the right tennis racket using natural language queries.

**This project is a WIP: I am currently exploring different text field combinations and search workflows.**

It includes:

- A web scraper for collecting racket product data
- Embedding generation using the `searchlite` package (*WIP*)
- Cosine similarity–based semantic search with `searchlite` (*WIP*)
- A basic API and frontend interface to run queries and view results (*WIP*)

This project uses the `DataShelf` library to organize and document all raw, intermediate, and final data sets. You can find all data used in any notebooks in the `.datashelf` folder. If you are in the repository, you can run the following to access any dataset in the `racquets` collection:

```python
# List the all data files in the racquets collection (note the hash of the file you want to load)

ds.ls("coll-files") # Enter "racquets" when prompted for collection name

# Load the dataset as a pd.DataFrame based on its hash value

df = ds.load(
  collection_name = "racquets",
  hash_value = <hash>
)
```
All processed data is stored in the `.datashelf/` directory.

## Setup

Clone the repo and install dependencies:

```bash
git clone https://github.com/r0hankrishnan/racket_semantic_search.git
cd racket_semantic_search
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you plan to use an Ollama-based embedding model run:

```bash
pip install searchlite[ollama]
```

instead of:

```bash
pip install searchlite
```

If you are exploring this project well into the future, you may want to scrape Tennis Warehouse's website again in case their listings have changed. You can reference `.datashelf/racquets/racquets_metadata.yaml` file to see the date the raw data was created. To scrape the racquet data from tennis warehouse:

```bash
python run_scraper.py
```

To run the required basic preprocessing operations on the data:

```bash
python run_preprocess.py
```

## Project Structure

* `.datashelf/` – directory of **all** datasets used in project (raw → final)
* `src/` – scraping, embedding, search, display, app code
* `notebooks/` – exploratory analysis and prototyping
* `notebooks/marimo_notebooks/` - marimo notebook equivalents for jupyter noteboks in `notebooks/`
* `tests/` – basic unit tests

## Notes

This is an early-stage data science project focused on experimenting with semantic search in a consumer product context. It is not intended for production or packaging.

