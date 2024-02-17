import tkinter as tk 

def for_weather(city):
    entered_city = city.get()
    entered_city.config(text=f"entered_city: (iSTANBUL)")

window = tk.Tk()
window.title("7 DAYS WEATHER FORECAST")
window.geometry("450x350")

write = tk.Label(text="•DATE\t•CITY\t•DEGREE", fg="black", font="verdana 13 bold ")
write.place(x=20,y=53)

write_2nd = tk.Label(text="*18.02.2024\t*İSTANBUL\t*9°C\t\t*CLOUDY*")
write_2nd.place(x=20,y=93)

write_2nd = tk.Label(text="*19.02.2024\t*İSTANBUL\t*10°C\t\t*CLOUDY*")
write_2nd.place(x=20,y=123)

write_2nd = tk.Label(text="*20.02.2024\t*İSTANBUL\t*11°C\t\t*SUNNY*")
write_2nd.place(x=20,y=153)

write_2nd = tk.Label(text="*21.02.2024\t*İSTANBUL\t*11°C\t\t*CLOUDY*")
write_2nd.place(x=20,y=183)

write_2nd = tk.Label(text="*22.02.2024\t*İSTANBUL\t*12°C\t\t*PARTLY CLOUDY*")
write_2nd.place(x=20,y=213)

write_2nd = tk.Label(text="*23.02.2024\t*İSTANBUL\t*14°C\t\t*SUNNY*")
write_2nd.place(x=20,y=243)

write_2nd = tk.Label(text="*24.02.2024\t*İSTANBUL\t*16°C\t\t*SUNNY*")
write_2nd.place(x=20,y=273)

write_2nd = tk.Label(text="*25.02.2024\t*İSTANBUL\t*17°C\t\t*CLOUDY*")
write_2nd.place(x=20,y=303)

tag = tk.Label(text="•weather forecast•", bg="navy blue" ,fg="light blue" ,font="verdana 24 bold")
tag.place(x=47,y=5)


window.mainloop()