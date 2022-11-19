#Play this game to gather training data.
#replace with directory file
directory = "PATH/.json"
# List
# Dict: Body-List-Body, Head-List-Head, Apple-List-Apples, HeadDirection-List-WASD, Border-List-Border
LearningData = {"Data": []}
import turtle
import time
import random
import json


class player():
	score = 0
	oldx = 0
	oldy = 0
	delay = False

running = True
delay1 = 0.1
delay2 = 0 #0.005
apples = []
#apples  = [[PositionX,PositionY]]
snakes= []
#snakes = [[turtlesnake,PositionX,PositionY,LastPositionX,LastPositionY]]

wn = turtle.Screen()
wn.title('Snake')
wn.bgcolor('white')
wn.setup(width=800, height=600)
wn.tracer(0)

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = "up"

def dead():
	print("lost")
	running = False
	return running

def movebody(x,y):
	for i in range(len(snakes)):
		if i == 0:
			frame = snakes[i][0]
			snakes[i][3] = frame.xcor()
			snakes[i][4] = frame.ycor()
			frame.goto(player.oldx,player.oldy)
			snakes[i][1] = player.oldx
			snakes[i][2] = player.oldy
		else:
			frame = snakes[i][0]
			snakes[i][3] = frame.xcor()
			snakes[i][4] = frame.ycor()
			frame.goto(snakes[i-1][3],snakes[i-1][4])
			snakes[i][1] = snakes[i-1][3]
			snakes[i][2] = snakes[i-1][4]


def snakemove():
	player.oldx = head.xcor()
	player.oldy = head.ycor()
	if head.direction == "up":
		y = head.ycor()
		head.sety(y + 20)
		movebody(head.xcor(),head.ycor())
		if y == 300:
			print("Dead")
			return dead(),head.direction
		else:
			for i in range(len(snakes)):
				x = head.xcor()
				y = head.ycor()
				if x == snakes[i][1]:
					if y == snakes[i][2]:
						print("Lost")
						return False,head.direction

		return True,head.direction
	elif head.direction == "down":
		y = head.ycor()
		head.sety(y - 20)
		movebody(head.xcor(),head.ycor())
		if y == -300:
			print("Dead")
			return dead(),head.direction
		else:
			for i in range(len(snakes)):
				x = head.xcor()
				y = head.ycor()
				if x == snakes[i][1]:
					if y == snakes[i][2]:
						print("Lost")
						return False,head.direction

		return True,head.direction
	elif head.direction == "left":
		x = head.xcor()
		head.setx(x - 20)
		movebody(head.xcor(),head.ycor())
		if x == -400:
			print("Dead")
			return dead(),head.direction
		else:
			for i in range(len(snakes)):
				x = head.xcor()
				y = head.ycor()
				if x == snakes[i][1]:
					if y == snakes[i][2]:
						print("Lost")
						return False,head.direction

		return True,head.direction
	elif head.direction == "right":
		x = head.xcor()
		head.setx(x + 20)
		movebody(head.xcor(),head.ycor())

		if x == 400:
			print("Dead")
			return dead(),head.direction
		else:
			for i in range(len(snakes)):
				x = head.xcor()
				y = head.ycor()
				if x == snakes[i][1]:
					if y == snakes[i][2]:
						print("Lost")
						return False,head.direction

		return True,head.direction
		
def go_up():
	if player.delay == False:
		if head.direction != "down":
			player.delay = True
			head.direction = "up"
	
def go_down():
	if player.delay == False:
		if head.direction != "up":
			player.delay = True
			head.direction = "down"
	
def go_left():
	if player.delay == False:
		if head.direction != "right":
			player.delay = True
			head.direction = "left"
	
def go_right():
	if player.delay == False:
		if head.direction != "left":
			player.delay = True
			head.direction = "right"
	
def spawnhead(x,y):
	headpart = turtle.Turtle()
	headpart.speed(0)
	headpart.shape("circle")
	headpart.color("green")
	headpart.penup()
	headpart.goto(x,y)
	snakes.insert(len(snakes)+1,[headpart,headpart.xcor(),headpart.ycor(),player.oldx,player.oldy])


def spawnapple(apples,head):
	lowx = -380
	highx = 380
	lowy = -280
	highy = 280
	basemove = 20
	if len(apples) == 0:
		#print("Spawn Apple")
		apple = turtle.Turtle()
		apple.speed(0)
		apple.shape("circle")
		apple.color("red")
		apple.penup()
		randomx = random.randint(lowx/basemove,highx/basemove)
		randomy = random.randint(lowy/basemove,highy/basemove)
		apple.goto(randomx*basemove,randomy*basemove)
		apples.insert(0,[randomx*basemove,randomy*basemove,apple])
	else:
		x = head.xcor()
		y = head.ycor()
		#print("Head",x,y)
		#print(apples[0][0],apples[0][1])
		if apples[0][0] == x:
			if apples[0][1] == y:
				apples[0][2].hideturtle()
				player.score = player.score +1
				apples.remove(apples[0])
				spawnhead(x,y)


