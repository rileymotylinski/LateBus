# Setup
1. setup virtual environment
```
pip install -r requirements.txt
```
2. start cronjob to fetch the static schedule data from Metro Transit. this is
   everyday (@ 8am) per [Metro Transit's
   recommendation](https://svc.metrotransit.org/), but feel free to do
   whatever's comfortable.
```
// after running crontab -e...
0 8 * * * python3 /home/<MY_USERNAME>/Documents/LateBus/lib/fetch_static_schedule.py
```
3. start data collection
```
python3 main.py
```