#---
#       IMPORT LIBRARIES
#---

import pandas as pd
from datetime import datetime, timedelta
import requests
#from basketball_reference_scraper.seasons import get_schedule
from requests import get
from bs4 import BeautifulSoup

from PIL import Image, ImageChops, ImageDraw, ImageFont
import os


#---
#       DICTIONNARIES
#---

LOGOS = {'BOS':'https://upload.wikimedia.org/wikipedia/en/8/8f/Boston_Celtics.svg','BRK':'https://upload.wikimedia.org/wikipedia/commons/4/44/Brooklyn_Nets_newlogo.svg','NYK':'https://upload.wikimedia.org/wikipedia/en/2/25/New_York_Knicks_logo.svg',
'PHI':'https://upload.wikimedia.org/wikipedia/en/0/0e/Philadelphia_76ers_logo.svg','TOR':'https://upload.wikimedia.org/wikipedia/en/3/36/Toronto_Raptors_logo.svg','CHI':'https://upload.wikimedia.org/wikipedia/en/6/67/Chicago_Bulls_logo.svg',
'CLE':'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Cleveland_Cavaliers_logo.svg/800px-Cleveland_Cavaliers_logo.svg.png','DET':'https://upload.wikimedia.org/wikipedia/commons/c/c9/Logo_of_the_Detroit_Pistons.svg','IND':'https://upload.wikimedia.org/wikipedia/en/1/1b/Indiana_Pacers.svg',
'MIL':'https://upload.wikimedia.org/wikipedia/en/4/4a/Milwaukee_Bucks_logo.svg','ATL':'https://upload.wikimedia.org/wikipedia/en/2/24/Atlanta_Hawks_logo.svg','CHO':'https://upload.wikimedia.org/wikipedia/en/c/c4/Charlotte_Hornets_%282014%29.svg',
'MIA':'https://upload.wikimedia.org/wikipedia/en/f/fb/Miami_Heat_logo.svg','ORL':'https://upload.wikimedia.org/wikipedia/en/1/10/Orlando_Magic_logo.svg','WAS':'https://upload.wikimedia.org/wikipedia/en/0/02/Washington_Wizards_logo.svg',
'DEN':'https://upload.wikimedia.org/wikipedia/en/7/76/Denver_Nuggets.svg','MIN':'https://upload.wikimedia.org/wikipedia/en/c/c2/Minnesota_Timberwolves_logo.svg','OKC':'https://upload.wikimedia.org/wikipedia/en/5/5d/Oklahoma_City_Thunder.svg',
'POR':'https://upload.wikimedia.org/wikipedia/en/2/21/Portland_Trail_Blazers_logo.svg','UTA':'https://upload.wikimedia.org/wikipedia/en/5/52/Utah_Jazz_logo_2022.svg',
'GSW':'https://upload.wikimedia.org/wikipedia/en/0/01/Golden_State_Warriors_logo.svg','LAC':'https://upload.wikimedia.org/wikipedia/en/thumb/e/ed/Los_Angeles_Clippers_%282024%29.svg/800px-Los_Angeles_Clippers_%282024%29.svg.png',
'LAL':'https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg','PHO':'https://upload.wikimedia.org/wikipedia/en/d/dc/Phoenix_Suns_logo.svg','SAC':'https://upload.wikimedia.org/wikipedia/en/c/c7/SacramentoKings.svg',
'DAL':'https://upload.wikimedia.org/wikipedia/en/9/97/Dallas_Mavericks_logo.svg','HOU':'https://upload.wikimedia.org/wikipedia/en/2/28/Houston_Rockets.svg','MEM':'https://upload.wikimedia.org/wikipedia/en/f/f1/Memphis_Grizzlies.svg',
'NOP':'https://upload.wikimedia.org/wikipedia/en/0/0d/New_Orleans_Pelicans_logo.svg','SAS':'https://upload.wikimedia.org/wikipedia/en/a/a2/San_Antonio_Spurs.svg'}

