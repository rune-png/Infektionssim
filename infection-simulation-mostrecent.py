import tkinter as tk
import tkinter.ttk as ttk
import time
import random
import sys
import matplotlib.pyplot as plt
n = 200 # How many agents are on the Canvas
stopper = 0.8
class Person(object):
    # Constructor: creates a new person/agent
    def __init__(self, canvas, x, y, fill):
        # Calculate parameters for the oval/circle to be drawn
        r = 4 # The radius of the agents circle, how big they are
        x0 = x-r
        y0 = y-r
        x1 = x+r
        y1 = y+r

        # Initialize the agents attributrs
        self.x = x
        self.y = y
        self.infected = False
        self.isolation = False
        self.isolation_timer = 0
        self.immune = False 
        self.infectedtimer = 0
        if random.random() > stopper:
            self.smittestop = True
        else:
            self.smittestop = False

        self.kontakter = []
        n = False
        self.canvas = canvas
        self.circle_id = canvas.create_oval(x0,y0,x1,y1, fill=fill, outline='')
        

    # A  Method that moves the agents a random number between +5 or minus -5 on the x and y values
    def move(self):
        x1, y1, x2, y2 = self.canvas.bbox(self.circle_id)
        if not self.isolation:
            dx = random.choice([-5, 5])
            dy = random.choice([-5, 5])

            self.canvas.move(self.circle_id, dx, dy)
            self.x = self.x + dx
            self.y = self.y + dy
        
        self.agent_isolationtimer()
        self.agent_infectedtimer() 
        self.agent_smittestop()

    # A method that is called if someone with smittestop has been infected
    def notifikation(self):
        self.canvas.itemconfig(self.circle_id, fill='orange')
        self.isolation = True
        self.isolation_timer = 100
        self.immune = True

    # A method that checks if the agents are close to eachother and infects them.
    def check_infected(self, persons):
        #Here the method checks how close they are to eachother 
        for person in persons: 
            d = ((self.x - person.x)**2 + (self.y - person.y)**2)**(1/2)

        # If its less than 20, then the agent gets infected
            if d < 20 and person.infected == True and self.infected == False and self.immune == False:
                self.infect()
        # If its less than 60, then the agent will get put in the notifikation list
            if d < 60 and person.smittestop and self.smittestop and self != person:
                self.kontakter.append([person,200])
 

    # A method thas makes the infectedtimer count down 
    def agent_infectedtimer(self):
        #Here it checks if the agents infectedtimer has reached 0 and them makes them healthy(green)
        if self.infectedtimer < 1 and self.infected == True:
            self.infected = False
            self.canvas.itemconfig(self.circle_id, fill='green')
            self.immune = True
            
        # If the above if statement is not fulfilled, the infectedtimer is lowered
        else:
            self.infectedtimer -= 1

    def agent_isolationtimer(self):
        if self.isolation_timer < 0 and self.isolation == True:
            self.isolation = False
            self.canvas.itemconfig(self.circle_id, fill='green')
        else:
            self.isolation_timer -= 1

    #A method that checks if a person has been chosen to have smittestop appen
    def agent_smittestop(self):
        if self.smittestop == True and self.infected == False:
            self.canvas.itemconfig(self.circle_id, fill='blue')
            for k in self.kontakter:
                k[1] -= 1
                if k[1] < 0:
                    self.kontakter.remove(k)



    # A method that infect the agents and makes them red, and starts the infected timer.
    def infect(self):
        self.infected = True
        self.canvas.itemconfig(self.circle_id, fill='red')
        self.infectedtimer = 100
        if self.smittestop == True and self.infected == True:
            for k in self.kontakter:
                k[0].notifikation()

       


    
class App(object):
    def __init__(self, master, **kwargs):
     # Create the canvas on which the agents are drawn
        self.master = master
        self.canvas = tk.Canvas(self.master, width=800, height=800,background='white')
        self.canvas.grid(row = 0, columnspan = 3)
        

        # Create a reset button for the simulation
        self.but_reset = ttk.Button(master, text = "Reset", command=self.init_sim)
        self.but_reset.grid(row = 1, column =0)
        

        #Creating 2 buttons to change the amount of agents
        self.amount_agent = ttk.Button(master, text = "Agents +1 ", command=self.agentsup)
        self.amount_agent.grid(row = 1, column = 1)

        self.amount_agent = ttk.Button(master, text = "Agents -1 ", command=self.agentsdown)
        self.amount_agent.grid(row = 1, column = 2)
        
         
        # Start / init the simulation
        self.init_sim()

        self.master.after(0, self.update)
        self.frame = 0


        self.smittede = []
        self.smittede2 = []
        
    # A method to make additional agents on the canvas
    def agentsup(self):
        global n
        n = n+1
        self.init_sim()
    # A method to make less agents on the canvas
    def agentsdown(self):
        global n
        n = n-1
        self.init_sim()

    # A method that updates the agents every frame
    def update(self):
        # Update / move each agent
        for person in self.persons:
            person.move()
            person.check_infected(self.persons)
        

        # Count number of infected persons
        ni = 0
        for p in self.persons:
            if p.infected:
                ni += 1

        print(ni)
        if stopper == 0.4:
            self.smittede2.append(ni)
        else:
            self.smittede.append(ni)
        if self.frame == 400:
            self.master.destroy()
            

        self.master.after(100, self.update)
        self.frame += 1

    # Start / init simulation (clear all agents and create new ones)
    def init_sim(self):
        self.canvas.delete('all')
        self.persons = []

        # Decides where agents starts on the canvas, they start random from the x and y values from 0 to 800.
        for i in range(n):
            x = random.randint(0,800)
            y = random.randint(0,800)
            p = Person(self.canvas, x, y, 'black') # The color of the agents is black when they are not infected

            #Infect 5% of the agents at the start of the simulation
            if i < 5:
                p.infect()

            self.persons.append(p)

        

        
# Create the Tkinter application and run it
root = tk.Tk()
app = App(root)
start=time.time()
root.mainloop()
stopper = 0.4
root = tk.Tk()
app2 = App(root)
start=time.time()
root.mainloop()
end=time.time()
print("Frames:",app.frame)
print("Runtime:",end-start)
print("Framerate:", app.frame/(end-start))
plt.plot(app.smittede)
plt.plot(app2.smittede2)
plt.show()