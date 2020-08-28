import undetected_chromedriver as uc
import MySQLdb
import time

f=open('spiro.ini','r')
f_lines=f.readlines()
all_competitions=f_lines[0].split(':')[1].replace('\n','').split(',')
user=f_lines[1].split(':')[1].replace('\n','')
passwd=f_lines[2].split(':')[1].replace('\n','')
db=f_lines[4].split(':')[1].replace('\n','')
host=f_lines[3].split(':')[1].replace('\n','')

f.close()

db=MySQLdb.connect(host=host, port=3306, user=user, passwd=passwd, db=db)
cursor=db.cursor()

for competition in all_competitions:

    driver = uc.Chrome()
    #driver.implicitly_wait(10)
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
            down_arrow=driver.find_elements_by_css_selector("div.sm-SplashMarket_Header:not(.sm-SplashMarket_HeaderOpen)")
            time.sleep(3)
            for arrow in down_arrow:
                driver.execute_script("arguments[0].click();", arrow)
                found_it=True
        except:
            pass        
    time.sleep(5)     
       
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
    # loop through the number of fixtures and click on them to get data on each fixture (team_names=fixtures)
    #while i<num_team_names:
            
    stop=0
    start=time.time()
    while i<num_team_names:
        dts=[]
        fixtures=[]
        total_cards_odds=[]
        total_cards_line=[]
        total_cards_side=[]
        asian_total_cards_odds=[]
        asian_total_cards_line=[]
        asian_total_cards_side=[]
        team_cards_teams=[]
        team_cards_side=[]
        team_cards_line=[]
        team_cards_odds=[]
        players=[]
        player_odds=[]
        goalscorers=[]
        anytime_odds=[]
        alt_corner_lines=[]
        alt_corner_over_odds=[]
        alt_corner_exactly_odds=[]
        alt_corner_under_odds=[]
        corner_lines=[]
        corner_over_odds=[]
        corner_under_odds=[]
        corner_match_up_odds=[]
        corner_match_up_sides=[]
        asian_corner_lines=[]
        asian_corner_over_odds=[]
        asian_corner_under_odds=[]
        asian_handicap_teams=[]
        asian_handicap_lines=[]
        asian_handicap_odds=[]
        
        try:
            stop=time.time()
            team_names=driver.find_elements_by_class_name('rcl-ParticipantFixtureDetails_TeamNames')
            # if we already have these fixtures, we can move on to the next one
            home_team_name=team_names[i].text.split('\n')[0].strip()
            away_team_name=team_names[i].text.split('\n')[1].strip()
            sql="SELECT id FROM teams WHERE name = '" + home_team_name + "';"
            cursor.execute(sql)
            home_id=cursor.fetchone()       
            sql="SELECT id FROM teams WHERE name = '" + away_team_name + "';"
            cursor.execute(sql)
            away_id=cursor.fetchone()
            if home_id is not None and away_id is not None:
                sql="SELECT * FROM fixtures WHERE home_team_id = " + str(home_id[0]) + " AND away_team_id = " + str(away_id[0]) + ";"
                cursor.execute(sql)
                result=cursor.fetchone()

                if result is None:
                    fixtures.append(team_names[i].text)
                    team_names[i].click()
                    i+=1
                else:
                    i+=1
                    driver.get(current_url)
                    continue
            else:
                fixtures.append(team_names[i].text)
                team_names[i].click()
                i+=1
            
        except:
            stop=time.time()
            continue
    
        stop=0
        start=time.time()
        found_it=False
        while True and stop-start<10:
            try:
                stop=time.time()
                this_date=driver.find_element_by_class_name('sph-ExtraData_TimeStamp')
                dts.append(this_date.text)
                found_it=True
                break
            except:
                stop=time.time()
                pass
                
        if not found_it:
            i+=1
            driver.get(current_url)
            
        else:
            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    tabs=driver.find_elements_by_class_name('sph-MarketGroupNavBarButton')
                    for t in tabs:
                        if t.text=='Corners':
                            found_it=True
                            t.click()
                            break
                except:
                    stop=time.time()
                    pass 
                    
            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    headers=driver.find_elements_by_class_name('gl-MarketGroupButton_Text')
                    for h in headers:
                        if h.text=='Alternative Corners':
                            col1=driver.find_elements_by_xpath('//*[text() = "Alternative Corners"]/parent::div/parent::div/div[position()=2]/div/div')
                            for col in col1:
                                items=col.find_elements_by_class_name('srb-ParticipantLabelCentered_Name')
                                for item in items:
                                    alt_corner_lines.append(item.text)
                                    found_it=True
                                    
                            col2=driver.find_elements_by_xpath('//*[text() = "Alternative Corners"]/parent::div/parent::div/div[position()=2]/div/div[position()=2]')        
                            for col in col2:
                                items=col.find_elements_by_class_name('gl-ParticipantOddsOnly_Odds')
                                for item in items:
                                    alt_corner_over_odds.append(item.text)
                                    found_it=True  
                            print(alt_corner_over_odds)
                            col3=driver.find_elements_by_xpath('//*[text() = "Alternative Corners"]/parent::div/parent::div/div[position()=2]/div/div[position()=3]')        
                            for col in col3:
                                items=col.find_elements_by_class_name('gl-ParticipantOddsOnly_Odds')
                                for item in items:
                                    alt_corner_exactly_odds.append(item.text)
                                    found_it=True  

                            col4=driver.find_elements_by_xpath('//*[text() = "Alternative Corners"]/parent::div/parent::div/div[position()=2]/div/div[position()=4]')        
                            for col in col4:
                                items=col.find_elements_by_class_name('gl-ParticipantOddsOnly_Odds')
                                for item in items:
                                    alt_corner_under_odds.append(item.text)
                                    found_it=True
            
                except:
                    stop=time.time()
                    pass             
                    
            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    headers=driver.find_elements_by_class_name('gl-MarketGroupButton_Text')
                    for h in headers:
                        if h.text=='Corners':
                            col1=driver.find_elements_by_xpath('//*[text() = "Corners"]/parent::div/parent::div/div[position()=2]/div/div')
                            for col in col1:
                                items=col.find_elements_by_class_name('srb-ParticipantLabelCentered_Name')
                                for item in items:
                                    corner_lines.append(item.text)
                                    found_it=True
                                    
                            col2=driver.find_elements_by_xpath('//*[text() = "Corners"]/parent::div/parent::div/div[position()=2]/div/div[position()=2]')        
                            for col in col2:
                                items=col.find_elements_by_class_name('gl-ParticipantOddsOnly_Odds')
                                for item in items:
                                    corner_over_odds.append(item.text)
                                    found_it=True   

                            col4=driver.find_elements_by_xpath('//*[text() = "Corners"]/parent::div/parent::div/div[position()=2]/div/div[position()=3]')        
                            for col in col4:
                                items=col.find_elements_by_class_name('gl-ParticipantOddsOnly_Odds')
                                for item in items:
                                    corner_under_odds.append(item.text)
                                    found_it=True
            
                except:
                    stop=time.time()
                    pass
                    
            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    headers=driver.find_elements_by_class_name('gl-MarketGroupButton_Text')
                    for h in headers:
                        if h.text=='Asian Total Corners':
                            col1=driver.find_elements_by_xpath('//*[text() = "Asian Total Corners"]/parent::div/parent::div/div[position()=2]/div/div')
                            for col in col1:
                                items=col.find_elements_by_class_name('srb-ParticipantLabelCentered_Name')
                                for item in items:
                                    asian_corner_lines.append(item.text)
                                    found_it=True
                                    
                            col2=driver.find_elements_by_xpath('//*[text() = "Asian Total Corners"]/parent::div/parent::div/div[position()=2]/div/div[position()=2]')        
                            for col in col2:
                                items=col.find_elements_by_class_name('gl-ParticipantOddsOnly_Odds')
                                for item in items:
                                    asian_corner_over_odds.append(item.text)
                                    found_it=True   

                            col4=driver.find_elements_by_xpath('//*[text() = "Asian Total Corners"]/parent::div/parent::div/div[position()=2]/div/div[position()=3]')        
                            for col in col4:
                                items=col.find_elements_by_class_name('gl-ParticipantOddsOnly_Odds')
                                for item in items:
                                    asian_corner_under_odds.append(item.text)
                                    found_it=True
            
                except:
                    stop=time.time()
                    pass
                    
            print('Asian Total Corners: Done')        

            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    headers=driver.find_elements_by_class_name('gl-MarketGroupButton_Text')
                    for h in headers:
                        if h.text=='Asian Handicap Corners':
                            col1=driver.find_elements_by_xpath('//*[text() = "Asian Handicap Corners"]/parent::div/parent::div/div[position()=2]/div/div')
                            for col in col1:
                                items=col.find_elements_by_class_name('gl-MarketColumnHeader ')
                                items2=col.find_elements_by_class_name('gl-ParticipantCentered_Handicap')
                                items3=col.find_elements_by_class_name('gl-ParticipantCentered_Odds')
                                for item in items:
                                    asian_handicap_teams.append(item.text)
                                    found_it=True
                                for item in items2:
                                    asian_handicap_lines.append(item.text)
                                for item in items3:
                                    asian_handicap_odds.append(item.text)
            
                except:
                    stop=time.time()
                    pass
                    
            print('Asian Handicap Corners: Done')        

            found_it=False
            these_sides=['Home','Tie','Away']
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    headers=driver.find_elements_by_class_name('gl-MarketGroupButton_Text')
                    for h in headers:
                        if h.text=='Corner Match Up':
                            items=driver.find_elements_by_xpath('//*[text() = "Corner Match Up"]/parent::div/parent::div')
                            for item in items:
                                odds=item.find_elements_by_class_name('srb-ParticipantStackedBorderless_Odds')
                                k=0
                                for o in odds:
                                    corner_match_up_odds.append(o.text)
                                    corner_match_up_sides.append(these_sides[k])
                                    k+=1
                                    found_it=True
                except:
                    stop=time.time()
                    pass
                
            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    tabs=driver.find_elements_by_class_name('sph-MarketGroupNavBarButton')
                    for t in tabs:
                        if t.text=='Player':
                            found_it=True
                            t.click()
                            break
                except:
                    stop=time.time()
                    pass   

            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    more=driver.find_elements_by_class_name('msl-ShowMore_Link')
                    for m in more:
                        if m.text=='Show more':
                            m.click()
                            found_it=True
                            break
                except:
                    stop=time.time()
                    pass     

            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    show_less=driver.find_elements_by_class_name('msl-ShowMore_Link')
                    for sl in show_less:
                        if sl.text=='Show less':
                            found_it=True
                            break
                except:
                    stop=time.time()
                    pass
            
            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    headers=driver.find_elements_by_class_name('gl-MarketGroupButton_Text')
                    for h in headers:
                        if h.text=='Goalscorers':
                            scorers=driver.find_elements_by_class_name('srb-ParticipantLabel_Name')
                            for s in scorers:
                                if s.text != 'No Goalscorer':
                                    goalscorers.append(s.text)

                    anytime=driver.find_elements_by_class_name('gl-Market_General-lastinrow')           
                    a_odds=anytime[0].find_elements_by_class_name('gl-ParticipantOddsOnly_Odds')
                    for a in a_odds:
                        anytime_odds.append(a.text)
                        found_it=True
                except:
                    stop=time.time()
                    pass                
            
            print('Goalscorers: Done')
            
            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    cards=driver.find_elements_by_class_name('sph-MarketGroupNavBarButton')
                    for c in cards:
                        if c.text=='Cards':
                            found_it=True
                            c.click()
                            break
                except:
                    stop=time.time()
                    pass
                    
            print('Beginning Cards...')        
                    
            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    total_cards=driver.find_elements_by_class_name('gl-MarketGroupButton_Text')
                    for tc in total_cards:
                        if tc.text=='Number of Cards in Match':
                            lines=tc.find_elements_by_xpath('//*[text() = "Number of Cards in Match"]/parent::div/following-sibling::div/div/div/div[2]/div')
                            odds_over=tc.find_elements_by_xpath('//*[text() = "Number of Cards in Match"]/parent::div/following-sibling::div/div/div[position()=2]/div[position()=2]/span')
                            odds_under=tc.find_elements_by_xpath('//*[text() = "Number of Cards in Match"]/parent::div/following-sibling::div/div/div[position()=3]/div[position()=2]/span')
                            found_it=True
                            break
                    
                except:
                    stop=time.time()
                    pass
                    
            print('Number of Cards: Done')        
             
            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    total_cards=driver.find_elements_by_class_name('gl-MarketGroupButton_Text')
                    for tc in total_cards:
                        if tc.text=='Asian Total Cards':
                            asian_total_lines=tc.find_elements_by_xpath('//*[text() = "Asian Total Cards"]/parent::div/following-sibling::div/div/div/div[2]/div')
                            asian_total_odds_over=tc.find_elements_by_xpath('//*[text() = "Asian Total Cards"]/parent::div/following-sibling::div/div/div[position()=2]/div[position()=2]/span')
                            asian_total_odds_under=tc.find_elements_by_xpath('//*[text() = "Asian Total Cards"]/parent::div/following-sibling::div/div/div[position()=3]/div[position()=2]/span')
                            found_it=True
                            break
                    
                except:
                    stop=time.time()
                    pass
                    
            print('Asian Total Cards: Done')        
                    
            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    total_cards=driver.find_elements_by_class_name('gl-MarketGroupButton_Text')
                    for tc in total_cards:
                        if tc.text=='Team Cards':
                            team1=tc.find_elements_by_xpath('//*[text() = "Team Cards"]/parent::div/following-sibling::div/div/div/div')
                            team1over_line=tc.find_elements_by_xpath('//*[text() = "Team Cards"]/parent::div/following-sibling::div/div/div/div[position()=2]/span')
                            team1over_odds=tc.find_elements_by_xpath('//*[text() = "Team Cards"]/parent::div/following-sibling::div/div/div/div[position()=2]/span[position()=2]')
                            team1under_line=tc.find_elements_by_xpath('//*[text() = "Team Cards"]/parent::div/following-sibling::div/div/div/div[position()=3]/span')
                            team1under_odds=tc.find_elements_by_xpath('//*[text() = "Team Cards"]/parent::div/following-sibling::div/div/div/div[position()=3]/span[position()=2]')                        
                            
                            team2=tc.find_elements_by_xpath('//*[text() = "Team Cards"]/parent::div/following-sibling::div/div/div[position()=2]/div')
                            team2over_line=tc.find_elements_by_xpath('//*[text() = "Team Cards"]/parent::div/following-sibling::div/div/div[position()=2]/div[position()=2]/span')
                            team2over_odds=tc.find_elements_by_xpath('//*[text() = "Team Cards"]/parent::div/following-sibling::div/div/div[position()=2]/div[position()=2]/span[position()=2]')
                            team2under_line=tc.find_elements_by_xpath('//*[text() = "Team Cards"]/parent::div/following-sibling::div/div/div[position()=2]/div[position()=3]/span[position()=1]')
                            team2under_odds=tc.find_elements_by_xpath('//*[text() = "Team Cards"]/parent::div/following-sibling::div/div/div[position()=2]/div[position()=3]/span[position()=2]')
                            
                            found_it=True
                            break
                    
                except:
                    stop=time.time()
                    pass   
                    
            print('Team Cards: Done')        

            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    player_to_be_booked=driver.find_elements_by_class_name('gl-MarketGroupButton_Text')
                    for p in player_to_be_booked:
                        if p.text=='Player to be booked':
                            p.click()
                            found_it=True
                            break
                except:
                    stop=time.time()
                    pass
                    
            print('Player to be booked: Done')        
                    
            found_it=False
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    more=driver.find_elements_by_class_name('msl-ShowMore_Link')
                    for m in more:
                        if m.text=='Show more':
                            m.click()
                            found_it=True
                            break
                except:
                    stop=time.time()
                    pass
                    
            found_it=False
            stop=0
            start=time.time()
            while not found_it and stop-start<10:
                try:
                    stop=time.time()
                    player_odds=driver.find_elements_by_class_name('gl-Market_General-cn2')
                    for po in player_odds:
                        pl_o=po.text.split('\n')
                        if not isinstance(pl_o[1],str):
                            continue
                        
                        players.append(pl_o[0])
                        player_odds.append(pl_o[1])
                        found_it=True

                except:
                    stop=time.time()
                    pass
                    
            # we cut the list in half because the first half of the list ends up being garbage for some reason         
            player_odds[:]=player_odds[-len(players):]
            
            try:
                total_cards_line.append(lines[0].text) 
                total_cards_line.append(lines[0].text) 
                total_cards_side.append('Over')
                total_cards_side.append('Under')
                total_cards_odds.append(odds_over[0].text)
                total_cards_odds.append(odds_under[0].text)
            except:
                pass
            
            try:
                asian_total_cards_line.append(asian_total_lines[0].text)
                asian_total_cards_line.append(asian_total_lines[0].text)
                asian_total_cards_side.append('Over')
                asian_total_cards_side.append('Under')
                asian_total_cards_odds.append(asian_total_odds_over[0].text)
                asian_total_cards_odds.append(asian_total_odds_under[0].text)
            except:
                pass
            
            try:
                team_cards_teams.append(team1[0].text)
                team_cards_teams.append(team1[0].text)
                team_cards_teams.append(team2[0].text)
                team_cards_teams.append(team2[0].text)
            except:
                pass
            
            try:
                team_cards_side.append(team1over_line[0].text.split()[0])
                team_cards_side.append(team1under_line[0].text.split()[0])
                team_cards_line.append(team1over_line[0].text.split()[1])
                team_cards_line.append(team1under_line[0].text.split()[1])
                team_cards_odds.append(team1over_odds[0].text)
                team_cards_odds.append(team1under_odds[0].text)
            except:
                pass
                
            try:
                team_cards_side.append(team2over_line[0].text.split()[0])
                team_cards_side.append(team2under_line[0].text.split()[0])
                team_cards_line.append(team2over_line[0].text.split()[1])
                team_cards_line.append(team2under_line[0].text.split()[1])
                team_cards_odds.append(team2over_odds[0].text)
                team_cards_odds.append(team2under_odds[0].text)
            except:
                pass
        
            driver.get(current_url)                
            print('Get another fixture if one available')
            
            
            try:
                sql="INSERT INTO competitions (name) SELECT * FROM (SELECT '" + competition + "' AS name) AS tmp WHERE NOT EXISTS (SELECT * FROM competitions WHERE name = '" + competition + "') LIMIT 1;"
                cursor.execute(sql)
            except:
                pass
            
            try:
                for team in teams:    
                    sql="INSERT INTO teams (name) SELECT * FROM (SELECT '" + team + "' AS name) AS tmp WHERE NOT EXISTS (SELECT * FROM teams WHERE name = '" + team + "') LIMIT 1;"    
                    cursor.execute(sql)
            except:
                pass
                
            try:    
                for player in players:
                    sql="INSERT INTO players (name) SELECT * FROM (SELECT '" + player.replace("'","\\'") + "' AS name) AS tmp WHERE NOT EXISTS (SELECT * FROM players WHERE name = '" + player + "') LIMIT 1;"
                    cursor.execute(sql)
            except:
                pass

            try:
                for goalscorer in goalscorers:
                    sql="INSERT INTO players (name) SELECT * FROM (SELECT '" + goalscorer.replace("'","\\'") + "' AS name) AS tmp WHERE NOT EXISTS (SELECT * FROM players WHERE name = '" + goalscorer.replace("'","\\'") + "') LIMIT 1;"

                    cursor.execute(sql)
            except:
                pass
                
            increment=0
            increment2=0
            print('Fixtures = ' + str(fixtures))
            for m in range(len(fixtures)):
                home_team_name=fixtures[m].split('\n')[0].strip()
                away_team_name=fixtures[m].split('\n')[1].strip()
                sql="SELECT id FROM teams WHERE name = '" + home_team_name + "';"
                cursor.execute(sql)
                home_result=cursor.fetchone()[0]
                sql="SELECT id FROM teams WHERE name = '" + away_team_name + "';"
                cursor.execute(sql)
                away_result=cursor.fetchone()[0]
                sql="SELECT id FROM competitions WHERE name = '" + competition + "';"
                cursor.execute(sql)
                competition_id=cursor.fetchone()[0]
                sql="INSERT INTO fixtures (dt, home_team_id, away_team_id, competition_id) VALUES ('" + dts[m] + "'," + str(home_result) + "," + str(away_result) + "," + str(competition_id) + ");"
                cursor.execute(sql)
                cursor.execute("SELECT LAST_INSERT_ID()")
                fixture_id=cursor.fetchone()[0]
             
                try:
                    sql="INSERT INTO total_cards (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(total_cards_line[m+increment]) + "','" + total_cards_side[m+increment] + "','" + total_cards_odds[m+increment] + "');"
                    cursor.execute(sql)
                    sql="INSERT INTO total_cards (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(total_cards_line[m+1+increment]) + "','" + total_cards_side[m+1+increment] + "','" + total_cards_odds[m+1+increment] + "');"
                    cursor.execute(sql)
                except:
                    pass
                
                try:
                    sql="INSERT INTO asian_total_cards (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(asian_total_cards_line[m+increment]) + "','" + asian_total_cards_side[m+increment] + "','" + asian_total_cards_odds[m+increment] + "');"
                    cursor.execute(sql)
                    sql="INSERT INTO asian_total_cards (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(asian_total_cards_line[m+1+increment]) + "','" + asian_total_cards_side[m+1+increment] + "','" + asian_total_cards_odds[m+1+increment] + "');"
                    cursor.execute(sql)
                except:
                    pass
                
                try:
                    sql="INSERT INTO team_cards (fixture_id, team_id, line, side, odds) VALUES (" + str(fixture_id) + "," + str(home_result) + ",'" + team_cards_line[m+increment2] + "','" + team_cards_side[m+increment2] + "','" + team_cards_odds[m+increment2] + "');"
                    cursor.execute(sql)
                    
                    sql="INSERT INTO team_cards (fixture_id, team_id, line, side, odds) VALUES (" + str(fixture_id) + "," + str(home_result) + ",'" + team_cards_line[m+1+increment2] + "','" + team_cards_side[m+1+increment2] + "','" + team_cards_odds[m+1+increment2] + "');"
                    cursor.execute(sql)
                    
                    sql="INSERT INTO team_cards (fixture_id, team_id, line, side, odds) VALUES (" + str(fixture_id) + "," + str(away_result) + ",'" + team_cards_line[m+2+increment2] + "','" + team_cards_side[m+2+increment2] + "','" + team_cards_odds[m+2+increment2] + "');"
                    cursor.execute(sql)
                    
                    sql="INSERT INTO team_cards (fixture_id, team_id, line, side, odds) VALUES (" + str(fixture_id) + "," + str(away_result) + ",'" + team_cards_line[m+3+increment2] + "','" + team_cards_side[m+3+increment2] + "','" + team_cards_odds[m+3+increment2] + "');"
                    cursor.execute(sql)
                except:
                    pass
                
                try:
                    for j in range(len(players)):
                        sql="SELECT id FROM players WHERE name = '" + players[j].replace("'","\\'") + "';"
                        cursor.execute(sql)
                        player_id=cursor.fetchone()[0]
                        
                        sql="INSERT INTO player_to_be_carded (fixture_id, player_id, odds) VALUES (" + str(fixture_id) + "," + str(player_id) + ",'" + str(player_odds[j]) + "');"
                        cursor.execute(sql)
                except:
                    pass
                       
                try:    
                    for j in range(len(goalscorers)):
                        sql="SELECT id FROM players WHERE name = '" + goalscorers[j].replace("'","\\'") + "';"
                        cursor.execute(sql)
                        player_id=cursor.fetchone()[0]
                        
                        sql="INSERT INTO goalscorer (fixture_id, player_id, odds) VALUES (" + str(fixture_id) + "," + str(player_id) + ",'" + str(anytime_odds[j]) + "');"
                        cursor.execute(sql)
                except:
                    pass
                    
                try:    
                    for j in range(len(corner_over_odds)):
                        sql="INSERT INTO total_corners (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(corner_lines[j]) + "','Over','" + str(corner_over_odds[j]) + "');"
                        cursor.execute(sql)
                        sql="INSERT INTO total_corners (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(corner_lines[j]) + "','Under','" + str(corner_under_odds[j]) + "');"
                        cursor.execute(sql)
                except:
                    pass
                     
                try:    
                    for j in range(len(alt_corner_over_odds)):
                        sql="INSERT INTO total_corners (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(alt_corner_lines[j]) + "','Over','" + str(alt_corner_over_odds[j]) + "');"
                        cursor.execute(sql)
                        sql="INSERT INTO total_corners (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(alt_corner_lines[j]) + "','Exactly','" + str(alt_corner_exactly_odds[j]) + "');"
                        cursor.execute(sql)
                        sql="INSERT INTO total_corners (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(alt_corner_lines[j]) + "','Under','" + str(alt_corner_under_odds[j]) + "');"
                        cursor.execute(sql)
                except:
                    pass
                    
                try:    
                    for j in range(len(asian_corner_over_odds)):
                        sql="INSERT INTO asian_total_corners (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(asian_corner_lines[j]) + "','Over','" + str(asian_corner_over_odds[j]) + "');"
                        cursor.execute(sql)
                        sql="INSERT INTO asian_total_corners (fixture_id, line, side, odds) VALUES (" + str(fixture_id) + ",'" + str(asian_corner_lines[j]) + "','Under','" + str(asian_corner_under_odds[j]) + "');"
                        cursor.execute(sql)  
                except:
                    pass
                    
                try:
                    for j in range(len(corner_match_up_odds)):
                        sql="INSERT INTO corners_match_bet (fixture_id, side, odds) VALUES (" + str(fixture_id) + ",'" + str(corner_match_up_sides[j]) + "','" + str(corner_match_up_odds[j]) + "');"
                        cursor.execute(sql)
                except:
                    pass
                
                try:
                    for j in range(len(asian_handicap_odds)):
                        sql="SELECT id FROM teams WHERE name = '" + asian_handicap_teams[j] + "';"
                        cursor.execute(sql)
                        team=cursor.fetchone()[0]
                        sql="INSERT INTO asian_handicap_corners (fixture_id, team_id, line, odds) VALUES (" + str(fixture_id) + "," + str(team) + ",'" + str(asian_handicap_lines[j]) + "','" + str(asian_handicap_odds[j]) + "');"
                        cursor.execute(sql)
                except:
                    pass
                
                increment+=1
                increment2+=3
    
    db.commit()    
    cursor.close()
    db.close()           
    driver.close()           