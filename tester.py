import time
import argparse
from decimal import Decimal

import jinja2
import psycopg
import tabulate

import config


RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"



# TODO: install dependencies
# pip install Jinja2 "psycopg[binary]" tabulate

# TODO: rounding needs to be checked manually

tests = {
    "1.sql": {
        "input": {"game_id": 22000529},
        "column_names": (
            "player_id",
            "first_name",
            "last_name",
            "period",
            "period_time",
        ),
        "output_first_row": (202696, "Nikola", "Vucevic", 1, "8:22"),
    },
    "2.sql": {
        "input": {"season_id": "22017"},
        "column_names": (
            "player_id",
            "first_name",
            "last_name",
            "team_id",
            "full_name",
            "PPG",
            "APG",
            "games",
        ),
        "output_first_row": (
            202328,
            "Greg",
            "Monroe",
            1610612738,
            "Boston Celtics",
            Decimal("10.82"),
            Decimal("2.27"),
            Decimal("22"),
        ),
    },
    "3.sql": {
        "input": {"game_id": 21701185},
        "column_names": (
            "player_id",
            "first_name",
            "last_name",
            "points",
            "2PM",
            "3PM",
            "missed_shots",
            "shooting_percentage",
            "FTM",
            "missed_free_throws",
            "FT_percentage",
        ),
        "output_first_row": (
            1627759,
            "Jaylen",
            "Brown",
            32,
            4,
            7,
            8,
            Decimal("57.89"),
            3,
            2,
            60,
        ),
    },
    "4.sql": {
        "input": {"season_id": "22018"},
        "column_names": (
            "player_id",
            "longest_streak",
        ),
        "output_first_row": (201566, 9),
    },
    "5.sql": {
        "input": {},
        "column_names": (
            "team_id",
            "team_name",
            "number_away_matches",
            "percentage_away_matches",
            "number_home_matches",
            "percentage_home_matches",
            "total_games",
        ),
        "output_first_row": (
            1610612737,
            "Atlanta Hawks",
            1986,
            Decimal("50.27"),
            1965,
            Decimal("49.73"),
            3951,
        ),
    },
    "6.sql": {
        "input": {"first_name": "LeBron", "last_name": "James"},
        "column_names": (
            "season_id",
            "stability",
        ),
        "output_first_row": ("22007", Decimal("9.84")),
    },
}


def main(print_full_table=False):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("./"))

    with psycopg.connect(
        f"dbname={config.DB_NAME} user={config.DB_USER} password={config.DB_PASSWORD}"
    ) as conn:
        with conn.cursor() as cur:
            for fileName in tests.keys():
                try:
                    template = env.get_template(fileName).render(tests[fileName]["input"])
                except jinja2.exceptions.TemplateNotFound:
                    print(f"{fileName}: ❌ {RED}Template not found. Skipping this test.{RESET}")
                    continue
                print(f"{fileName}: Starting test")

                template = env.get_template(fileName).render(tests[fileName]["input"])

                try:
                    execution_start_time = time.time()
                    cur.execute(template)
                    execution_end_time = time.time()
                    execution_time = execution_end_time - execution_start_time

                    res_col_names = [desc[0] for desc in cur.description]
                    res = cur.fetchall()
                except Exception as e:
                    print(f"{fileName}: {RED}Error in the {fileName} file{RESET}")
                    continue

                if tests[fileName]["column_names"] != tuple(res_col_names):
                    print(f"[{RED}Test Failed{RESET}] {fileName}: Column names don't match")
                    print(
                        f"expected:{tests[fileName]['column_names']} != \n     got:{res_col_names}"
                    )
                    continue

                else: print(f"[{GREEN}Test passed{RESET}] {fileName}: Column names match")
                
                if tests[fileName]["output_first_row"] != res[0]:
                    print(f"[{RED}Test Failed{RESET}] {fileName}: First column values don't match")
                    print(
                        f"expected :{tests[fileName]['output_first_row']} != got:{res[0]}"
                    )
                    continue

                print(f"[{GREEN}Test passed{RESET}] {fileName}: First rows match")

                if print_full_table:
                    print(
                        tabulate.tabulate(
                            res,
                            headers=res_col_names,
                            tablefmt="psql",
                            showindex=range(1, len(res) + 1),
                        )
                    )
                    print(f"({len(res)} rows) ({execution_time:.2f}s)\n")
                else:
                    print(f"Test completed in {execution_time:.2f} seconds.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run database tests with optional full table print")
    parser.add_argument("-f", "--full-table", action="store_true", help="Print the full table results")
    
    args = parser.parse_args()
    
    main(print_full_table=args.full_table)
