## Jinja 2 template tester for DBS

-  ```pip install Jinja2 "psycopg[binary]" tabulate```
- Create config.py by following config.example.py
- The tester needs to be in the same folder as the sql files
- The tester checks the validity of column names and first row values

tester.py validates all files sequentially\
runner.py is used for getting the output of a single file without any validation
