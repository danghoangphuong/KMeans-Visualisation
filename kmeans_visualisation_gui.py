import numpy as np
import matplotlib.pyplot as plt
import pygame, sys
from random import randint
import math 
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")

class Button:
	def __init__(self, text, pos, description):
		self.text = text #text
		self.pos = pos #text position
		self.description = description #btn function 

	def draw_text_box(self,screen,Mouse_x,Mouse_y):
		des_font = pygame.font.Font('freesansbold.ttf', 25)
		btn_font = pygame.font.Font('freesansbold.ttf', 32)
		text_on_btn = btn_font.render(self.text, True, (255,255,255))
		self.text_box = text_on_btn.get_rect() #(0,0,x,y)		
		pygame.draw.rect(screen, (0,0,0), (self.pos[0]-15, self.pos[1]-15, self.text_box[2]+30, self.text_box[3]+30))
		screen.blit(text_on_btn, (self.pos))
		
		if self.is_mouse_on_btn(Mouse_x,Mouse_y): #check if mouse hover on btn
			#display function of each button
			description = des_font.render("Function: " + self.description, True, (255,255,255), (255,0,0)) 
			screen.blit(description, (50,560))
			#change textbox color
			pygame.draw.rect(screen, (255,0,0), (self.pos[0]-15, self.pos[1]-15, self.text_box[2]+30, self.text_box[3]+30))  
			screen.blit(text_on_btn, (self.pos))

	def is_mouse_on_btn(self,Mouse_x,Mouse_y): #check if mouse is on button
		if (self.pos[0]-15<Mouse_x<self.pos[0]-15+self.text_box[2]+30) and (self.pos[1]-15<Mouse_y<self.pos[1]-15+self.text_box[3]+30):
			return True

def notification(noti, not_btn_font,screen):
	noti_display = not_btn_font.render("Status: " + noti, True, (255,255,255), (255,0,0)) 
	screen.blit(noti_display, (50,650))

def is_mouse_on_panel(Mouse_x, Mouse_y):
	if (50 < Mouse_x < 750) and (50 < Mouse_y < 550):
		return True

def draw_data_point(data_points,screen):
	pos = data_points
	pygame.draw.circle(screen, (0,0,0), pos, 8)
	pygame.draw.circle(screen, (255,255,255), pos, 6)

def draw_cluster(cluster_pos, screen,CLUSTER_COLORS,k):
	pos = cluster_pos
	pygame.draw.circle(screen, CLUSTER_COLORS, cluster_pos, 12)

def customise():
	pygame_icon = pygame.image.load('hhhh.png')
	pygame.display.set_icon(pygame_icon)
	pygame.display.set_caption("Kmeans visualisation")
	screen = pygame.display.set_mode((1200,700))
	imp = pygame.image.load("back_ground.png")
	return screen, imp

def calc_distance(p1, p2):
	dimension = len(p1) 
	distance = 0
	for i in range(dimension):
		distance += (p1[i] - p2[i])**2
	return math.sqrt(distance)

def picture_compress():
	img = plt.imread("a.jpg") # shape -> (656, 561, 3) 

	height = img.shape [0] #rows
	width = img.shape[1] #columns

	img = img.reshape(height*width,3) # shape -> (368016, 3)

	kmeans = KMeans(n_clusters=3).fit(img)
	labels = kmeans.predict(img)
	clusters = kmeans.cluster_centers_

	new_img = np.zeros_like(img) # shape -> (368016, 3)

	for i in range(len(new_img)):
		new_img[i] = clusters[labels[i]]

	new_img = new_img.reshape(height,width,3) # shape -> (656, 561, 3)
	plt.imshow(new_img)
	new_pic = plt.savefig("img.jpg")	
	return new_pic

def update_k(K):
	k_newest = []
	k_newest.append(K)
	print(k_newest)
	return k_newest[-1]

