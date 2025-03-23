## Jinja 2 template tester for DBS


# How to use:
1. **Create a virtual enviroment**
```shell
python -m venv venv
```
2. **Go into the venv**  
* Windows
```shell
venv\Scripts\activate
```
* Linux and MacOS
```shell
source myvenv/bin/activate
```
3. **Install Jinja2 library**
```shell
pip install Jinja2 "psycopg[binary]" tabulate
```
4. **Create `config.py` by following `config.example.py`**
5. The tester needs to be in the same folder as the sql files
- The tester checks the validity of column names and first row values

tester.py validates all files sequentially\
runner.py is used for getting the output of a single file without any validation