#Muss ich noch lernen :D
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")


while running == True:
	wn.update()	
	running,headdirection = snakemove()
	time.sleep(delay2)
	player.delay = False
	time.sleep(delay1)
	spawnapple(apples,head)
	
	if running == False:
		break
	elif len(apples) > 0:
		newTab = []
		for i in range(len(snakes)):
			newTab.append([snakes[i][1],snakes[i][2],snakes[i][3],snakes[i][4]])
		#print(newTab)
		LearningData["Data"].append({"Body" : newTab,"HeadDirection" : [headdirection,head.xcor(),head.ycor()],"Apple" : [apples[0][0],apples[0][1]],"Border":[800,600]})

		# List
		# Dict: Body-List-Body, Head-List-Head, Apple-List-Apples, HeadDirection-List-WASD, Border-List-Border

def getInput(LearningData,ind):
	UnpackedData = []
	lData = LearningData["Data"][ind]
	baseLeft = 0
	baseTop = 0
	baseRight = 0
	baseBottom = 0
	baseX = lData["HeadDirection"][1]
	baseY = lData["HeadDirection"][2]
	baseLeftminX = lData["HeadDirection"][1]-20
	baseBottomminY = lData["HeadDirection"][2]-20
	baseRightposX = lData["HeadDirection"][1]+20
	baseTopposY = lData["HeadDirection"][2]+20
	#Apples
	if lData["Apple"][0] == baseLeftminX and baseY == lData["Apple"][1]:
		baseLeft = 1
	if lData["Apple"][0] == baseRightposX and baseY == lData["Apple"][1]:
		baseRight = 1
	if lData["Apple"][1] == baseBottomminY and baseX == lData["Apple"][0]:
		baseTop = 1
	if lData["Apple"][1] == baseTopposY and baseX == lData["Apple"][0]:
		baseBottom = 1
	#Borders
	if baseLeftminX == -420:
		baseLeft = -1
	if baseRightposX == 420:
		baseRight = -1
	if baseTopposY == -320:
		baseTop = -1
	if baseBottomminY == 320:
		baseBottom = -1
	#BodyHitBox
	tab = lData["Body"]
	for i in range(len(tab)):
		posX = tab[i][0]
		posY = tab[i][1]
		if posX == baseLeftminX:
			baseLeft = -1
		if posX == baseRightposX:
			baseRight = -1
		if posY == baseTopposY:
			baseTop = -1
		if posY == baseBottomminY:
			baseBottom = -1
	baseLeft2 = 0
	baseTop2 = 0
	baseRight2 = 0
	baseBottom2 = 0
	if lData["HeadDirection"][0] == "up":
		baseBottom = -1
	elif lData["HeadDirection"][0] == "right":
		baseLeft = -1
	elif lData["HeadDirection"][0] == "down":
		baseTop = -1
	elif lData["HeadDirection"][0] == "left":
		baseRight = -1
	else: 
		print("Wtf u stooopid!")
	UnpackedData.append(baseLeft)
	UnpackedData.append(baseTop)
	UnpackedData.append(baseRight)
	UnpackedData.append(baseBottom)
	#UnpackedData[len(UnpackedData)-1] = None
	#print(UnpackedData)
	return UnpackedData

def getWished(LearningData2):
	for i in range(len(LearningData2["Data"])-1):
		inp = getInput(LearningData2,i)
		UnpackedData = []
		lData = LearningData2["Data"][i-1]
		lDataFut = LearningData2["Data"][i]
		baseBottom = 0
		baseLeft = 0
		baseTop = 0
		baseRight = 0
		if lDataFut["HeadDirection"][0] == "up":
			baseTop = 1
		elif lDataFut["HeadDirection"][0] == "right":
			baseRight = 1
		elif lDataFut["HeadDirection"][0] == "down":
			baseBottom = 1
		elif lDataFut["HeadDirection"][0] == "left":
			baseLeft = 1
		UnpackedData.append(baseLeft)
		UnpackedData.append(baseTop)
		UnpackedData.append(baseRight)
		UnpackedData.append(baseBottom)
		LearningData2["Data"][i-1]["InputData"] = inp
		LearningData2["Data"][i-1]["WishData"] = UnpackedData
		#print(LearningData)
	return LearningData

getWished(LearningData)
LearningData["Data"].pop()

with open(directory, "w") as outfile:
    json.dump(LearningData, outfile)

with open(directory) as json_file:
    data = json.load(json_file)
print("Done")
text = "Your Score is ",player.score
turtle.write(text,True,"center",("Arial",40,"normal"))

#input("\n")