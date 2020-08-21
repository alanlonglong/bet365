import undetected_chromedriver as uc
import MySQLdb
import time


driver = uc.Chrome()
driver.get('https://bet365.com')

while True:
    try:
        left_menu_div = driver.find_elements_by_class_name("wn-WebNavModule")
        left_menu = left_menu_div[0].find_elements_by_class_name("wn-PreMatchGroup")
        break
    except:
        pass
        
while True:        
    try:
        elems=driver.find_elements_by_class_name('wn-PreMatchItem ')
        break
    except:
        pass
        
for elem in elems:
    if elem.text=='Basketball':
        elem.click()
        break
        
found_it=False
while not found_it:
    try:
        elems=driver.find_elements_by_class_name("sm-CouponLink_Title")
        for elem in elems:
            if 'Game Lines' in elem.text:
                elem.click()
                found_it=True
    except:
        pass
     
found_it=False
teams=[]
spread_lines=[]
spread_odds=[]
total_lines=[]
total_sides=[]
total_odds=[]
moneyline_odds=[]
dts=[]
fixtures=[]
while not found_it:
    try:
        teams=driver.find_elements_by_class_name('src-ParticipantFixtureDetailsHigher_Team')
        team_count=0
        for team in teams:
            if len(team.text)>0 and '<' not in team.text:
                teams.append(team.text)
                team_count+=1
                found_it=True
                
    except:
        pass
        
teams[:]=teams[int(len(teams)/2):] 
team_count=len(teams)
        
found_it=False  
while not found_it:
    try:
        line_count=0
        lines=driver.find_elements_by_class_name('sab-ParticipantCenteredStacked50OTB_Handicap')
        for line in lines:
            if len(line.text)>0 and ('+' in line.text or '-' in line.text) and line_count<team_count:
                spread_lines.append(line.text)
                line_count+=1
                found_it=True
            if len(line.text)>0 and ('O' in line.text or 'U' in line.text):
                total_sides.append(line.text.split()[0])
                total_lines.append(line.text.split()[1])
    except:
        pass
   
found_it=False
while not found_it:
    try:
        odds=driver.find_elements_by_class_name('sab-ParticipantCenteredStacked50OTB_Odds')
        odds_count=0
        for odd in odds:
            if len(odd.text)>0 and odds_count<team_count:
                spread_odds.append(odd.text)
                odds_count+=1
                found_it=True
            if len(odd.text)>0 and odds_count>=team_count-1:
                total_odds.append(odd.text)
                odds_count+=1
    except:
        pass

found_it=False
while not found_it:
    try:
        moneylines=driver.find_elements_by_class_name('sab-ParticipantOddsOnly50OTB_Odds')
        moneyline_count=0
        for moneyline in moneylines:
            if len(moneyline.text)>0 and moneyline_count<team_count:
                moneyline_odds.append(moneyline.text)
                moneyline_count+=1
                found_it=True
    except:
        pass
     
print(teams)
print(spread_lines)
print(spread_odds)
print(total_lines)
print(total_sides)
print(total_odds) 
print(moneyline_odds)

current_url=driver.current_url
while True:
    try:
        team_names=driver.find_elements_by_class_name('src-ParticipantFixtureDetailsHigher_TeamNames')
        num_team_names=len(team_names)
        break
    except:
        pass
        
i=0        
while i<num_team_names:
   
    while True:
        try:
            team_names=driver.find_elements_by_class_name('src-ParticipantFixtureDetailsHigher_TeamNames')
            fixtures.append(team_names[i].text)
            team_names[i].click()
            i+=1
            break
        except:
            pass
    
    while True:
        try:
            this_date=driver.find_element_by_class_name('sph-ExtraData_TimeStamp')
            dts.append(this_date.text)
            break
        except:
            pass
            
    driver.get(current_url)   

    while True:
        try:
            player_props=driver.find_element_by_class_name('sph-MarketGroupNavBarButton')
            player_props.click()
            break
        except:
            pass
    while True:
        try:
            more=driver.find_element_by_class_name('msl-ShowMore')
            more.click()
            break
        except:
            pass
    players=[]
    while True:
        try:
            these_players=driver.find_elements_by_class_name('srb-ParticipantLabelWithTeam_Name')
            for p in these_players:
                players.append(p.text)
            break
        except:
            pass

#print(dts)
#print(fixtures)
print(players)

db=MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="a6!modern", db="basketball")
cursor=db.cursor()
for team in teams:    
    sql="INSERT INTO teams (name) SELECT * FROM (SELECT '" + team + "' AS name) AS tmp WHERE NOT EXISTS (SELECT * FROM teams WHERE name = '" + team + "') LIMIT 1;"    
    cursor.execute(sql)

increment=0
for i in range(len(fixtures)):
    home_team_name=fixtures[i].split('\n')[0].strip()
    away_team_name=fixtures[i].split('\n')[1].strip()
    sql="SELECT id FROM teams WHERE name = '" + home_team_name + "';"
    cursor.execute(sql)
    home_result=cursor.fetchone()[0]
    sql="SELECT id FROM teams WHERE name = '" + away_team_name + "';"
    cursor.execute(sql)
    away_result=cursor.fetchone()[0]
    sql="INSERT INTO fixtures (dt, home_team_id, away_team_id) VALUES ('" + dts[i] + "'," + str(home_result) + "," + str(away_result) + ");"
    cursor.execute(sql)
    cursor.execute("SELECT LAST_INSERT_ID()")
    fixture_id=cursor.fetchone()[0]
    try:
        sql="INSERT INTO moneyline (fixture_id, team_id, odds) VALUES (" + str(fixture_id) + "," + str(home_result) + ",'" + moneyline_odds[i+increment] + "');"
        cursor.execute(sql)
        sql="INSERT INTO moneyline (fixture_id, team_id, odds) VALUES (" + str(fixture_id) + "," + str(away_result) + ",'" + moneyline_odds[i+1+increment] + "');"
        cursor.execute(sql)
    except:
        pass
    try:    
        sql="INSERT INTO spread (fixture_id, team_id, line, odds) VALUES (" + str(fixture_id) + "," + str(home_result) + ",'" + spread_lines[i+increment] + "','" + spread_odds[i] + "');"
        cursor.execute(sql)
        sql="INSERT INTO spread (fixture_id, team_id, line, odds) VALUES (" + str(fixture_id) + "," + str(away_result) + ",'" + spread_lines[i+1+increment] + "','" + spread_odds[i+1] + "');"
        cursor.execute(sql)
        
    except:
        pass
    try:    
        sql="INSERT INTO totalpoints (fixture_id, side, line, odds) VALUES (" + str(fixture_id) + "," + str(home_result) + ",'" + spread_lines[i+increment] + "','" + spread_odds[i] + "');"
        cursor.execute(sql)
        sql="INSERT INTO spread (fixture_id, team_id, line, odds) VALUES (" + str(fixture_id) + "," + str(away_result) + ",'" + spread_lines[i+1+increment] + "','" + spread_odds[i+1] + "');"
        cursor.execute(sql)
        
    except:
        pass    

    increment+=1

db.commit()    
cursor.close()
db.close()    
               

        
driver.close()        
        
        