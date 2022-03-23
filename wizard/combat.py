from operator import countOf
import tkinter as tk
from tkinter import ttk
from random import randint
#project files
from output import table
hit_amount_entry:tk.Entry
hit_type_entry:tk.Entry
damage_amount_entry:tk.Entry
damage_type_entry:tk.Entry
health_reduction_amount_entry:tk.Entry
health_reduction_id_entry:tk.Entry
kill_amount_entry:tk.Entry
kill_type_entry:tk.Entry
bottom_label:tk.Label
cursor = None 
db = None
def hit_roll():
    global hit_amount_entry, hit_type_entry, cursor, db
    type = f'"{hit_type_entry.get()}"'
    amount = hit_amount_entry.get()
    if len(type) > 0:
        cursor.execute(f'select * from summons where creature_type={type};')
    else:
        cursor.execute(f'select * from summons;')
    results = cursor.fetchall()
    if len(results) > 0:
        rolls = [randint(1,20)+int(results[i][3]) for i in range(int(amount))]
        tab_master = tk.Toplevel()
        tab = table([rolls], width=2, title="hit rolls", icon="icon.ico", master=tab_master, scrollable="x")
        tab.pack(side=tk.TOP)
        tk.Label(tab_master, text=f'modifier: {results[0][3]}').pack(side=tk.TOP)
        ttk.Separator(tab_master).pack(side=tk.TOP, fill=tk.X)
        for i in range(1+int(results[0][3]), 21+int(results[0][3])):
            num = countOf(rolls,i)
            if num > 0:
                print(f'{num} roll(s) with value {i}')
                tk.Label(tab_master, text=f'{num} roll(s) with value {i}').pack(side=tk.TOP)
        bottom_label.config(text="succssfully rolled hit rolls", fg="green")
    else:
        bottom_label.config(text=f'no creatures of type {type} found')
def damage_roll():
    global damage_amount_entry, damage_type_entry, cursor
    type = f'"{damage_type_entry.get()}"'
    amount = damage_amount_entry.get()
    if len(type) > 0:
        cursor.execute(f'select * from summons where creature_type={type};')
    else:
        cursor.execute(f'select * from summons;')
    results = cursor.fetchall()
    if len(results) > 0:
        rolls = [randint(1,6)+int(results[i][4]) for i in range(int(amount))]
        tab_master = tk.Toplevel()
        tab = table([rolls], width=2, title="damage rolls", icon="icon.ico", master=tab_master, scrollable="x")
        tab.pack(side=tk.TOP)
        tk.Label(tab_master, text=f'modifier: {results[0][4]}').pack(side=tk.TOP)
        ttk.Separator(tab_master).pack(side=tk.TOP, fill=tk.X)
        for i in range(1+int(results[0][4]), 20+int(results[0][4])):
            num = countOf(rolls,i)
            if num > 0:
                print(f'{num} roll(s) with value {i}')
                tk.Label(tab_master, text=f'{num} roll(s) with value {i}').pack(side=tk.TOP)
        print(f'total: {sum(rolls)} damage')
        tk.Label(tab_master, text=f'total: {sum(rolls)} damage').pack(side=tk.TOP)
        bottom_label.config(text="succssfully rolled damage rolls", fg="green")
    else:
        print(f'no creatures of type {type} found')

def reduce_health():
    global health_reduction_amount_entry,health_reduction_id_entry,cursor,db
    amount = health_reduction_amount_entry.get()
    id = f'{health_reduction_id_entry.get()}'
    try:
        cursor.execute(f'select * from summons where id={id}')
        result = cursor.fetchall()[0]
        print(f'{result[1]} with id {id} has {int(result[2])-int(amount)} hp remaining!')
        if int(result[2])-int(amount)<= 0:
            print(f'{result[1]} with id {id} died!')
            cursor.execute(f'delete from summons where id = {id}')
        else:
            cursor.execute(f'update summons set health={int(result[2])-int(amount)} where id={id}')
            db.commit()
        bottom_label.config(text=f'{result[1]} with id {id} has {int(result[2]) - int(amount)} hp remaining!', fg="red")
    except Exception as e:
        print("failed to execute mysql command")
        print(e)
