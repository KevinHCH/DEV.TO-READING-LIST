#!/usr/bin/env bash
CRON_NAME=devto_list
SCRIPT=$(pwd)/main.py
PDF_FILES=$(pwd)/pdf/*.pdf

## INSTALL DEPENDENCIES ########
pipenv install

## CONFIG CRONTAB ########
crontab -l >> $CRON_NAME
# Run this command all days at 10:00
echo "00 10 * * * pipenv run python3 $SCRIPT > /dev/null " >> $CRON_NAME
# Delete pdf files per day
echo "00 23 * * * rm -rf $PDF_FILES > /dev/null"
# Delete reading list per month
echo "00 23 30 * * rm -rf $(pwd)/*.json > /dev/null"

printf "## The deploy has been completed \n"
