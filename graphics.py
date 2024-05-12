import tkinter as tk
from tkinter import ttk
from random import choice
from vectors import Scalar, Vector, VectorOperations

root = tk.Tk()
root.geometry('940x600')
root.config(bg='#fff')
root.wm_resizable(False, False)

canvas = tk.Canvas(root, height=600, width=600, bg="#fff")

colors = ["green","red","blue","orange"]

elements = {}

vo = VectorOperations()

def draw_piano_cartesiano():
    for y in range(0,600,18):
        canvas.create_line(0,y,600,y, fill="grey" if y!=270 else "black", width=1)
    for x in range(0,600,18):
        canvas.create_line(x,0,x,600, fill="grey" if x!=270 else "black", width=1)

def fix_coord(components: list|tuple|set):
    x=18*(components[0]+15)
    y=18*(-1*components[1]+15)
    return x, y

def put_point(components: list|tuple|set, id: str, fill="black"):
    canvas.create_oval(components[0]-3, components[1]-3, components[0]+3, components[1]+3,fill=fill)
    #canvas.create_oval(18*components[0]-3, 18*components[1]-3, 18*components[0]+3, 18*components[1]+3,fill="red")
    # canvas.create_text(components[0]-3, components[1]+3, text=id, font=("Comfortaa",11))

def represent_vector(vector):
    #if "cross" in vector:
        elements[vector.id]=vector
        graph_cmpnts = fix_coord(vector.start)
        canvas.create_line(graph_cmpnts[0], graph_cmpnts[1], graph_cmpnts[0]+vector.x*18, graph_cmpnts[1]+vector.y*-18, fill=choice(colors), width=2)
        canvas.create_text((graph_cmpnts[0]+graph_cmpnts[0]+vector.x*18)/2, (graph_cmpnts[1]+graph_cmpnts[1]+vector.y*-18)/2, text=vector.id, font=("Comfortaa",11))
    # else:
    #     pass

def represent_magnitude(cross):
    elements[cross[2]]=("cross", cross[3]) #from id represent inspect
    vectors = cross[0]
    sx=(vectors[0].start[0]+vectors[1].start[0])/2
    sy=(vectors[0].start[1]+vectors[1].start[1])/2
    p1=fix_coord((sx, sy))#bottom left
    p2=fix_coord((sx+vectors[0].x, sy+vectors[0].y))#upper left
    p3=fix_coord(((sx+vectors[0].x)+vectors[1].x,(sy+vectors[0].y)+vectors[1].y))#upper right
    p4=fix_coord((sx+vectors[1].x, sy+vectors[1].y))#bottom right

    canvas.create_polygon(p1,p2,p3,p4,fill=choice(colors), width=1,stipple="gray50")
    canvas.create_text((p1[0]+p3[0])/2, (p1[1]+p3[1])/2, text=cross[2]+"\n~"+str(cross[1])[:str(cross[1]).find(".")+3])

draw_piano_cartesiano()


console_frame = tk.LabelFrame(root, text="Console", bg="#F7F8F3", width=400, height=600)

tabControl = ttk.Notebook(console_frame)
inspector_tab = ttk.Frame(tabControl)
operations_tab = ttk.Frame(tabControl)
tabControl.add(inspector_tab, text="Inspector")
tabControl.add(operations_tab, text="Operations")

input_field_insp = tk.Entry(inspector_tab, width=46, borderwidth=2)
input_field_insp.pack()
btn=tk.Button(inspector_tab, width=39, text="inspect", command=lambda: inspect(None, input_field_insp.get().split(" ")), bg="#F7444E")
btn.pack()
output_field = tk.Text(inspector_tab, width=40, height=80, state="disabled", font=("lucida sans typewriter", 10), fg="black", wrap="word")#"Bradley Hand ITC"
output_field.pack(pady=20, expand=True)

def inspect(event, ids = None):
    if not ids:
        ids = input_field_insp.get().split(" ")
    output_field.config(state="normal")
    output_field.delete("1.0", tk.END)
    for id in ids:
        output_field.insert(tk.END, elements[id].inspect() if type(elements[id])!=tuple else elements[id][1])
    output_field.config(state="disabled")

