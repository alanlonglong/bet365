import undetected_chromedriver as uc
import MySQLdb
import time



f=open('spiro.ini','r')
lines=f.readlines()
all_competitions=lines[0].split(':')[1].split(',')

f.close()

for competition in all_competitions:

    

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
            elems=driver.find_elements_by_class_name('wn-PreMatchItem')
            break
        except:
            pass
            
    for elem in elems:
        if elem.text=='Soccer':
            elem.click()
            break
                    
    found_it=False      
    while not found_it:
        try:
            competitions=driver.find_elements_by_class_name('sm-CouponLink_Title')
            for c in competitions:
                if c.text==competition:
                    found_it=True
                    driver.execute_script("arguments[0].click();", c)
                    break
        except:
            pass

    found_it=False
    teams=[]      
    team_count=0  
    while not found_it:
        try:
            teams=driver.find_elements_by_class_name('rcl-ParticipantFixtureDetails_Team')
            team_count=0
            for team in teams:
                if len(team.text)>0 and '<' not in team.text:
                    teams.append(team.text)
                    team_count+=1
                    found_it=True
                    
        except:
            pass
    
    dts=[]
    fixtures=[]
    total_cards_odds=[]
    total_cards_line=[]
    total_cards_side=[]
    # we cut the list in half because the first half of the list ends up being garbage for some reason
    teams[:]=teams[int(len(teams)/2):] 
    team_count=len(teams)  

    # collect the fixtures to see how many and then go through them all so you can click on them and get the dates
    current_url=driver.current_url
    while True:
        try:
            team_names=driver.find_elements_by_class_name('rcl-ParticipantFixtureDetails_TeamNames')
            num_team_names=len(team_names)
            break
        except:
            pass
            
    i=0        
    while i<num_team_names:
       
        while True:
            try:
                team_names=driver.find_elements_by_class_name('rcl-ParticipantFixtureDetails_TeamNames')
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
                
        found_it=False
        while not found_it:
            try:
                cards=driver.find_elements_by_class_name('sph-MarketGroupNavBarButton')
                for c in cards:
                    if c.text=='Cards':
                        found_it=True
                        c.click()
                        break
            except:
                pass
                
        found_it=False
        while not found_it:
            try:
                total_cards=driver.find_elements_by_class_name('gl-MarketGroupButton_Text')
                for tc in total_cards:
                    if tc.text=='Number of Cards in Match':
                        lines=tc.find_elements_by_xpath('//*[text() = "Number of Cards in Match"]/parent::div/following-sibling::div/div/div[1]/div')
                        odds_over=tc.find_elements_by_xpath('//*[text() = "Number of Cards in Match"]/parent::div/following-sibling::div/div/div[position()=2]/div[position()=2]/span')
                        odds_under=tc.find_elements_by_xpath('//*[text() = "Number of Cards in Match"]/parent::div/following-sibling::div/div/div[position()=3]/div[position()=2]/span')
                        found_it=True
                        break
                
            except:
                pass
        total_cards_line.append(lines[1].text) # first line is an empty space
        total_cards_line.append(lines[1].text) # first line is an empty space
        total_cards_side.append('Over')
        total_cards_side.append('Under')
        total_cards_odds.append(odds_over[0].text)
        total_cards_odds.append(odds_under[0].text)
        driver.get(current_url)  

    db=MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="a6!modern", db="football")
    cursor=db.cursor()
    
    sql="INSERT INTO competitions (name) SELECT * FROM (SELECT '" + competition + "' AS name) AS tmp WHERE NOT EXISTS (SELECT * FROM competitions WHERE name = '" + competition + "') LIMIT 1;"
    cursor.execute(sql)
    
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
        sql="SELECT id FROM competitions WHERE name = '" + competition + "';"
        cursor.execute(sql)
        competition_id=cursor.fetchone()[0]
        sql="INSERT INTO fixtures (dt, home_team_id, away_team_id, competition_id) VALUES ('" + dts[i] + "'," + str(home_result) + "," + str(away_result) + "," + str(competition_id) + ");"
        cursor.execute(sql)
        cursor.execute("SELECT LAST_INSERT_ID()")
        fixture_id=cursor.fetchone()[0]
     
        sql="INSERT INTO total_cards (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(total_cards_line[i+increment]) + "','" + total_cards_side[i+increment] + "','" + total_cards_odds[i+increment] + "');"
        cursor.execute(sql)
        sql="INSERT INTO total_cards (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(total_cards_line[i+1+increment]) + "','" + total_cards_side[i+1+increment] + "','" + total_cards_odds[i+1+increment] + "');"
        cursor.execute(sql)
        
        increment+=1
        
    
    db.commit()    
    cursor.close()
    db.close()    
                   
    
            
            
    driver.close()        
        
        