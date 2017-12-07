# Expected Input format

```python
Grammar = {
    'METHOD_BODY': [
        [
            ('STATEMENT_LIST', 'n')
        ]
    ],
    'STATEMENT_LIST': [
        [
            ('STATEMENT', 'n')
        ],
        [
            ('STATEMENT_LIST', 'n'),
            ('STATEMENT', 'n')
        ],
        [
            (None, 't')
        ]
    ],
    'STATEMENT': [
        [
            ('DECLARATION', 'n')
        ],
        [
            ('IF', 'n')
        ],
        [
            ('WHILE', 'n')
        ],
        [
            ('ASSIGNMENT', 'n')
        ]
    ],
    'DECLARATION': [
        [
            ('PRIMITIVE_TYPE', 'n'),
            ('id', 't'),
            (';', 't')
        ]
    ],
    'PRIMITIVE_TYPE': [
        [
            ('int', 't')
        ],
        [
            ('float', 't')
        ]
    ],
    'IF': [
        [
            ('if', 't'),
            ('(', 't'),
            ('EXPRESSION', 'n'),
            (')', 't'),
            ('{', 't'),
            ('STATEMENT', 'n'),
            ('}', 't'),
            ('else', 't'),
            ('{', 't'),
            ('STATEMENT', 'n'),
            ('}', 't'),
        ]
    ],
    'WHILE': [
        [
            ('while', 't'),
            ('(', 't'),
            ('EXPRESSION', 'n'),
            (')', 't'),
            ('{', 't'),
            ('STATEMENT', 'n'),
            ('}', 't')
        ]
    ],
    'ASSIGNMENT': [
        [
            ('id', 't'),
            ('=', 't'),
            ('EXPRESSION', 'n'),
            (';', 't')
        ]
    ]
}
``` 

# Expected Output format

```python
First = {
    'ASSIGNMENT': ['id'],
    'WHILE': ['while'],
    'IF': ['if'],
    'PRIMITIVE_TYPE': ['int', 'float'],
    'DECLARATION': ['int', 'float'],
    'STATEMENT': ['int', 'float', 'if', 'while', 'id', None],
    'STATEMENT_LIST': ['int', 'float', 'if', 'while', 'id', None],
    'METHOD_BODY': ['int', 'float', 'if', 'while', 'id', None]
}
```
