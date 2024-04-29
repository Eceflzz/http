import random

def draw(gamers):
 
 winner = random.choice(gamers)
 return winner


if __name__ == "__main__":
 gamers = ["ahmet", "kübra" , "ali" , "ayşe"]

 winner = draw(gamers)

 print("winner:", winner)