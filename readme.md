# b5

An EC graph data store with a built-in query engine. This is a 'toy' project now and should not be used seriously.

## structure
All data is stored in [table, ID, key, value] format. On writing, the time stamp is written between the ID and the key. Data cannot be overwritten. If write conflicts need to be resolved, it can be decided by the application. There is one built-in function to get the last written value for a key. 

## querying
Queries have two parts: a list of variables to get, and a list of chained queries. Variables are strings that start with ?, and literals are everything else. 

For example, to get a list of soups made in Ohio, by name, you would do:

```
.query(["?soupName"], [["soup", "?soupId", "?t1", "name", "?soupName"], ["soup", "?soupId", "?t2", "mfg", "?mfgId"], ["mfg", "?mfgId", "?t3", "state", "Ohio"]])
```


