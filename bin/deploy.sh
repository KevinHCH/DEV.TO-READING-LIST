#!/usr/bin/env bash
CRON_NAME=devto_list
SCRIPT=$(pwd)/main.py
PDF_FILES=$(pwd)/pdf/*.pdf

## INSTALL DEPENDENCIES ########
pipenv install

# Install wkhtmltopdf in centos
# https://gist.github.com/paulsturgess/cfe1a59c7c03f1504c879d45787699f5
## CREATING ENV_VARS ########
printf "USERNAME_GIT=\nPASSWORD_GIT=\nMAIL_SENDER=\nMAIL_PASSWORD=\nMAIL_RECEIVER=\n" >> .env

## CONFIG CRONTAB ########
crontab -l >> $CRON_NAME
# Run this command all days at 10:00
echo "00 10 * * * pipenv run python3 $SCRIPT > /dev/null " >> $CRON_NAME
# Delete pdf files per day
echo "00 23 * * * rm -rf $PDF_FILES > /dev/null"
# Delete reading list per month
echo "00 23 30 * * rm -rf $(pwd)/*.json > /dev/null"

printf "## The deploy has been completed \n"
