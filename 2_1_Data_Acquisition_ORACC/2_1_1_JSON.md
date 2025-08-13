## 2.1.1 The JSON Data Format

:::{margin}
See http://oracc.org/doc/opendata/json/index.html for a description of the ORACC JSON files.
:::

JavaScript Object Notation, or [JSON](http://www.json.org) is recognized as a lightweight but very versatile data structure. Databases (and `.csv` files) need a fixed number of fields; key/value combinations in JSON can be extended at will. Representation of hierarchical structures is very natural in JSON, but is complex in (relational) databases. We will see that [ORACC](http://oracc.org) JSON makes extensive use of hierarchies. The two characteristics mentioned here (extensibility and hierarchical structure) are shared with XML, which is in many ways similar to JSON. Generally, JSON is considered to be lighter (smaller files) and more efficient, because the data structure is very closely aligned to data structures in common programming languages such as JavaScript, Python, and R. 

The contents of a valid JSON file are wrapped in curly brackets, very similar to a Python dictionary, and consist of `"key" : "value"` pairs, as in:

```json
{"id_text": "P334930", "designation": "SAA 03, 001"}
```

In a `"key" : "value"` pair, keys are always strings. Values may be string, number, boolean (true or false), list, or another dictionary. A list is wrapped in square brackets and may look like this:

```json
["ABRT 1 32", "SAA 03, 001"]
```

A dictionary is wrapped in curly brackets and consists, again, of `key`: `value` pairs.

The following is an (abbreviated) example of a JSON file (the catalog of an imaginary [ORACC](http://oracc.org) project) that illustrates the format:

```json
{"members": {
		"P334930": {
			"id_text": "P334930",
			"designation": "SAA 03, 001",
			"publications": ["ABRT 1 32", "SAA 03, 001"]
		},
		"P334929": {
			"id_text": "P334929",
			"designation": "SAA 03, 002",
			"publications": ["ABRT 1 29", "SAA03, 002"]
		}
	}
}
```

The value of the key `members` is a dictionary (surrounded by curly brackets) with length of 2. The value of each key in this dictionary is again a dictionary (surrounded by curly brackets and consisting of `key` : `value` pairs). The key `publications` has a list as its value. A list is a way to associate multiple values with a single key - in this case the multiple publications of a single text. In `publications`  the values inside the list are strings (surrounded by quotation marks), but they may be of any data type, including lists or dictionaries. This allows for very complex trees with a minimal arsenal of data structures.

:::{margin}
For a more formal and more complete description of the JSON data structure see [http://www.json.org/](http://www.json.org). 
:::

:::{important}
For all practical purposes, a JSON object is identical in structure to a Python dictionary, but the naming conventions are slightly different. To avoid confusion, we use the Python vocabulary here (key, list, dictionary), even when talking about JSON data structures.

| JSON   | Python     | Surrounded by | Defined as                                                   |
| ------ | ---------- | ------------- | ------------------------------------------------------------ |
| object | dictionary | {}            | unordered sequence of name/value pairs                       |
| array  | list       | []            | ordered sequence of values                                   |
| value  | value      |               | string, number, boolean, list (= array), or dictionary (= object) |
| name   | key        |               | string                                                       |

:::