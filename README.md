![New Relic logo](https://newrelic.com/static-assets/images/logo/nr-logo-50vh.png)
# Introduction
If you don't already know why you need a monitoring and observability solution, it can be challenging to find an example that is illustrative, compelling, and engaging. There are literally thousands of "monitor this fake take-out food website" examples and - while they certainly show a valid real-world example of something you might want to monitor - they are usually a real yawner.

What if - and hear us out - you could play around with a monitoring solution AND PLAY A VIDEO GAME at the same time?!? WE KNOW, RIGHT?!?

That's what this example is all about. Install a game, set it up in New Relic, and then play the game to see your stats. 

Dangerous Dave was a classic 1980's side-scroller style game that many spent hours playing when we should have been doing productive work. Now we've turned the tables, making Dave help with our actual work.

The point of this project is two-fold: 

 1. To give folks a fun way to kick the tires on New Relic monitoring; 
 2. and to show how easy it is to instrument a custom application, capture and collect non-standard metrics, and display them in a meaningful way.

We hope you enjoy!

## Prerequisites

- You'll need a New Relic account. The good news is that you can create a [free account here](https://newrelic.com/signup) (no credit card required).
- To compile the program, you must have Python 3 installed.
- You will need to install the following packages using `pip` before starting the program. You may wish to install these packages in a [virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).
  - pygame (e.g. `pip install pygame`)
  - newrelic (e.g. `pip install newrelic`)
- New Relic instrumentation
  - Update the newrelic.ini file by replacing INSERT_YOUR_INGEST_LICENSE_KEY_HERE with your account's [ingest license key](https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/).
  - To see your game stats on a New Relic dashboard edit the game_stats.json file by doing a global search and replace to substitute "YOUR_ACCOUNT_ID" with your 7-digit [account ID](https://docs.newrelic.com/docs/accounts/accounts-billing/account-structure/account-id/). 
  - Then, copy the modified JSON and [import the dashboard](https://docs.newrelic.com/docs/query-your-data/explore-query-data/dashboards/introduction-dashboards/#dashboards-import) into your New Relic account.

## Running the program

- You can run either of the main python scripts located at the root of the repository: `python main_oo.py` or `python main_fun.py`. This should start the game immediately.
- Only main_fun.py has been instrumented to send data to New Relic.

## Misc

- The project is almost a identical replica - the only thing that wasn't implemented was the enemies, due to the project's deadline.
- Yes, we plan on making updates in the future.

## ![New Relic logo icon](https://newrelic.com/static-assets/images/icons/avatar-newrelic.png) New Relic DevOpsDays Challenge

Win in 3 simple steps:
1. Clone this repository, and complete the New Relic instrumentation prerequisites.
2. Play the game, and stop by the **New Relic** booth to show off your game stats dashboard. (you will be rewarded for this effort)
3. If you have the high score, you win the grand prize!

# Dangerous Dave Replica
*(this is the original description you can find over on https://github.com/mwolfart/dangerous-dave) We remain deeply endebted to them for their effort to bring this classic game to life on the python platform! - Rachel and Leon)*

 - This project is a replica of the 1988 DOS game Dangerous Dave, made by John Romero. The project was built in Python along with a team of three students (Arthur Medeiros, Guilherme Cattani and me), as a course assignment.
 - The goal of the project was to study and practice the three types of programming paradigms: imperative, object-oriented and functional. To achieve this, we picked Python as a language since it can perform all three types of tasks in a fairly good way.
