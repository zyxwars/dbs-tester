import json
import sys
import time

import jinja2
import psycopg
import tabulate

import config

# TODO: install dependencies
# pip install Jinja2 "psycopg[binary]" tabulate


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            'Usage: python runner.py 6.sql \'{"first_name": "LeBron", "last_name": "James"}\''
        )
        sys.exit(1)

    print(sys.argv[2])

    env = jinja2.Environment(loader=jinja2.FileSystemLoader("./"))

    with psycopg.connect(
        f"dbname=nba user={config.DB_USER} password={config.DB_PASSWORD}"
    ) as conn:
        with conn.cursor() as cur:
            template = env.get_template(sys.argv[1]).render(json.loads(sys.argv[2]))

            execution_start_time = time.time()
            cur.execute(template)
            execution_end_time = time.time()
            execution_time = execution_end_time - execution_start_time

            res_col_names = [desc[0] for desc in cur.description]
            res = cur.fetchall()

            print(
                tabulate.tabulate(
                    res,
                    headers=res_col_names,
                    tablefmt="psql",
                    showindex=range(1, len(res) + 1),
                )
            )
            print(f"({len(res)} rows) ({execution_time:.2f}s)\n")
