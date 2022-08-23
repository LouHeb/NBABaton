
import pandas as pd
from datetime import datetime, timedelta
import requests

from PIL import Image, ImageChops, ImageDraw, ImageFont
import os

from basketball_reference_scraper.seasons import get_schedule

def LaSaison(M,Y):
    if M>=9:return(Y+1)
    else:return(Y)

Yest = datetime.now() - timedelta(216)

# --- Get the season's last year
Year = LaSaison(int(datetime.strftime(Yest,"%m")),int(datetime.strftime(Yest,"%Y")))

print(Year)

d_RS = get_schedule(Year)


print(d_RS)