def main():
	pygame.init() 
	screen, imp = customise()
	
	running = True
	BACKGROUND_PANEL = (249,255,230)
	clock = pygame.time.Clock()	
	not_btn_font = pygame.font.Font('freesansbold.ttf', 40)
	
	notifications = []
	
	#initial value of K and error
	K = update_k(0)
	error = 0
	
	# data point position
	data_points = []

	#cluster position 
	clusters = []
	labels = []

	# Cluster color
	RED = (255,0,0)
	GREEN = (0,255,0)
	BLUE = (0,0,255)
	YELLOW = (147,153,35)
	PURPLE = (255,0,255)
	SKY = (0,255,255)
	ORANGE = (255,125,25)
	GRAPE = (100,25,125)
	GRASS = (55,155,65)
	CLUSTER_COLORS = [RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]
	
	display_img = 0
	new_img = picture_compress()
	if K != 0:
		print("xxxx")

	while running:
		clock.tick(60)	
		screen.fill((214,214,214))	
		screen.blit(imp,(0,0)) #display background

		# draw panel
		pygame.draw.rect(screen, (0,0,0), (50, 50, 700, 500))
		pygame.draw.rect(screen, BACKGROUND_PANEL, (55,55,690,490))
		
		
		#get mouse position
		Mouse_x, Mouse_y = pygame.mouse.get_pos() # --> (mouseX, mouseY)
		mouse_font = pygame.font.Font('freesansbold.ttf', 15)
		if is_mouse_on_panel(Mouse_x,Mouse_y):
			mouse_pos = mouse_font.render("(" + str(Mouse_x-50) + "," + str(Mouse_y-50) + ")", True, (0,0,0))
			screen.blit(mouse_pos, (Mouse_x+10,Mouse_y))

		#K value
		text_k = not_btn_font.render('K = ' + str(K), True, (0,0,0))
		screen.blit(text_k, (1050,55))
		
		# plus btn
		btn_plus = Button('+', (860,60),"Increase K value")
		btn_plus.draw_text_box(screen,Mouse_x, Mouse_y)

		# minus btn
		btn_minus = Button('-', (960,60),"Decrease K value")
		btn_minus.draw_text_box(screen,Mouse_x, Mouse_y)

		# run btn
		btn_run = Button('RUN', (890,250), "Run without external library")
		btn_run.draw_text_box(screen,Mouse_x, Mouse_y)
		
		#algorithm btn
		btn_algorithm = Button('Algorithm', (850,350), "Run with external library")
		btn_algorithm.draw_text_box(screen,Mouse_x, Mouse_y)
		
		#reset btn
		btn_reset = Button('Reset', (870,630), "Reset program")
		btn_reset.draw_text_box(screen,Mouse_x, Mouse_y)

		#Random btn
		btn_random = Button('Random cluster', (815,550), "Create cluster")
		btn_random.draw_text_box(screen,Mouse_x, Mouse_y)

		# Picture compressed btn
		btn_compressed = Button('Picture compressed', (795,450), "Compress picture")
		btn_compressed.draw_text_box(screen,Mouse_x, Mouse_y)
		
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN: # check click
				if event.button == 1: # check left click	
					# create data point
					if is_mouse_on_panel(Mouse_x, Mouse_y):
						labels = []
						point = [Mouse_x-50, Mouse_y-50]
						data_points.append(point)

					# K+ button
					if btn_plus.is_mouse_on_btn(Mouse_x,Mouse_y):
						if 0 <= K < 9:
							K += 1 	
							noti = "K value has been increased !"
							notifications.append(noti)
							update_k(K)
						
					# K- button
					if btn_minus.is_mouse_on_btn(Mouse_x,Mouse_y):
						if K > 0:
							K -= 1 	
							noti = "K value has been decreased !"
							notifications.append(noti)

					# random button draw cluster
					if btn_random.is_mouse_on_btn(Mouse_x,Mouse_y):
						clusters = [] # --> (pos1, pos2) 
						noti = "Create cluster !"
						notifications.append(noti)
						for i in range(K):
							cluster_pos = [randint(0,700), randint(0,500)] #random pos
							clusters.append(cluster_pos) #create list of position
					
					# run button 
					if btn_run.is_mouse_on_btn(Mouse_x,Mouse_y):
						noti = "Run algorithm !"
						notifications.append(noti)
						labels = []
						# calculate distance from point to cluster to assign label
						try:
							for p in data_points:
								distances = [] #value when calc distance from each p to c
								for c in clusters:
									distance = calc_distance(p, c) #calculate distance from each point to clusters 
									distances.append(distance)
									
								min_distance = min(distances) #find min distance
								#find index to assign label
								idx_min = distances.index(min_distance)# -->0/1/...
								labels.append(idx_min) #assign label
						except:
							noti = "Check cluster first !"
							notifications.append(noti)
						
						# change cluster centroid position 
						for i in range(K):
							sum_x = 0 
							sum_y = 0
							point_count = 0 
							for j in range(len(data_points)):
								if i == labels[j]:
									sum_x += data_points[j][0]
									sum_y += data_points[j][1]
									point_count += 1
							if point_count != 0:
								#new pos = average pos
								new_x = sum_x/point_count 
								new_y = sum_y/point_count
								clusters[i] = [new_x, new_y] #update position

					# algorithm button 
					if btn_algorithm.is_mouse_on_btn(Mouse_x, Mouse_y):
						try:
							noti = "Scikit learn used!"
							notifications.append(noti)
							kmeans = KMeans(n_clusters=K).fit(data_points)
							labels = kmeans.predict(data_points)
							clusters = kmeans.cluster_centers_
						except:
							noti = "Check K and data points!"
							notifications.append(noti)

					# reset button
					if btn_reset.is_mouse_on_btn(Mouse_x,Mouse_y):
						noti = "System reset !"
						notifications.append(noti)
						display_img = 0
						clusters = []
						K = 0 
						data_points = []
						labels = []

					#picture compress button
					if btn_compressed.is_mouse_on_btn(Mouse_x, Mouse_y):
						noti = "Processing..."
						notifications.append(noti)
						display_img = 1
						ori_img = pygame.image.load("a.jpg")
						new_img = pygame.image.load("img.jpg")

			if event.type == pygame.QUIT:
				running = False

		# draw data point 
		for i in range(len(data_points)):
			draw_data_point((data_points[i][0]+50,data_points[i][1]+50),screen) #data_points[i] --> (Mouse_x, Mouse_y)
			#assign label 
			if len(labels) !=0:
				pygame.draw.circle(screen, CLUSTER_COLORS[labels[i]], (data_points[i][0]+50,data_points[i][1]+50), 6)

		# draw cluster 
		for i in range(len(clusters)):
			draw_cluster((clusters[i][0]+50,clusters[i][1]+50),screen,CLUSTER_COLORS[i],K)

		# display notification 
		for i in range(len(notifications)):
			notification(notifications[-1], not_btn_font, screen)
		
		#calculate error
		distance_calc = 0
		error = 0
		if labels != [] and clusters != []:
			distance_square = [] #error = (sum of all distances)^2
			for i in range(len(data_points)):
				distance_calc += calc_distance(data_points[i], clusters[labels[i]])
				distance_square.append(distance_calc)
				error += distance_square[i]**2
		
		text_error = not_btn_font.render('ERROR = ' + str(int(error)), True, (0,0,0))
		screen.blit(text_error, (830,155))
		
		# display picture 
		if display_img == 1:
			screen.blit(new_img, (550, 50))
			screen.blit(ori_img, (50, 50))

		pygame.display.flip()	

	pygame.quit()


main()