TeamName = {
'PHW':'Philadelphia Warriors','CHS':'Chicago Stags','STB':'St Louis Bombers','PRO':'Provodence Steamrollers','TRH':'Toronto Huskies',
'CLR':'Cleveland Rebels','DTF':'Detroit Falcons','PIT':'Pittsburgh Ironmen','WSC':'Washington Capitols','BLB':'Baltimore Bullets','NOK':'New Orleans/Oklahoma City Hornets',
'MNL':'Minneapolis Lakers','INJ':'Indianapolis Jets','FTW':'Fort Wayne Pistons','ROC':'Rochester Royals','DNN':'Denver Nuggets','CHA':'Charlotte Bobcats',
'SHE':'Sheboygan Red Skins','TRI':'Tri-Cities Blackhawks','SYR':'Syracuse Nationals','INO':'Indianapolis Olympians','WAT':'Waterloo Hawks',
'AND':'Anderson Packers','MLH':'Milwaukee Hawks','STL':'St. Louis Hawks','CIN':'Cincinnati Royals','CHP':'Chicago Packers','CHZ':'Chicago Zephyrs',
'SFW':'San Francisco Warriors','BAL':'Baltimore Bullets','SEA':'Seattle SuperSonics','SDR':'San Diego Rockets','BUF':'Buffalo Braves',
'KCO':'Kansas City-Omaha Kings','CAP':'Capital Bullets','NOJ':'New Orleans Jazz','WSB':'Washington Bullets','KCK':'Kansas City Kings',
'NYN':'New York Nets','NJN':'New Jersey Nets','SDC':'San Diego Clippers','CHH':'Charlotte Hornets','VAN':'Vancouver Grizzlies','NOH':'New Orleans Hornets',
'NYK':'New York Knicks',
'ATL':'Atlanta Hawks',
'BOS':'Boston Celtics',
'BRK':'Brooklyn Nets',
'CHO':'Charlotte Hornets',
'CHI':'Chicago Bulls',
'CLE':'Cleveland Cavaliers',
'DAL':'Dallas Mavericks',
'DEN':'Denver Nuggets',
'DET':'Detroit Pistons',
'GSW':'Golden State Warriors',
'HOU':'Houston Rockets',
'IND':'Indiana Pacers',
'LAC':'Los Angeles Clippers',
'LAL':'Los Angeles Lakers',
'MEM':'Memphis Grizzlies',
'MIA':'Miami Heat',
'MIL':'Milwaukee Bucks',
'MIN':'Minnesota Timberwolves',
'NOP':'New Orleans Pelicans',
'OKC':'Oklahoma City Thunder',
'ORL':'Orlando Magic',
'PHI':'Philadelphia 76ers',
'PHO':'Phoenix Suns',
'POR':'Portland Trail Blazers',
'SAC':'Sacramento Kings',
'SAS':'San Antonio Spurs',
'TOR':'Toronto Raptors',
'UTA':'Utah Jazz',
'WAS':'Washington Wizards'
}

ActualTeams = ['ATL','BOS','BRK','CHI','CHO','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']

TeamAbbr = {TeamName[x]:x for x in TeamName}

Creation = {'ATL':1949,'BOS':1946,'BRK':1976,'LAC':1970,'CHO':1988,'CHI':1966,'WAS':1961,'CLE':1970,'DAL':1980,'DEN':1976,'DET':1948,'GSW':1946,'HOU':1967,'IND':1976,'LAL':1948,'MEM':1995,'MIA':1988,'MIL':1968,'MIN':1989,'NOP':2002,'NYK':1946,'OKC':1967,'ORL':1989,'PHI':1949,'PHO':1968,'POR':1970,'SAC':1948,'SAS':1976,'TOR':1995,'UTA':1974}

Lit_Day = {"01":"1st","02":"2nd","03":"3rd","04":"4th","05":"5th","06":"6th","07":"7th","08":"8th","09":"9th","10":"10th","11":"11th","12":"12th","13":"13th","14":"14th","15":"15th","16":"16th","17":"17th","18":"18th","19":"19th","20":"20th","21":"21st","22":"22nd","23":"23rd","24":"24th","25":"25th","26":"26th","27":"27th","28":"28th","29":"29th","30":"30th","31":"31st"}
Lit_Month = {'01':"January",'02':"February",'03':"March",'04':"April",'05':"May",'06':"June",'07':"July",'08':"August",'09':"September",'10':"October",'11':"November",'12':"December",}

#---
#       FUNCTIONS
#---
def LaSaison(M,Y):
    if M>=9:return(Y+1)
    else:return(Y)

def GameExtractor(LeGet,Num,IsNext='No'):
    if IsNext=='Next':
        return([TeamAbbr[LeGet['VISITOR'][Num]],datetime.strftime(LeGet['DATE'][Num].to_pydatetime(),"%Y%m%d"),TeamAbbr[LeGet['HOME'][Num]]])
    elif IsNext=='No':
        return([TeamAbbr[LeGet['VISITOR'][Num]],datetime.strftime(LeGet['DATE'][Num].to_pydatetime(),"%Y%m%d"),TeamAbbr[LeGet['HOME'][Num]],str(int(LeGet['VISITOR_PTS'][Num])),str(int(LeGet['HOME_PTS'][Num]))])


def ReadLeFile(name):
    with open(name,"r", encoding="utf-8") as f:
        lines = [line.strip().split(" ") for line in f]
    return(lines)

def WriteLeFile(Liste,Name):
    file = open(Name,"w") 
    for line in Liste:
        for word in line:
            file.write(word+' ')
        file.write('\n')
    file.close()

def ReplaceUnderBySpace(x):
    res = ''
    for l in x:
        if l=='_':res+=' '
        else:res+=l
    return(res)

def ReplaceSpaceByUnder(x):
    res = ''
    for l in x:
        if l==' ':res+='_'
        else:res+=l
    return(res)

def Arr(x):
    return(int(x*100)/100)

