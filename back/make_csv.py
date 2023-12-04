names = ["Имя", "Seva", "Max", "Serega"]
stacks = ["Специализация", "Backend", 'Mobile', "Web"]
hours_of_work = ["Количество часов", 40, 50, 45]


with open("example.csv", 'w') as file:
    for n, s, h in zip(names, stacks, hours_of_work):
        file.write(f"{n},{s},{h}\n")
