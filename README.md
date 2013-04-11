kart-analyzer
=============

Python Tool to analyze kart and driver relative performance


Instructions

1) Create mysql DB (db=spk , user=[youruser], pass=[yourpass])
2) Create mysql DB structure (mysql -h mydatabasehost -u user -p passwd spk < mysql_db.sql)
3) Add/Subtract drivers to be computed to/from the table spk.drivers
4) Change user/password in all python scripts at top
5) Setup a Cron job to pull new data (get_new_heat_data.py) (do not run this often or you might get banned)
6) to analyze karts, run ./analyze_karts.py (not currently taking into account league karts)
7) compare karts by running ./list_karts_.py (needs tweaks)