def kill():
    global kill_type_entry, kill_type_entry
    type = kill_type_entry.get()
    amount = kill_amount_entry.get()
    cursor.execute(f'select * from summons where creature_type="{type}"')
    result = cursor.fetchall()
    if len(result)> 0:
        for i in range(int(amount)):
            cursor.execute(f'delete from summons where id ="{result[i][0]}"')
            print(f'killed {type} with id {result[i][0]}')
            bottom_label.config(text=f'killed {type} with id {result[i][0]}', fg="red")
        db.commit()
    else:
        print(f'no creatures of type {type} found')

def zombie_preset():
    global hit_amount_entry,hit_type_entry,damage_amount_entry,damage_type_entry,cursor
    cursor.execute("select * from summons where creature_type='zombie'")
    result = cursor.fetchall()
    amount = len(result)
    hit_amount_entry.delete(0, len(hit_amount_entry.get()))
    hit_amount_entry.insert(tk.END, amount)
    hit_type_entry.delete(0, len(hit_type_entry.get()))
    hit_type_entry.insert(tk.END, "zombie")
    damage_amount_entry.delete(0,len(damage_amount_entry.get()))
    damage_amount_entry.insert(tk.END, amount)
    damage_type_entry.delete(0,len(damage_type_entry.get()))
    damage_type_entry.insert(tk.END, "zombie")
    bottom_label.config(text="successfully set zombie preset", fg="green")
def skeleton_preset():
    global hit_amount_entry,hit_type_entry,damage_amount_entry,damage_type_entry,cursor
    cursor.execute("select * from summons where creature_type='skeleton'")
    result = cursor.fetchall()
    amount = len(result)
    hit_amount_entry.delete(0, len(hit_amount_entry.get()))
    hit_amount_entry.insert(tk.END,amount)
    hit_type_entry.delete(0, len(hit_type_entry.get()))
    hit_type_entry.insert(tk.END, "skeleton")
    damage_amount_entry.delete(0,len(damage_amount_entry.get()))
    damage_amount_entry.insert(tk.END, amount)
    damage_type_entry.delete(0,len(damage_type_entry.get()))
    damage_type_entry.insert(tk.END, "skeleton")
    bottom_label.config(text="successfully set skeleton preset", fg="green")

