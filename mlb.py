
from urllib.request import urlopen

import codecs
import json
import operator
month_list=['01','02','03','04','05','06','07','08','09','10','11','12']
date_list =['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
date_ = []
big_month = range(31)
small_month = range(30)
luna_month = range(29)	# 2016 special !
class Game:
	def __init__(self,away,home):
		self.away = away
		self.away_rate = -1
		self.home = home
		self.home_rate = -1
		self.final_away_rate = -1
		self.final_home_rate = -1
		self.away_loserate =-1
		self.home_loserate =-1
		self.final_away_loserate = -1
		self.final_home_loserate = -1
	def awayrate(self,away_rate):
		self.away_rate = away_rate
	def homerate(self,home_rate):
		self.home_rate = home_rate
	def awayloserate(self,away_loserate):
		self.away_loserate = away_loserate
	def homeloserate(self,home_loserate):
		self.home_loserate = home_loserate
	def finalrate(self):
		#if (self.home_rate+self.away_rate) == 0:
		#	self.final_away_rate=format(50,'.2%')
		#	self.final_home_rate=format(50,'.2%')
		
		self.final_away_rate=format(self.away_rate * 1/(self.home_rate+self.away_rate),'.2%')
		self.final_home_rate=format(self.home_rate * 1/(self.home_rate+self.away_rate),'.2%')
		self.final_away_loserate = format(self.away_loserate * 1/(self.home_loserate+self.away_loserate),'.2%')
		self.final_home_loserate = format(self.home_loserate * 1/(self.home_loserate+self.away_loserate),'.2%')
class Team:
	def __init__(self,name):
		self.name = name
		self.away_win = 0
		self.home_win = 0
		self.away_lose = 0
		self.home_lose = 0
		self.yesterday = "none"
		self.win_streak_count = 0
		self.win_streak_max = 0
		self.win_streak_board = []
		self.lose_streak_count = 0
		self.lose_streak_board = []
		self.lose_streak_max = 0
		
	def homewinGame(self):
		self.home_win += 1
		
		self.win_streak()
	def homeloseGame(self):
		self.home_lose += 1
		
		self.lose_streak()
	def awaywinGame(self):
		self.away_win += 1
		
		self.win_streak()
	def awayloseGame(self):
		self.away_lose += 1
		
		self.lose_streak()
	def win_streak(self): #連勝
		if self.yesterday == "win":   
			self.win_streak_board[self.win_streak_count-1] -=1
			self.win_streak_count += 1
			if self.win_streak_max < self.win_streak_count :
				self.win_streak_board.append(1)
				self.win_streak_max = self.win_streak_count
			else :
				self.win_streak_board[self.win_streak_count-1] +=1
		elif self.yesterday == "none": #第一場
			self.yesterday = "win"
			self.win_streak_board.append(1)
			self.win_streak_count += 1
			self.win_streak_max += 1
		else :
			self.yesterday = "win"   #止敗
			self.win_streak_count = 1
			self.lose_streak_count = 0
			if self.win_streak_max < self.win_streak_count :
				self.win_streak_board.append(1)
				self.win_streak_max = self.win_streak_count
			else :
				self.win_streak_board[self.win_streak_count-1] +=1
	def lose_streak(self): #連敗
		if self.yesterday == "lose":   
			self.lose_streak_board[self.lose_streak_count-1] -=1
			self.lose_streak_count += 1
			if self.lose_streak_max < self.lose_streak_count :
				self.lose_streak_board.append(1)
				self.lose_streak_max = self.lose_streak_count
			else :
				self.lose_streak_board[self.lose_streak_count-1] +=1
		elif self.yesterday == "none": #第一場
			self.yesterday = "lose"
			self.lose_streak_board.append(1)
			self.lose_streak_count += 1
			self.lose_streak_max += 1
		else :
			self.yesterday = "lose"   #止勝
			self.lose_streak_count = 1
			self.win_streak_count = 0
			if self.lose_streak_max < self.lose_streak_count :
				self.lose_streak_board.append(1)
				self.lose_streak_max = self.lose_streak_count
			else :
				self.lose_streak_board[self.lose_streak_count-1] +=1
for i in range(12):
	month = i + 1
	if(month == 1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):
		date_.append(big_month)
	elif(month == 4 or month==6 or month==9 or month==11):
		date_.append(small_month)
	elif(month == 2):
		date_.append(luna_month)


x = 0
team_list =['Red Sox','Nationals','Pirates','Cardinals','Blue Jays','Athletics','Rays','Angels',
'Rockies','Mariners','Braves','Yankees','Giants','Reds','Dodgers','Marlins','Orioles','Twins',
'Mets','Phillies','Indians','Padres','Cubs','White Sox','Royals','Astros','Tigers','D-backs',
'Brewers','Rangers']
team = []
team_ws_ls = []
#team standing
for x in team_list:
	team.append(Team(x))
	
month_count = 4-1 #began on april third
date_count =  3-1
total_games = 0
postpone_games = 0

while month_count < 8-1 or date_count < 6-1:
	
	x=0
	
	month = month_list[month_count]	
	date=date_list[date_count]
	#f = open(month+date, 'w', encoding = 'UTF-8')
	print (month,date)
	url = 'http://mlb.mlb.com/gdcross/components/game/mlb/year_2016/month_'+month+'/day_'+date+'/master_scoreboard.json'
	response = urlopen(url)  
	reader = codecs.getreader("utf-8")
	data = json.load(reader(response))
	
	ddd = len(data["data"]["games"]["game"])
	total_games += ddd
	while x <ddd:
		
		d = data["data"]["games"]["game"][x]
		#f.write(d["home_team_name"]+"@"+d["away_team_name"]+"\n")
		#print (d["status"]["status"])
		if d["status"]["status"]=="Final":
			if int(d["linescore"]["r"]["home"]) > int(d["linescore"]["r"]["away"]):
				h = "win"
				a = "lose"
				
				
			elif int(d["linescore"]["r"]["home"]) < int(d["linescore"]["r"]["away"]):
				a = "win"
				h = "lose"
				
			y = 0
			if h == "win":
				for it in team:
					if it.name == d["home_team_name"]:
						it.homewinGame()
					if it.name == d["away_team_name"]:
						it.awayloseGame()
			elif h == "lose":
				for it in team:
					if it.name == d["home_team_name"]:
						it.homeloseGame()
					if it.name == d["away_team_name"]:
						it.awaywinGame()
			#print(d["home_team_name"],d["linescore"]["r"]["home"],h)
			#print(d["away_team_name"],d["linescore"]["r"]["away"],a,"\n")
		else :
			postpone_games += 1
			#print(d["home_team_name"],"cancel")
			#print(d["away_team_name"],"cancel","\n")
		x += 1
	#f.close()
	date_count += 1
	if date_count == len(date_[month_count]) :
		date_count = 0
		month_count +=1
	if month_count == 6:
			if  date_count == 10 :
				date_count+=4
################### 預測明天的比賽
#month = month_list[month_count]	
date=date_list[date_count]
print ("Tomorrow is:",month_count+1," ",date_count+1)
url = 'http://mlb.mlb.com/gdcross/components/game/mlb/year_2016/month_'+month+'/day_'+date+'/master_scoreboard.json'
response = urlopen(url)  
reader = codecs.getreader("utf-8")
data = json.load(reader(response))

ddd = len(data["data"]["games"]["game"])

game = []


#################### 



#for x in sorted(team, key=operator.attrgetter('win'), reverse=True):   #各隊的勝排行
#	print (x.name,x.win,x.lose)

for y in range(ddd):
	d = data["data"]["games"]["game"][y-1]
	game.append(Game(d["away_team_name"],d["home_team_name"]))

for ii in game:
	
	for it in team:
		if ii.away == it.name:
			win_p = 0#各個連勝數總和
			win_o = 0#目前連勝以上
			for count in range(len(it.win_streak_board)) :
				win_p += it.win_streak_board[count-1]
				if count >= it.win_streak_count:
					win_o += it.win_streak_board[count-1]
			win_p -= 1
			win_o -= 1
			
			lose_p = 0
			lose_o = 0
			for count in range(len(it.lose_streak_board)) :
				lose_p += it.lose_streak_board[count-1]
				if count >= it.lose_streak_count:
					lose_o += it.lose_streak_board[count-1]
			if it.win_streak_max == it.win_streak_count:
				ii.awayrate(0)
			elif it.lose_streak_max == it.lose_streak_count:
				ii.awayloserate(0)
			else:
				ii.awayrate(win_o/win_p*it.away_win/(it.away_win+it.away_lose))
				ii.awayloserate(lose_o/lose_p*it.away_lose/(it.away_win+it.away_lose))
		elif ii.home == it.name:
			win_p = 0#各個連勝數總和
			win_o = 0#目前連勝以上
			for count in range(len(it.win_streak_board)) :
				win_p += it.win_streak_board[count-1]
				if count >= it.win_streak_count:
					win_o += it.win_streak_board[count-1]
			win_p -= 1
			win_o -= 1
			
			lose_p = 0
			lose_o = 0
			for count in range(len(it.lose_streak_board)) :
				lose_p += it.lose_streak_board[count-1]
				if count >= it.lose_streak_count:
					lose_o += it.lose_streak_board[count-1]
			if it.win_streak_max == it.win_streak_count:
				ii.homerate(0)
			elif it.lose_streak_max == it.lose_streak_count:
				ii.homeloserate(0)
			else:
				ii.homerate(win_o/win_p*it.home_win/(it.home_win+it.home_lose))
				ii.homeloserate(lose_o/lose_p*it.home_lose/(it.home_win+it.home_lose))
		
		

for z in game:
	z.finalrate()
	print ()
	print (z.away,"@",z.home)
	print (z.final_away_rate,"@",z.final_home_rate)
	print (z.final_home_loserate,"@",z.final_away_loserate) #敗率要互換
	if z.final_away_rate > z.final_home_rate and z.final_home_loserate > z.final_away_loserate :
		print ("不錯喔")
	elif z.final_away_rate < z.final_home_rate and z.final_home_loserate < z.final_away_loserate:
		print ("不錯喔")