def get_schedule(season, playoffs=False):
    months = ['October', 'November', 'December', 'January', 'February', 'March',
            'April', 'May', 'June']
    if season==2020:
        months = ['October-2019', 'November', 'December', 'January', 'February', 'March',
                'July', 'August', 'September', 'October-2020']
    df = pd.DataFrame()
    for month in months:
        r = get(f'https://www.basketball-reference.com/leagues/NBA_{season}_games-{month.lower()}.html')
        if r.status_code==200:
            soup = BeautifulSoup(r.content, 'html.parser')
            table = soup.find('table', attrs={'id': 'schedule'})
            if table:
                month_df = pd.read_html(str(table))[0]
                df = pd.concat([df, month_df])

    df = df.reset_index()

    cols_to_remove = [i for i in df.columns if 'Unnamed' in i]
    cols_to_remove += [i for i in df.columns if 'Notes' in i]
    cols_to_remove += [i for i in df.columns if 'Start' in i]
    cols_to_remove += [i for i in df.columns if 'Attend' in i]
    cols_to_remove += [i for i in df.columns if 'Arena' in i]
    cols_to_remove += [i for i in df.columns if 'LOG' in i]
    cols_to_remove += ['index']
    df = df.drop(cols_to_remove, axis=1)
    df.columns = ['DATE', 'VISITOR', 'VISITOR_PTS', 'HOME', 'HOME_PTS']

    if season==2020:
        df = df[df['DATE']!='Playoffs']
        df['DATE'] = df['DATE'].apply(lambda x: pd.to_datetime(x))
        df = df.sort_values(by='DATE')
        df = df.reset_index().drop('index', axis=1)
        playoff_loc = df[df['DATE']==pd.to_datetime('2020-08-17')].head(n=1)
        if len(playoff_loc.index)>0:
            playoff_index = playoff_loc.index[0]
        else:
            playoff_index = len(df)
        if playoffs:
            df = df[playoff_index:]
        else:
            df = df[:playoff_index]
    else:
        # account for 1953 season where there's more than one "playoffs" header
        if season == 1953:
            df.drop_duplicates(subset=['DATE', 'HOME', 'VISITOR'], inplace=True)
        playoff_loc = df[df['DATE']=='Playoffs']
        if len(playoff_loc.index)>0:
            playoff_index = playoff_loc.index[0]
        else:
            playoff_index = len(df)
        if playoffs:
            df = df[playoff_index+1:]
        else:
            df = df[:playoff_index]
        df['DATE'] = df['DATE'].apply(lambda x: pd.to_datetime(x))
    return df

def GameDay(date,teamExt,teamDom,streak,lastHold,Side,Round = 'Bleu'):#'Finals'):
    
    # Background
    bg = Image.open("bg_"+teamDom+".jpg").convert("RGBA")
    bgBleu = Image.open("bg_"+Round+".jpg").convert("RGBA")
    Background = ImageChops.multiply(bg, bgBleu)
           
    # Boxes Contender and Defender
    Contender = Image.open("Contender.png").convert("RGBA")
    W_cont, H_cont = Contender.size
    Defender = Image.open("Defender.png").convert("RGBA")
    W_def, H_def = Defender.size
    pAway = 466
    pHome = 1184
    if Side=='Away':
        Background.paste(Defender, (pAway-int(W_def/2), 186),Defender)
        Background.paste(Contender, (pHome-int(W_cont/2), 730),Contender)
    elif Side=='Home':
        Background.paste(Defender, (pHome-int(W_def/2), 186),Defender)
        Background.paste(Contender, (pAway-int(W_cont/2), 730),Contender)
        
    #title    
    Top = Image.open("Top.png").convert("RGBA")
    Background.paste(Top, (0, 0),Top)
        
    #Logos Teams
    pLogo = 552
    LogoDom = Image.open(teamDom+".png").convert("RGBA")
    WDom, HDom = LogoDom.size    
    LogoExt = Image.open(teamExt+".png").convert("RGBA")
    WExt, HExt = LogoExt.size

    Background.paste(LogoDom, (pHome-int(WDom/2), pLogo-int(HDom/2)),LogoDom)
    Background.paste(LogoExt, (pAway-int(WExt/2), pLogo-int(HExt/2)),LogoExt)
    
#    x = 0.5
#    LogoDom = LogoDom.resize((int(W*x),int(H*x)))
    
    #Nom du tour playoffs/playin/finales
    if Round!='Bleu':
        LogoRound = Image.open(Round+".png").convert("RGBA")
        Background.paste(LogoRound, (0, 0),LogoRound)
    
    #plus foncé pour le background 
    Surground = Image.open("fg_"+Round+".png").convert("RGBA")
    Final = ImageChops.multiply(Background, Surground)
    

    # write date
    d = ImageDraw.Draw(Final)
    W, H = Final.size    
    fnt = ImageFont.truetype(font='Futura-CondensedLight.otf', size=61)
    msg = "- "+date+" -"
    w, h = fnt.getbbox(msg)[2:]
    
    if Round=='Playoffs':d.text(((W-w)/2,195-h/2), msg, font=fnt, fill=(255, 203, 203))
    elif Round=='Finals':d.text(((W-w)/2,195-h/2), msg, font=fnt, fill=(252, 230, 200))
    elif Round=='PlayIn':d.text(((W-w)/2,195-h/2), msg, font=fnt, fill=(137, 186, 215))
    else:
        d.text(((W-w)/2,195-h/2), msg, font=fnt, fill=(137, 255, 255))

    # write streak
    fnt = ImageFont.truetype(font='Futura-CondensedLight.otf', size=42)
    if streak==1: msg = "1 game"
    else:
        msg = str(streak)+ " games"
    w, h = fnt.getbbox(msg)[2:]

    if Side=='Away': W = (264+668)/2
    elif Side=='Home': W = (982+1386)/2
    d.text((W-w/2,818-h/2), msg, font=fnt, fill=(0, 0, 0))
    d.text((W-w/2+1,818-h/2+1), msg, font=fnt, fill=(0, 0, 0))

    # write last hold
    fnt = ImageFont.truetype(font='Futura-CondensedLight.otf', size=42)
    msg = lastHold
    w, h = fnt.getbbox(msg)[2:]
    if Side=='Away': W = (1011+1357)/2
    elif Side=='Home': W = (293+639)/2
    d.text((W-w/2,818-h/2), msg, font=fnt, fill=(0, 0, 0))
    d.text((W-w/2+1,818-h/2+1), msg, font=fnt, fill=(0, 0, 0))
    
    
    Final.save('0_GameDay.png',"PNG")


