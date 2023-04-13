# Dangerous Dave Replica

This project is a replica of the 1988 DOS game Dangerous Dave, made by John Romero. The project was built in Python along with a team of three students (Arthur Medeiros, Guilherme Cattani and me), as a course assignment.

The goal of the project was to study and practice the three types of programming paradigms: imperative, object-oriented and functional. To achieve this, we picked Python as a language since it can perform all three types of tasks in a fairly good way.

## Prerequisites

- To compile the program, you must have Python 3 installed.
- Additionally, you may need to install the following packages using `pip` before starting the program:
  - pygame (e.g. `pip install pygame`)
  - newrelic (e.g. `pip install newrelic`)
- New Relic instrumentation
  - To send your game data to New Relic you must have an account. You can create a [free account](https://newrelic.com/signup) (no credit card required).
  - Update the newrelic.ini file by replacing INSERT_YOUR_INGEST_LICENSE_KEY_HERE with your account's [ingest license key](https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/).
  - To see your game stats on a New Relic dashboard edit the game_stats.json file by replacing YOUR_ACCOUNT_ID with your 7-digit [account ID](https://docs.newrelic.com/docs/accounts/accounts-billing/account-structure/account-id/).

## Running the program

- You can run either of the main python scripts located at the root of the repository: `python main_oo.py` or `python main_fun.py`. This should start the game immediately.
- Only main_fun.py has been instrumented to send data to New Relic.

## Misc

- The project is almost a identical replica - the only thing that wasn't implemented was the enemies, due to the project's deadline.
