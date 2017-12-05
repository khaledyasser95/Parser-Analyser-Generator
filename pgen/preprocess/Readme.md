# Expected Input format

```
# TERM = FACTOR
| TERM 'mulop' FACTOR
# METHOD_BODY = STATEMENT_LIST
```
# Expected Output format

```python
Grammer = {
	'TERM':[
		[
			('FACTOR', 'n')
		],
		[
			('TERM', 'n'),
			('mulop', 't'), 
			('FACTOR', 'n')
		]
	],
	'METHOD_BODY':[
		[
			('STATEMENT_LIST', 'n')
		]
	]

}
``` 