def NewHolders(NewHolder,lastHold,Round = 'Bleu'):#'Finals'):
    BackgroundNew = Image.open("bg_"+NewHolder+".jpg").convert("RGBA")
#    bgBleuNew = Image.open("bg_Bleu.jpg").convert("RGBA")
#    BackgroundNew = ImageChops.multiply(bgNew, bgBleuNew)

    CadreNew = Image.open("NewHolder.png").convert("RGBA")
    BackgroundNew.paste(CadreNew, (0, 0),CadreNew)

    pLogo = 552
    LogoNew = Image.open(NewHolder+".png").convert("RGBA")
    W, H = LogoNew.size    
    BackgroundNew.paste(LogoNew, (825-int(W/2), pLogo-int(H/2)),LogoNew)
    
    if Round=='PlayIn':
        LogoRound = Image.open(Round+".png").convert("RGBA")
        BackgroundNew.paste(LogoRound, (0, 0),LogoRound)
    
    SurgroundNew = Image.open("fg_"+Round+".png").convert("RGBA")
    FinalNew = ImageChops.multiply(BackgroundNew, SurgroundNew)
    
    LogoBaton = Image.open("LogoBaton.png").convert("RGBA")
    FinalNew.paste(LogoBaton, (0, 0),LogoBaton)
    
    dNew = ImageDraw.Draw(FinalNew)
    W, H = FinalNew.size
    fnt = ImageFont.truetype(font='Futura-CondensedLight.otf', size=42)
    msg = lastHold
    w, h = fnt.getbbox(msg)[2:]
    dNew.text(((W-w)/2,807-h/2), msg, font=fnt, fill=(0,0,0))
    dNew.text(((W-w)/2+1,807-h/2+1), msg, font=fnt, fill=(0,0,0))
    FinalNew.save('0_TheNewHolder.png',"PNG")



def SameHolders(SameHolder,Newstreak,Round = 'Bleu'):#'Finals'):
    BackgroundSame = Image.open("bg_"+SameHolder+".jpg").convert("RGBA")
#    bgBleuSame = Image.open("bg_Bleu.jpg").convert("RGBA")
#    BackgroundSame = ImageChops.multiply(bgSame, bgBleuSame)

    CadreSame = Image.open("SameHolder.png").convert("RGBA")
    BackgroundSame.paste(CadreSame, (0, 0),CadreSame)
    
    if Round=='PlayIn':
        LogoRound = Image.open(Round+".png").convert("RGBA")
        BackgroundSame.paste(LogoRound, (0, 0),LogoRound)

    pLogo = 552
    LogoSame = Image.open(SameHolder+".png").convert("RGBA")
    W, H = LogoSame.size    
    BackgroundSame.paste(LogoSame, (825-int(W/2), pLogo-int(H/2)),LogoSame)
    
    SurgroundSame = Image.open("fg_"+Round+".png").convert("RGBA")
    FinalSame = ImageChops.multiply(BackgroundSame, SurgroundSame)
    
    LogoBaton = Image.open("LogoBaton.png").convert("RGBA")
    FinalSame.paste(LogoBaton, (0, 0),LogoBaton)
    
    dSame = ImageDraw.Draw(FinalSame)
    W, H = FinalSame.size
    fnt = ImageFont.truetype(font='Futura-CondensedLight.otf', size=42)
    msg = str(Newstreak)+' games'
    w, h = fnt.getbbox(msg)[2:]
    dSame.text(((W-w)/2,807-h/2), msg, font=fnt, fill=(0,0,0))
    dSame.text(((W-w)/2+1,807-h/2+1), msg, font=fnt, fill=(0,0,0))
    FinalSame.save('0_TheSameHolder.png',"PNG")

def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days[1:]

#---
#       CODE
#---

# --- Get Last time run
with open("date.txt","r", encoding="utf-8") as f:
    lines = [line.strip().split("XXX") for line in f]
Last = datetime.strptime(lines[0][0], '%d/%m/%Y')
    
# --- Get yesterday date
Hier = datetime.now() - timedelta(1)

# Create a new file for the player stats each first af Jan.
if Hier.month==1 and Hier.day==1:
    Checkfile = open("PlayerStatsEachGame_byYear/PlayerStatsEachGame_"+str(Hier.year+1)+".txt",'w+')
    Checkfile.close

# --- Evaluate the days between last run    
LesDates = date_range(Last, Hier)

# --- Get the season's last year
Year = LaSaison(int(datetime.strftime(Hier,"%m")),int(datetime.strftime(Hier,"%Y")))