input_field_ops = tk.Entry(operations_tab, width=46, borderwidth=2)
input_field_ops.pack()
btn1=tk.Button(operations_tab, width=39, text="execute", command=lambda: execute(None, input_field_ops.get()), bg="#F7444E")
btn1.pack()

def execute(event, operation=None):
    if not operation:
        operation = input_field_ops.get()
    id = operation[operation.find(" ")+1:]
    operation=operation[:operation.find(" ")]
    if "+" in operation:
        vectors_id=operation.split("+")
        vectors = [elements[vectors_id[0]],elements[vectors_id[1]]]
        vector_sum = vo.sum(vectors)
        vector_sum.id = id
        represent_vector(vector_sum)
    elif "-" in operation:
        vectors_id=operation.split("-")
        vectors = [elements[vectors_id[0]],elements[vectors_id[1]]]
        vector_sub = vo.subtraction(vectors)
        vector_sub.id = id
        represent_vector(vector_sub)
    elif "x" in operation:
        vectors_id=operation.split("x")
        vectors = [elements[vectors_id[0]],elements[vectors_id[1]]]
        cross_prod = vo.cross_product(vectors, id=id)
        represent_magnitude(cross_prod)
    elif "*" in operation:
        vector_id=operation.split("*")[0]
        scalar = float(operation.split("*")[1])
        prod = vo.product(elements[vector_id], Scalar(scalar, None))
        prod.id = id
        represent_vector(prod)
    elif "/" in operation:
        vector_id=operation.split("/")[0]
        scalar = int(operation.split("/")[1])
        div = vo.division(elements[vector_id], Scalar(scalar, None))
        div.id = id
        represent_vector(div)


new_vector_frame = tk.LabelFrame(operations_tab, text="New Vector", width=400, height=600, bg="white")

id_field = tk.Entry(new_vector_frame, width=46)
id_field.insert(0, "id")
id_field.pack()
mag_field = tk.Entry(new_vector_frame, width=46)
mag_field.insert(0, "magnitude (float)")
mag_field.pack()
mu_field = tk.Entry(new_vector_frame, width=46)
mu_field.insert(0, "measurement unit (float)")
mu_field.pack()
angle_field = tk.Entry(new_vector_frame, width=46)
angle_field.insert(0, "direction angle (degrees)")
angle_field.pack()
start_field = tk.Entry(new_vector_frame, width=46)
start_field.insert(0, "origin (x, y)")
start_field.pack()

fields = {id_field: "id", mag_field: "magnitude (float)", mu_field: "measurement unit (float)", angle_field: "direction angle (degrees)", start_field: "origin (x, y)"}

btn2=tk.Button(new_vector_frame, width=39, text="create", command=lambda: create(id_field.get(), mag_field.get(), angle_field.get(), mu_field.get(), start_field.get()), bg="#F7444E")
btn2.pack()


def create(id, mag, angle, mu, start):
    origin = (float(start.split(",")[0]),float(start.split(",")[1]))
    nv = Vector(float(mag), float(angle), origin, mu, id)
    represent_vector(nv)
    for field in fields.keys():
        field.delete(0, tk.END)
        field.insert(0, fields[field])

new_vector_frame.pack()

def clear_entry(event, entry):
    entry.delete(0, tk.END)

input_field_ops.bind('<Return>', execute)
input_field_insp.bind('<Return>', inspect)
input_field_insp.bind('<Button-1>', lambda event: clear_entry(event, input_field_insp))
id_field.bind('<Button-1>', lambda event: clear_entry(event, id_field))
mag_field.bind('<Button-1>', lambda event: clear_entry(event, mag_field))
mu_field.bind('<Button-1>', lambda event: clear_entry(event, mu_field))
angle_field.bind('<Button-1>', lambda event: clear_entry(event, angle_field))
start_field.bind('<Button-1>', lambda event: clear_entry(event, start_field))

def show():
    #tk.Label(root, text="Vector representations", bg="white", font=("Comfortaa",11)).pack()
    canvas.pack(side=tk.LEFT)
    console_frame.pack(side=tk.RIGHT, fill=tk.Y)
    #inspector.pack()
    tabControl.pack(expand=1, fill="both")
    root.mainloop()
