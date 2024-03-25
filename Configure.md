![New Relic logo](https://newrelic.com/static-assets/images/logo/nr-logo-50vh.png)

## Win in 3 easy steps

1. Download the [latest release](https://github.com/zmrfzn/data-driven-dave/releases) and complete the prerequisites below including the New Relic instrumentation.
2. Play the game, and stop by the **New Relic** booth to show off your game stats dashboard. (you will be rewarded for this effort)
3. If you have the high score, you win the grand prize!

## Prerequisites

- You'll need a New Relic account. The good news is that you can create a [free account here](https://newrelic.com/signup?utm_source=event&utm_medium=community&utm_campaign=apj-fy-24-q1-devrel-kcdmumbai) (no credit card required).
- To run the game on your machine you will need the following:
  - ENV VAR named `NEW_RELIC_CONFIG_FILE` with the value of absolute path to the file `newrelic.ini` on your system (e.g. `export NEW_RELIC_CONFIG_FILE=/Users/username/Downloads/dangerous-dave/newrelic.ini`)
  
- New Relic instrumentation
  - Update the newrelic.ini file by replacing INSERT_YOUR_INGEST_LICENSE_KEY_HERE with your account's [ingest license key](https://docs.newrelic.com/docs/apis/intro-apis/new-relic-api-keys/).
  - To see your game stats on a New Relic dashboard edit the game_stats.json file by doing a global search and replace to substitute "YOUR_ACCOUNT_ID" with your 7-digit [account ID](https://docs.newrelic.com/docs/accounts/accounts-billing/account-structure/account-id/).
  - Then, copy the modified JSON and [import the dashboard](https://docs.newrelic.com/docs/query-your-data/explore-query-data/dashboards/introduction-dashboards/#dashboards-import) into your New Relic account.

> Note: the release bundle contains all the files you need to run the game. You do not need to download or clone the source code.

## Running the program

Simply Double click (Windows) or run the executable file from your favorite terminal `data-dave-linux.exe` `data-dave-mac` on your machine.

## Troubleshooting

- If the game is crashing or you are unable to run the game, make sure you have complete the prerequisites above especially the ENV VAR and adding New Relic License Key to the `newrelic.ini` file.
- After adding the ENV VAR (`export NEW_RELIC_CONFIG_FILE=/Users/username/Downloads/dangerous-dave/newrelic.ini`), launch the game using the binary from the same terminal instance. Alternatively you can add the ENV VAR to your `.bashrc`, `.zshrc` or `.bash_profile` file and restart your terminal session.

## ![New Relic logo icon](https://newrelic.com/static-assets/images/icons/avatar-newrelic.png) New Relic DevOpsDays Challenge