# --- Request the games of the current season
d_RS = get_schedule(Year)
d_PO = get_schedule(Year,True)
d = pd.concat([d_RS,d_PO],ignore_index=True)

#  ==>   ------ Get yesterday's games and update the overall games list -------------
for Yesti in LesDates:   


    # --- Put the date correctly formated
    Yest_Nb = datetime.strftime(Yesti,"%Y%m%d")
    Yest = datetime.strftime(Yesti,"%d/%m/%Y")

    # --- Write the date in a file
    FileDate = open("date.txt","w") 
    FileDate.write(Yest)
    FileDate.close()

    # --- Récuperer les indices des matchs de la nuit derniere
    GameIndexes = []
    Dates = list(d['DATE'])
    for i in range(0,len(Dates)):
        LaDate = datetime.strftime(Dates[i].to_pydatetime(),"%d/%m/%Y")
        if LaDate==Yest:GameIndexes.append(i)

    # --- Récuperer les matchs de la nuit derniere
    YestGames = [GameExtractor(d,index) for index in GameIndexes]

    #  ==>   ------ Get the current holder and the Big_Stats list for update the index.m later -------------
    BatonAtStake = False
    # --- Get the NBA holders list
    BatonHolders = ReadLeFile('BatonHistoryTable.txt')  
    # --- Get the current holder and the streak
    CurrentHolder = TeamAbbr[ReplaceUnderBySpace(BatonHolders[-1][1])]
    Streak = int(BatonHolders[-1][2])
    # --- Get the Big Statslder
    Big_Stats = ReadLeFile('BigStats.txt')    

    if len(GameIndexes)>0: # if there were games yesterday
        # --- Get the Games Overall List
        All_Games_List = ReadLeFile('Games_Database.txt')

        # --- Add yesterday games
        for g in YestGames:
            All_Games_List.append(g)

        # --- Write the updated file
        WriteLeFile(All_Games_List,'Games_Database.txt')    

    #  ==>   ----------- Check if the Baton is at stake -------------
        for g in YestGames:
            if CurrentHolder in [g[0],g[2]]:
                if CurrentHolder == g[0]:
                    BatonAtStake = True
                    Challenger = g[2]
                    HolderScore = int(g[3])
                    ChallengerScore = int(g[4])
                elif CurrentHolder == g[2]:
                    BatonAtStake = True
                    Challenger = g[0]
                    HolderScore = int(g[4])
                    ChallengerScore = int(g[3])

                if HolderScore>ChallengerScore:
                    GameBaton = g[:3]+[Challenger]
                    Situation = 'Same'
                    FormerHolder = Challenger
                elif HolderScore<ChallengerScore:
                    GameBaton = g[:3]+['New']
                    Situation = 'New'
                    FormerHolder = CurrentHolder
                    CurrentHolder = Challenger          

        if BatonAtStake:

    #  ==>   ------ Update List of games with baton at stake -------------

            # --- Get the Games Baton List
            Baton_Games_List = ReadLeFile('Games_Baton.txt')

            # --- Add the game
            Baton_Games_List.append(GameBaton)

            # --- Write the updated file
            WriteLeFile(Baton_Games_List,'Games_Baton.txt')


    #  ==>   ------ Update Baton holder and the list of holders + Bigstats -------------

            # --- Get the Baton holders List
            Baton_Holder_List = ReadLeFile('BatonHistoryTable.txt')    

            # --- Update the list
            if Situation == 'Same':
                Streak = int(Baton_Holder_List[-1][-1])+1
                Baton_Holder_List[-1][-1]=str(Streak)
            elif Situation == 'New':
                Streak = 1
                Baton_Holder_List.append([Yest, ReplaceSpaceByUnder(TeamName[CurrentHolder]), '1'])

            # --- Write the updated file
            WriteLeFile(Baton_Holder_List,'BatonHistoryTable.txt')

            # --- Get the line corresponding to the holder
            index = 0
            while Big_Stats[index][0]!=CurrentHolder:index+=1

            # --- Update the Longest
            if Streak>int(Big_Stats[index][1]):Big_Stats[index][1]=str(Streak)

            # --- Update the Cummulate
            Big_Stats[index][2]=str(int(Big_Stats[index][2])+1)

            # --- Update the NbTake
            if Situation=='New':Big_Stats[index][7]=str(int(Big_Stats[index][7])+1)

            # --- Update the Avg.Stk
            Big_Stats[index][3] = str(Arr(int(Big_Stats[index][2])/int(Big_Stats[index][7])))

            # --- Update the 10
            if Streak==10:Big_Stats[index][4]=str(int(Big_Stats[index][4])+1)

            # --- Update the NbSeas every
            for t in Big_Stats:
                if t[0] in Creation:t[8]=str(Year-Creation[t[0]])

            # --- Update the TakePerSeason
            Big_Stats[index][5] = str(Arr(int(Big_Stats[index][7])/int(Big_Stats[index][8])))

            # --- Update the LastHold
            if Situation=='New':
                Big_Stats[index][6] = 'Current_holder'
                index2 = 0
                while Big_Stats[index2][0]!=FormerHolder:index2+=1
                Big_Stats[index2][6] = Yest[-4:]+Yest[3:5]+Yest[0:2]

            # --- Update the Date at the beginning of the file
            Big_Stats[0][1]=Yest

            # --- Write the updated file
            WriteLeFile(Big_Stats,'BigStats.txt')

     #  ==>   ------ Update Players Stats in a NBA Baton game -------------

            # --- GetDataFromWebsites
            url="https://www.basketball-reference.com/boxscores/"+GameBaton[1]+"0"+GameBaton[2]+".html"
            SourceCode = requests.get(url).text

            Players = []

            # --- ExtractData
            for team in [GameBaton[0],GameBaton[2]]:
                phraseStart = '''<div id="all_box-'''+str(team)+'''-game-basic" class="table_wrapper">'''
                phraseEnd = '''Team Totals'''

                debut = 1
                fin = 1
                while SourceCode[debut:debut+len(phraseStart)]!=phraseStart:
                    debut+=1
                    fin+=1
                while SourceCode[fin:fin+len(phraseEnd)]!=phraseEnd:
                    fin+=1
                UsefulSourceCode=SourceCode[debut:fin]

                # --- Transform the string in a list
                phrasePlayer = '''"player" csk="'''
                phrasePoint = '''a-stat="pts" >'''
                phraseCodePlayer = '''ref="/players/'''
                letter = 1
                while letter<len(UsefulSourceCode):
                    if UsefulSourceCode[letter:letter+len(phrasePlayer)]==phrasePlayer:                    
                        player = []
                        Name =''
                        Surname =''
                        letter+=14
                        while UsefulSourceCode[letter]!=',':
                            if UsefulSourceCode[letter]!=' ':
                                Name+=UsefulSourceCode[letter]
                            else :
                                Name+='_'
                            letter+=1
                        letter+=1
                        while UsefulSourceCode[letter]!='"':
                            if UsefulSourceCode[letter]!=' ':
                                Surname+=UsefulSourceCode[letter]
                            else :
                                Surname+='_'
                            letter+=1
                        player.append(Name)
                        player.append(Surname)
                    elif UsefulSourceCode[letter:letter+len(phraseCodePlayer)]==phraseCodePlayer:
                        codePlayer =''
                        letter+=16
                        while UsefulSourceCode[letter]!='.':
                            codePlayer+=UsefulSourceCode[letter]
                            letter+=1
                        player.append(codePlayer)
                    elif UsefulSourceCode[letter:letter+len(phrasePoint)]==phrasePoint:

                        points =''
                        letter+=14
                        while UsefulSourceCode[letter]!='<':
                            points+=UsefulSourceCode[letter]
                            letter+=1
                        player.append(points)
                        player.append(GameBaton[1])
                        player.append(team)
                        if team == CurrentHolder:player.append('1')  # 1 means game holding the baton
                        elif team == FormerHolder:player.append('0')  # 0 = you have lost the bato
                        else:
                            player.append('2')                # 2 means missed-opportunity game
                        Players.append(player)
                    else:
                        letter+=1


            # --- Get the List of this year players stats
            This_Year_Pl_Stats_List = ReadLeFile('PlayerStatsEachGame_byYear/PlayerStatsEachGame_'+str(Yest[-4:])+'.txt')    

            # --- Update the List of this year players stats
            for p in Players: This_Year_Pl_Stats_List.append(p)

            # --- Write the updated file
            WriteLeFile(This_Year_Pl_Stats_List,'PlayerStatsEachGame_byYear/PlayerStatsEachGame_'+str(Yest[-4:])+'.txt')

            # --- Get the List of TOTAL players stats
            Total_Pl_Stats_List = ReadLeFile('PlayerStatsAvg.txt')    

            for LeJoueur in Players:
            # --- Check if the player already played for the baton
                if LeJoueur[2] not in [x[2] for x in Total_Pl_Stats_List[2:]]:
                    Total_Pl_Stats_List.append([LeJoueur[1], LeJoueur[0], LeJoueur[2], '0', '0', 'XXXXXXXX', '0', '0', '0'])

            # --- Get the line corresponding to the player
                index = 2
                while Total_Pl_Stats_List[index][2]!=LeJoueur[2]:index+=1

            # --- Update the Best_Scoring
                if int(LeJoueur[3])>int(Total_Pl_Stats_List[index][4]):
                    Total_Pl_Stats_List[index][4]=LeJoueur[3]
            # --- Update the BestSc_Date
                    Total_Pl_Stats_List[index][5]=Yest[-4:]+Yest[3:5]+Yest[0:2]

            # --- Update the Games_played
                Total_Pl_Stats_List[index][6]=str(int(Total_Pl_Stats_List[index][6])+1)

            # --- Update the Games_w_Baton
                if LeJoueur[6]=='1':Total_Pl_Stats_List[index][7]=str(int(Total_Pl_Stats_List[index][7])+1)

            # --- Update the Missed_Opportunity
                elif LeJoueur[6]=='2':Total_Pl_Stats_List[index][8]=str(int(Total_Pl_Stats_List[index][8])+1)

            # --- Update the Pts/game
                Total_Pl_Stats_List[index][3]= str((float(Total_Pl_Stats_List[index][3])*(int(Total_Pl_Stats_List[index][6])-1)+int(LeJoueur[3]))/int(Total_Pl_Stats_List[index][6]))

            # --- Update the Date at the beginning of the file
            Total_Pl_Stats_List[0][1]=Yest

            # --- Write the updated file
            WriteLeFile(Total_Pl_Stats_List,'PlayerStatsAvg.txt')


    #  ==>   ------ Check when is the next game -------------

    # --- find the next game with the current holder
    if len(GameIndexes)>0: # if there were games yesterday
        GameId = GameIndexes[-1]
        NextOrNot = '?'
    else:   # if there were no games yesterday, we find if there will be after
        i = 0
        while i<len(Dates) and datetime.strftime(Dates[i].to_pydatetime(),"%Y%m%d")<Yest_Nb:
            i+=1
        if i<len(Dates): # there will be after
            GameId = i-1
            NextOrNot = '?'
        else:  # there wont be after
            NextOrNot = 'Not'

    if NextOrNot != 'Not':     # if there will be after, we check if the holder will take part
        GameId += 1
        LeMatch = GameExtractor(d,GameId,'Next')
        while CurrentHolder not in [LeMatch[0],LeMatch[2]] and GameId<len(d['DATE'])-1:
            GameId+=1
            LeMatch = GameExtractor(d,GameId,'Next')

        # --- if the holder has another scheduled game
        if GameId < len(d['DATE'])-1:
            if CurrentHolder==LeMatch[0]:
                BatonSitu = 'Away'
                Cont = LeMatch[2]
            elif CurrentHolder==LeMatch[2]:
                BatonSitu = 'Home'
                Cont = LeMatch[0]
            Date = Lit_Month[LeMatch[1][4:6]]+', '+Lit_Day[LeMatch[1][6:]]

            # find last possession of the Contender
            LaTeam = 3
            while Big_Stats[LaTeam][0]!=Cont:LaTeam+=1
            LastPos = Big_Stats[LaTeam][6]
            LastPos = Lit_Month[LastPos[4:6]]+' '+Lit_Day[LastPos[6:]]+', '+LastPos[:4]

            os.chdir('Stock')
            GameDay(Date, LeMatch[0],LeMatch[2],Streak,LastPos,BatonSitu)#,'Playoffs')

            NewHolders(Cont,LastPos)
            SameHolders(CurrentHolder,Streak+1)

            os.chdir('..')
            # --- Write the Situation in a variable
            NextOrNot = 'Next'          
        else:  # if the holder wont have another game
            # --- Write the Situation in a variable
            NextOrNot = 'Not'    

    #  ==>  ------ Update the index.m file -------------

    # --- Read the actual file    
    with open("index.md","r", encoding="utf-8") as f:
        lines = [line.strip().split("XXX") for line in f]    

    # -- add an S if many games
    if Streak==1:Ss = ''
    else:
        Ss = 's'

    # --- adjust the first lines
    lines[2]=['<img src="'+LOGOS[CurrentHolder]+'" width="100" title="'+TeamName[CurrentHolder]+'"><p style="font-size:20px; font-family: FuturaHeavy;">For '+str(Streak)+' game'+Ss+'.</p>']
    if NextOrNot == 'Next':
        lines[5]=['<img src="https://raw.githubusercontent.com/LouHeb/NBABaton/gh-pages/Stock/0_GameDay.png" width="1000" title="Next NBA Baton Game">']
    else:
        lines[5]=['']

    # --- write the file
    file = open("index.md","w") 
    for l in lines[:8]:
        file.write(l[0]+'\n')    

    # --- write the Stats table
    for Team in ActualTeams:
        # find last possession of the team
        LaTeam = 3
        while Big_Stats[LaTeam][0]!=Team:LaTeam+=1
        LastPos = Big_Stats[LaTeam][6]
        if LastPos=='Current_holder':
            file.write('<tr><td style="text-align:center;font-size:13px;">  <img src="'+LOGOS[Team]+'" width="20" title="'+TeamName[Team]+'"></td><td style="text-align:center;font-size:13px;">  '+Big_Stats[LaTeam][1]+'</td><td style="text-align:center;font-size:13px;">  '+Big_Stats[LaTeam][2]+'</td><td style="text-align:center;color: red; font-family: FuturaHeavy;font-size:13px;">  Current defender</td></tr>\n')    
        else:
            LastPos = Lit_Month[LastPos[4:6]]+' '+Lit_Day[LastPos[6:]]+', '+LastPos[:4]
            file.write('<tr><td style="text-align:center;font-size:13px;">  <img src="'+LOGOS[Team]+'" width="20" title="'+TeamName[Team]+'"></td><td style="text-align:center;font-size:13px;">  '+Big_Stats[LaTeam][1]+'</td><td style="text-align:center;font-size:13px;">  '+Big_Stats[LaTeam][2]+'</td><td style="text-align:center;font-size:13px;">  '+LastPos+'</td></tr>\n')    

    for l in lines[38:41]:
        file.write(l[0]+'\n')   


    if BatonAtStake:
        # --- write the History table
        if Situation=='New':
            Ajd = Lit_Month[Yest[3:5]]+' '+Lit_Day[Yest[:2]]+', '+Yest[6:]
            file.write('<tr><td style="text-align:center">  '+Ajd+'</td><td style="text-align:center"><img src="'+LOGOS[CurrentHolder]+'" width="30" title="'+TeamName[CurrentHolder]+'"></td><td style="text-align:center"> 1 </td></tr>\n')
            for l in lines[41:]:
                file.write(l[0]+'\n')  
        else:
            file.write(lines[41][0][:-12]+str(Streak)+lines[41][0][-11:]+'\n')
            for l in lines[42:]:
                file.write(l[0]+'\n')              
    else:
        for l in lines[41:]:
            file.write(l[0]+'\n')  

    file.close()

    #  ==>  ------ Update the Baton distance -------------
    if NextOrNot == 'Next':  # --- if the holder has another scheduled game
        def FindNeighbors(game,LaList):
            LeReturn =[]
            counterA = game+1
            counterB = game+1
            TeamA = LaList[game][0]
            TeamB = LaList[game][2]
            while counterA<len(LaList) and LaList[counterA][0]!=TeamA and LaList[counterA][2]!=TeamA:
                counterA+=1
            while counterB<len(LaList) and LaList[counterB][0]!=TeamB and LaList[counterB][2]!=TeamB:
                counterB+=1

            if counterA!=len(LaList):
                if len(LaList[counterA][3])==0:
                    LaList[counterA][3]=LaList[game][3]+[game]
                    LeReturn.append(counterA)
                elif len(LaList[counterA][3])>len(LaList[game][3]+[game]):
                    LaList[counterA][3]=LaList[game][3]+[game]
                    LeReturn.append(counterA)
            if counterB!=len(LaList):
                if len(LaList[counterB][3])==0:
                    LaList[counterB][3]=LaList[game][3]+[game]
                    LeReturn.append(counterB)
                elif len(LaList[counterB][3])>len(LaList[game][3]+[game]):
                    LaList[counterB][3]=LaList[game][3]+[game]
                    LeReturn.append(counterB)
            return (LeReturn)

        def IsItGood(team, match,LaList):
            if LaList[match][0]!=team and LaList[match][2]!=team:
                return(False)
            else:
                return(True)

        def AfficherParcours(match,LaList):
            leretour = []
            for i in LaList[match][3]:
                leretour.extend([LaList[i][:3]])
            leretour.extend([LaList[match][:3]])
            return(leretour)

        def SortByNbOfGames(Nexts,LaList):
            PathsLength =[]
            for j in Nexts:
                PathsLength.append(len(LaList[j][3]))
            Z = [x for _,x in sorted(zip(PathsLength,Nexts))] #sort Nexts according to PathsLength items
            return (Z)

        Teams = ['ATL','BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',  'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
        Paths =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        PathsHistory =[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        Holder = CurrentHolder
        Today = int(datetime.strftime(Yesti+timedelta(1),"%Y%m%d"))

        # Condition to know if the shorter path is controled by the date or by the nb of game
        SortByDate = True

        #-------------------------Games List-----------------------------
        for Team in Teams :
            Games = []
            for g in range(0,len(d['DATE'])):
                Games.append(GameExtractor(d,g,'Next'))
            for g in Games:         #   Add an empty list at the end of each game item
                g.extend([[]])

        #-------------------------Main-----------------------------
            #Find the next game of the holder
            TodayGame = 0
            while int(Games[TodayGame][1])<Today:
                TodayGame+=1
            while Games[TodayGame][0]!=Holder and Games[TodayGame][2]!=Holder :
                TodayGame+=1

            game = TodayGame
            Condition = IsItGood(Team,game,Games)

            if Condition:
                Paths[Teams.index(Team)]=AfficherParcours(game,Games)
                PathsHistory[Teams.index(Team)].append(len(Paths[Teams.index(Team)]))
            else :
                Next = FindNeighbors(game,Games)
            #    --
                if SortByDate:
                    Next.sort()
                else:
                    Next=SortByNbOfGames(Next,Games)
            #    --
                item = 0
                while not Condition and item<len(Next):
                    game = Next[item]
                    Next.extend(FindNeighbors(game,Games))
            #       --
                    if SortByDate:
                        Next.sort()
                    else:
                        Next=SortByNbOfGames(Next,Games)
            #       --
                    Condition = IsItGood(Team,game,Games)
                    item+=1
                if Condition:
                    Paths[Teams.index(Team)]=AfficherParcours(game,Games)
                    PathsHistory[Teams.index(Team)].append(len(Paths[Teams.index(Team)]))
                else:
                    Paths[Teams.index(Team)]=["No way!"]
                    PathsHistory[Teams.index(Team)].append(100)

        # ------ Write result in a file ------   
        file = open("DistanceToBaton.txt","w") 
        for tim in range(0,len(Teams)):
            file.write(Teams[tim]+' ')      # team name
            if Paths[tim]==["No way!"]:
                file.write('X ')            # nb game
                file.write('X ')            # date
            else:
                file.write(str(len(Paths[tim]))+' ')       #nb game
                LaDate = Paths[tim][-1][1]                # date
                file.write(LaDate[6:]+'/'+LaDate[4:6]+'/'+LaDate[:4]+' ')
                for p in Paths[tim]:           # path
                    file.write(' -> '+p[1]+'-'+p[0]+'@'+p[2])
            file.write('\n')
        file.close() 
