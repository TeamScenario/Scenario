@echo off
TITLE scenario
:: Enables virtual env mode and then starts scenario
env\scripts\activate.bat && py -m scenario