def combat(Cursor, Db):
    global bottom_label, kill_type_entry, kill_amount_entry, health_reduction_amount_entry, health_reduction_id_entry, hit_amount_entry, hit_type_entry, damage_amount_entry, damage_type_entry, cursor, db
    ##make some window with functions to make combat easier
    cursor = Cursor
    db = Db
    window = tk.Toplevel()

    bottom_label = tk.Label(window, text="Combat textbox")
    bottom_label.pack(side=tk.BOTTOM)
    
    bottom_panel = tk.Frame(window)
    bottom_panel.pack(side=tk.BOTTOM)

    hit_roll_panel = tk.LabelFrame(bottom_panel, text="Hit roll")
    hit_roll_panel.pack(side=tk.LEFT)

    hit_amount_panel = tk.Frame(hit_roll_panel)
    hit_amount_panel.pack(side=tk.TOP)
    hit_amount_text = tk.Label(hit_amount_panel, text="Amount")
    hit_amount_text.pack(side=tk.TOP)
    hit_amount_entry = tk.Entry(hit_amount_panel)
    hit_amount_entry.pack(side=tk.TOP)
    hit_amount_entry.insert(tk.END,1)

    hit_type_panel = tk.Frame(hit_roll_panel)
    hit_type_panel.pack(side=tk.TOP)
    hit_type_text = tk.Label(hit_type_panel, text="Type")
    hit_type_text.pack(side=tk.TOP)
    hit_type_entry = tk.Entry(hit_type_panel)
    hit_type_entry.pack(side=tk.TOP)
    hit_type_entry.insert(tk.END,"zombie")

    hit_roll_button = tk.Button(hit_roll_panel, text="Roll hit roll", width=20,command=hit_roll)
    hit_roll_button.pack(side=tk.BOTTOM)
    
    damage_roll_panel = tk.LabelFrame(bottom_panel,text="Damage roll")
    damage_roll_panel.pack(side=tk.LEFT)

    damage_amount_panel = tk.Frame(damage_roll_panel)
    damage_amount_panel.pack(side=tk.TOP)
    damage_text = tk.Label(damage_amount_panel,text="Amount")
    damage_text.pack(side=tk.TOP)
    damage_amount_entry = tk.Entry(damage_amount_panel)
    damage_amount_entry.pack(side=tk.TOP)
    damage_amount_entry.insert(tk.END,1)

    damage_type_panel = tk.Frame(damage_roll_panel)
    damage_type_panel.pack(side=tk.TOP)
    damage_type_text = tk.Label(damage_type_panel, text="Type")
    damage_type_text.pack(side=tk.TOP)
    damage_type_entry = tk.Entry(damage_type_panel)
    damage_type_entry.pack(side=tk.TOP)
    damage_type_entry.insert(tk.END,"zombie")

    damage_roll_button = tk.Button(damage_roll_panel, text="Roll damage roll", width=20,command=damage_roll)
    damage_roll_button.pack(side=tk.BOTTOM)

    ##health reduction
    health_reduction_panel = tk.LabelFrame(bottom_panel,text="Health reduction")
    health_reduction_panel.pack(side=tk.LEFT)

    health_reduction_amount_panel = tk.Frame(health_reduction_panel)
    health_reduction_amount_panel.pack(side=tk.TOP)
    health_reduction_text = tk.Label(health_reduction_amount_panel,text="Amount")
    health_reduction_text.pack(side=tk.TOP)
    health_reduction_amount_entry = tk.Entry(health_reduction_amount_panel)
    health_reduction_amount_entry.pack(side=tk.TOP)
    health_reduction_amount_entry.insert(tk.END,1)

    health_reduction_type_panel = tk.Frame(health_reduction_panel)
    health_reduction_type_panel.pack(side=tk.TOP)
    health_reduction_type_text = tk.Label(health_reduction_type_panel, text="Id")
    health_reduction_type_text.pack(side=tk.TOP)
    health_reduction_id_entry = tk.Entry(health_reduction_type_panel)
    health_reduction_id_entry.pack(side=tk.TOP)
    health_reduction_id_entry.insert(tk.END,1)

    health_reduction_button = tk.Button(health_reduction_panel, text="Reduce health of creature", width=20,command=reduce_health)
    health_reduction_button.pack(side=tk.BOTTOM)

    ##kill
    kill_panel = tk.LabelFrame(bottom_panel,text="Kill creature(s)")
    kill_panel.pack(side=tk.LEFT)

    kill_amount_panel = tk.Frame(kill_panel)
    kill_amount_panel.pack(side=tk.TOP)
    kill_text = tk.Label(kill_amount_panel,text="Amount")
    kill_text.pack(side=tk.TOP)
    kill_amount_entry = tk.Entry(kill_amount_panel)
    kill_amount_entry.pack(side=tk.TOP)
    kill_amount_entry.insert(tk.END,1)

    kill_type_panel = tk.Frame(kill_panel)
    kill_type_panel.pack(side=tk.TOP)
    kill_type_text = tk.Label(kill_type_panel, text="Type")
    kill_type_text.pack(side=tk.TOP)
    kill_type_entry = tk.Entry(kill_type_panel)
    kill_type_entry.pack(side=tk.TOP)
    kill_type_entry.insert(tk.END,"zombie")
    

    kill_button = tk.Button(kill_panel, text="Kill creature(s)", width=20,command=kill)
    kill_button.pack(side=tk.BOTTOM)
    
    top_panel = tk.LabelFrame(window, text="Controls")
    top_panel.pack(side=tk.TOP)
    exit_button = tk.Button(top_panel,text="Exit", fg="red",command=window.destroy)
    exit_button.pack(side=tk.LEFT)
    zombie_button = tk.Button(top_panel,text="Zombie preset", command=zombie_preset)
    zombie_button.pack(side=tk.LEFT)
    skeleton_button = tk.Button(top_panel,text="Skeleton preset", command=skeleton_preset)
    skeleton_button.pack(side=tk.LEFT)

    try:
        window.iconbitmap("icon.ico")
    except:
        print("probably running in linux")
    
    window.resizable(False,False)
    window.title("Combat Window")