kart-analyzer
=============

Python Tool to analyze kart and driver relative performance


Instructions

1) Create mysql DB (db=spk , user=[youruser], pass=[yourpass])
2) Create mysql DB structure (**run blahblah.sql < **)
3) Add drivers to be computed to table spk.drivers
4) Change user/password in all python scripts at top
5) Cron(Daily) to pull new data (get_new_heat_data.py) (do not run this often or you might get banned)
6) to analyze karts, run ./analyze_karts.py; **./analyze_league_karts.py**
7) compare karts by running ./list_karts_.py

** needs adjustments to code
