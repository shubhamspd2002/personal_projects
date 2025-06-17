# biogrid

1. Open https://thebiogrid.org/ read documentation
2. Down load `BIOGRID-CORONAVIRUS-4.4.242.tab3.zip`
3. unzip and explore the data

## List of useful pandas functions:

```python
COLUMNS = [
    "#BioGRID Interaction ID",
    "Official Symbol Interactor A",
    "Official Symbol Interactor B",
    "Experimental System",
    "Experimental System Type",
    "Organism ID Interactor A",
    "Organism ID Interactor B",
    "Organism Name Interactor A",
    "Organism Name Interactor B",
    "Score",
    "SWISS-PROT Accessions Interactor A",
    "SWISS-PROT Accessions Interactor B",
]```

Disclaimer: Before you use any of the functions, look up the exact documentation of the function in the official pandas docs!
- read_csv(): Loads csv file to dataframe
- df.rename(): Renames columns in dataframe by dictionary
- df.replace(): Replaces specific values in df with new values
- df.notna(): Mask of bool values for each element in Series/DataFrame that indicates whether an element is not an NA value.
- concat(): merge two Series/Dataframes into 1
- df.drop_duplicates(): Returns df with duplicates removed
- df.reset_index(): Resets index of dataframe

List of useful SQLAlchemy functions:
```python
with self.Session.begin() as session:
    #some operations with session
```
Opens up a session you can now query results from database
- session.add(Object): adds an object to db
- session.flush(): Writes out all pending object creations, deletions and modifications to the database as INSERTs, DELETEs, UPDATEs, etc. Operations are automatically ordered by the Session's unit of work dependency solver.
