# Python Developer Assignment

## Project Structure

```

.
├── app.py            # Main application entry point
├── clean.py          # Data cleaning logic and export of anomalies to output folder
├── normalize.py      # Normalization of tables and export to output folder
├── utils.py          # Helper functions, including JSON Lines export logic
├── assignment_input.csv  # Input data (keep private)
├── output/           # Folder for exported JSON Lines files
└── test/             # Unit tests for clean.py, normalize.py, etc.

````

---


## Setup

1. Place the `assignment_input.csv` file in the **project root folder**.  
   *(Was instructed to keep it private.)*

2. Install required packages:

```bash
pip install pandas pytest
````

---

## Run Instructions

To process the data and export JSON Lines outputs:

```bash
python app.py
```

* Outputs will be saved in the `output/` folder.

---

## Run Unit Tests

From the project root folder:

```bash
PYTHONPATH=. pytest
```

This will run all tests in the `test/` folder.

---

## Notes

* All outputs are in **JSON Lines (`.jsonl`)** format.
* Anomalies in the data (negative values etc) are exported alongside cleaned data.
* Version was built under “you should not spend more than an afternoon on this” constraint; would normally require more time to refine and test for production
* Documentation generated with AI assistance for clearance.
