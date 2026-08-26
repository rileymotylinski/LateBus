# Setup
1. setup virtual environment
```bash
python3 -m venv venv
source venv/bin/activate # or whatever on your respective os
pip install -r requirements.txt
```
2. start cronjob to fetch the static schedule data from Metro Transit. This is
   everyday (@ 8am) per [Metro Transit's
   recommendation](https://svc.metrotransit.org/), but feel free to do
   whatever's comfortable.
```bash
# after running crontab -e...
0 8 * * * python3 /path/to/project/LateBus/lib/fetch_static_schedule.py
```
3. start data collection
```bash
python3 main.py
```