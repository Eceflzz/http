import tkinter as tk 

def place_order(food_entry,drink_entry,result_label):
    #take the information
    food = food_entry.get()
    drink= drink_entry.get()
    #reflect information on label
    result_label.config(text=f"choosen food: {food}\nchoosen drink: {drink}")

#make tkinter window
window = tk.Tk()
window.title("NOSTALGIA RESTAURANT")
window.geometry("450x350")

#message for customers
write = tk.Label(window, text="Welcome to Nostalgia Restaurant",fg="black",font= ("times new roman" , 20) )
write.place(x=65,y=7)
#starting to form
#entry field for drink and food information

food_label = tk.Label(window, text="FOOD:",fg="black",font=("times new roman",13))
food_label.place(x=20,y=45)


food_entry = tk.Entry(window)
food_entry.place(x=80,y=50)

#drink informaitons
drink_label = tk.Label(window, text="DRINK:",fg="black",font=("times new roman",13))
drink_label.place(x=20,y=85)

drink_entry = tk.Entry(window)
drink_entry.place(x=85,y=90)

#for order result
result_label = tk.Label(window , text="your results will be show here", fg="red", font=("times new roman",15))
result_label.place(x=20,y=150)

#order comfirmation
submit_button = tk.Button(
    window,
    text="confirm order",
    command=lambda: place_order(food_entry , drink_entry , result_label)
)
submit_button.place(x=20,y=120)

#start main loop
window.mainloop()
