from abc import ABC, abstractmethod
from datetime import datetime
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt


GRAPH_TYPES = ["plot", "scatter", "bar", "histogram", "pie"]

MAX_CELL_NUMBER = 5

COLORS = [
    "red", "blue", "green", "yellow", "black", "white", "purple",
    "orange", "pink", "brown", "gray", "cyan", "magenta", "lime",
    "navy", "gold", "teal", "violet", "indigo", "olive",
]

MARKERS = [
    " ", ".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4",
    "s", "p", "*", "h", "H", "+", "x", "X", "D", "d", "|", "_",
]


# Function to convert string input to list of floats or strings
def get_list(string_var: tk.StringVar) -> list[float | str]:
    user_input = string_var.get()
    if not user_input:
        return []
    items = user_input.split(",")
    processed_items = []
    for item in items:
        item = item.strip()
        if not item:
            continue
        try:
            processed_items.append(float(item))
        except ValueError:
            processed_items.append(item)
    return processed_items


# Classes for different graph types -----------------------------------
# Base class for all cells
class Cell(ABC):
    def __init__(self, frame):
        self.frame = frame
        self.id = id(self)

        self.label = tk.StringVar()

        self.label_entry_frame = tk.LabelFrame(
            self.frame,
            text="Label",
            bd=1,
            relief="solid",
        )
        self.label_entry_frame.grid(row=0, column=0, padx=5, pady=5)
        self.label_entry = tk.Entry(
            self.label_entry_frame,
            textvariable=self.label,
        )
        self.label_entry.pack(padx=5, pady=5)

        self.remove_button = tk.Button(
            self.frame,
            text="rm",
            command=lambda: cell_manager.delete_cell(self.id),
        )
        self.remove_button.grid(row=0, column=1, padx=5, pady=5)

    @abstractmethod
    def build(self):
        pass


# Base class for 2D cells
class TwoDimensionalCell(Cell):
    def __init__(self, frame):
        super().__init__(frame)

        self.x = tk.StringVar()
        self.x_entry_frame = tk.LabelFrame(
            self.frame,
            text="x",
            bd=1,
            relief="solid",
        )
        self.x_entry_frame.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.x_entry = tk.Entry(
            self.x_entry_frame,
            textvariable=self.x,
        )
        self.x_entry.pack(padx=5, pady=5, fill="x")

        self.y = tk.StringVar()
        self.y_entry_frame = tk.LabelFrame(
            self.frame,
            text="y",
            bd=1,
            relief="solid",
        )
        self.y_entry_frame.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.y_entry = tk.Entry(
            self.y_entry_frame,
            textvariable=self.y,
        )
        self.y_entry.pack(padx=5, pady=5, fill="x")

        self.color = tk.StringVar(value=COLORS[0])
        self.color_combobox_frame = tk.LabelFrame(
            self.frame,
            text="Color",
            bd=1,
            relief="solid",
        )
        self.color_combobox_frame.grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.color_combobox = ttk.Combobox(
            self.color_combobox_frame,
            textvariable=self.color,
            values=COLORS,
            state="readonly",
        )
        self.color_combobox.pack(padx=5, pady=5, fill="x")


class PlotCell(TwoDimensionalCell):
    def __init__(self, frame):
        super().__init__(frame)

        self.linewidth = tk.StringVar(value="1.5")
        self.linewidth_spinbox_frame = tk.LabelFrame(
            self.frame,
            text="Line width",
            bd=1,
            relief="solid",
        )
        self.linewidth_spinbox_frame.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.linewidth_spinbox = ttk.Spinbox(
            self.linewidth_spinbox_frame,
            from_=0,
            to=30,
            textvariable=self.linewidth,
            increment=0.5,
            format="%.1f",
        )
        self.linewidth_spinbox.pack(padx=5, pady=5, fill="x")

        self.linestyles = ["solid", "dashed", "dashdot", "dotted", "None"]
        self.linestyle = tk.StringVar(value=self.linestyles[0])
        self.linestyle_combobox_frame = tk.LabelFrame(
            self.frame,
            text="Line style",
            bd=1,
            relief="solid",
        )
        self.linestyle_combobox_frame.grid(
            row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.linestyle_combobox = ttk.Combobox(
            self.linestyle_combobox_frame,
            textvariable=self.linestyle,
            values=self.linestyles,
            state="readonly",
        )
        self.linestyle_combobox.pack(padx=5, pady=5, fill="x")

        self.marker = tk.StringVar(value=MARKERS[0])
        self.marker_combobox_frame = tk.LabelFrame(
            self.frame,
            text="Marker",
            bd=1,
            relief="solid",
        )
        self.marker_combobox_frame.grid(
            row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.marker_combobox = ttk.Combobox(
            self.marker_combobox_frame,
            textvariable=self.marker,
            values=MARKERS,
            state="readonly",
        )
        self.marker_combobox.pack(padx=5, pady=5, fill="x")

    def build(self):
        x = get_list(self.x)
        y = get_list(self.y)

        if not x:
            plt.plot(
                y,
                color=self.color.get(),
                label=self.label.get(),
                linewidth=self.linewidth.get(),
                linestyle=self.linestyle.get(),
                marker=self.marker.get(),
            )
        else:
            plt.plot(
                x,
                y,
                color=self.color.get(),
                label=self.label.get(),
                linewidth=self.linewidth.get(),
                linestyle=self.linestyle.get(),
                marker=self.marker.get(),
                markersize=float(self.linewidth.get()) + 4.5,
            )


class ScatterCell(TwoDimensionalCell):
    def __init__(self, frame):
        super().__init__(frame)

        self.marker = tk.StringVar(value=MARKERS[1])
        self.marker_combobox_frame = tk.LabelFrame(
            self.frame,
            text="Marker",
            bd=1,
            relief="solid",
        )
        self.marker_combobox_frame.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.marker_combobox = ttk.Combobox(
            self.marker_combobox_frame,
            textvariable=self.marker,
            values=MARKERS,
            state="readonly",
        )
        self.marker_combobox.pack(padx=5, pady=5, fill="x")

        self.markersize = tk.StringVar(value="6.0")
        self.markersize_spinbox_frame = tk.LabelFrame(
            self.frame,
            text="Marker size",
            bd=1,
            relief="solid",
        )
        self.markersize_spinbox_frame.grid(
            row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.markersize_spinbox = ttk.Spinbox(
            self.markersize_spinbox_frame,
            from_=0,
            to=30,
            textvariable=self.markersize,
            increment=0.5,
            format="%.1f",
        )
        self.markersize_spinbox.pack(padx=5, pady=5, fill="x")

    def build(self):
        x = get_list(self.x)
        y = get_list(self.y)

        plt.scatter(
            x,
            y,
            color=self.color.get(),
            label=self.label.get(),
            marker=self.marker.get(),
            s=float(self.markersize.get()) ** 2,
        )


class BarCell(TwoDimensionalCell):
    def build(self):
        x = get_list(self.x)
        y = get_list(self.y)

        plt.bar(x, y, color=self.color.get(), label=self.label.get())


class HistogramCell(Cell):
    def __init__(self, frame):
        super().__init__(frame)

        self.data = tk.StringVar()
        self.data_entry_frame = tk.LabelFrame(
            self.frame,
            text="Data",
            bd=1,
            relief="solid",
        )
        self.data_entry_frame.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.data_entry = tk.Entry(
            self.data_entry_frame,
            textvariable=self.data,
        )
        self.data_entry.pack(padx=5, pady=5, fill="x")

        self.bins = tk.StringVar()
        self.bins_entry_frame = tk.LabelFrame(
            self.frame,
            text="Bins",
            bd=1,
            relief="solid",
        )
        self.bins_entry_frame.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.bins_entry = tk.Entry(
            self.bins_entry_frame,
            textvariable=self.bins,
        )
        self.bins_entry.pack(padx=5, pady=5, fill="x")

        self.color = tk.StringVar(value=COLORS[0])
        self.color_combobox_frame = tk.LabelFrame(
            self.frame,
            text="Color",
            bd=1,
            relief="solid",
        )
        self.color_combobox_frame.grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.color_combobox = ttk.Combobox(
            self.color_combobox_frame,
            textvariable=self.color,
            values=COLORS,
            state="readonly",
        )
        self.color_combobox.pack(padx=5, pady=5, fill="x")

    def build(self):
        data = get_list(self.data)
        bins_str = self.bins.get()
        if not bins_str:
            plt.hist(data, color=self.color.get(), label=self.label.get())
        else:
            plt.hist(
                data,
                bins=int(bins_str),
                color=self.color.get(),
                label=self.label.get(),
            )


class PieCell(Cell):
    def __init__(self, frame):
        super().__init__(frame)

        self.label_entry_frame.config(text="Labels")

        self.data = tk.StringVar()
        self.data_entry_frame = tk.LabelFrame(
            self.frame,
            text="Data",
            bd=1,
            relief="solid",
        )
        self.data_entry_frame.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.data_entry = tk.Entry(
            self.data_entry_frame,
            textvariable=self.data,
        )
        self.data_entry.pack(padx=5, pady=5, fill="x")

    def build(self):
        data = get_list(self.data)
        labels = get_list(self.label)
        if not labels:
            plt.pie(data)
        else:
            plt.pie(data, labels=labels)


# Class to manipulate cells ---------------------------------------------
# This class is responsible for creating, deleting and showing cells
class CellManager:
    def __init__(self):
        # Cell list, where key is cell id and value is Cell object
        self.cells: dict[int, Cell] = {}

    def create_cell(self, graph_type):
        if len(self.cells) == MAX_CELL_NUMBER:
            add_status_text("Max number of cells reached!")
            return

        if (
            graph_option_menu["menu"].entrycget(
                GRAPH_TYPES.index(graph_type), "state"
            )
            == "disabled"
        ):
            return

        frame = tk.LabelFrame(
            cells_list,
            text=graph_type,
            bd=1,
            relief="solid",
        )
        frame.pack(side="left", anchor="n", padx=10, pady=10)

        def disable_pie():
            if not self.cells:
                menu = graph_option_menu["menu"]
                menu.entryconfig(GRAPH_TYPES.index("pie"), state="disabled")

        match graph_type:
            case "plot":
                cell = PlotCell(frame)
                disable_pie()
            case "scatter":
                cell = ScatterCell(frame)
                disable_pie()
            case "bar":
                cell = BarCell(frame)
                disable_pie()
            case "histogram":
                cell = HistogramCell(frame)
                disable_pie()
            case "pie":
                cell = PieCell(frame)
                menu = graph_option_menu["menu"]
                for i in range(menu.index("end") + 1):
                    menu.entryconfig(i, state="disabled")

        self.cells[cell.id] = cell

    def delete_cell(self, cell_id):
        self.cells[cell_id].frame.destroy()
        del self.cells[cell_id]

        if not self.cells:
            menu = graph_option_menu["menu"]
            for i in range(menu.index("end") + 1):
                menu.entryconfig(i, state="normal")

    def show(self):
        if not self.cells:
            add_status_text("No cells to plot!")
            return

        # Make all frames white
        for cell in self.cells.values():
            cell.frame.config(bg=cells_list.cget("bg"))

        plt.figure()
        for cell in self.cells.values():
            try:
                cell.build()
            except Exception as e:
                add_status_text(f"Error in red cell {cell.id}: {e}")
                cell.frame.config(bg="#FFCCCC")
                plt.close()
                return

        add_status_text("Successfully plotted!")

        if title_var.get():
            plt.title(title_var.get())
        if xlabel_var.get():
            plt.xlabel(xlabel_var.get())
        if ylabel_var.get():
            plt.ylabel(ylabel_var.get())
        if legend_var.get():
            plt.legend()
        if grid_var.get():
            plt.grid()

        plt.show()


# GUI ---------------------------------------------------------------------
root = tk.Tk()
root.title("Plotting App")
root.geometry("530x550")

# Navigation --------------------------------------------------------------
navigation = tk.LabelFrame(
    root,
    text="Choose graph type",
    bd=1,
    relief="solid",
)
navigation.pack(
    anchor="w",
    padx=10,
    pady=5,
    fill="x",
)

graph_type = tk.StringVar(value=GRAPH_TYPES[0])
graph_option_menu = tk.OptionMenu(
    navigation,
    graph_type,
    *GRAPH_TYPES,
)
graph_option_menu.config(width=10)
graph_option_menu.pack(side="left", padx=10, pady=5)

create_cell = tk.Button(
    navigation,
    text="Create cell",
    command=lambda: cell_manager.create_cell(graph_type.get()),
)
create_cell.pack(side="left", padx=10, pady=5)

number_label = tk.Label(
    navigation,
    text=f"Max number of cells: {MAX_CELL_NUMBER}",
)
number_label.pack(side="right", padx=10, pady=5)

# Cell List ---------------------------------------------------------------
main_frame = tk.Frame(root, relief="solid")
main_frame.pack(pady=5, fill="both", expand=True)

canvas_frame = tk.Frame(main_frame)
canvas_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(canvas_frame)
canvas.pack(side="left", fill="both", expand=True)

y_scrollbar = tk.Scrollbar(
    canvas_frame, orient="vertical", command=canvas.yview
)
y_scrollbar.pack(side="right", fill="y")

x_scrollbar = tk.Scrollbar(
    main_frame, orient="horizontal", command=canvas.xview
)
x_scrollbar.pack(fill="x")

canvas.configure(
    xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set
)

cells_list = tk.Frame(canvas, relief="solid")
canvas.create_window((0, 0), window=cells_list, anchor="nw")


def update_scrollregion(event):
    canvas.config(scrollregion=canvas.bbox("all"))


cells_list.bind("<Configure>", update_scrollregion)


def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def _on_linux_scroll(event):
    if event.num == 4:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        canvas.yview_scroll(1, "units")


canvas.bind("<MouseWheel>", _on_mousewheel)
canvas.bind("<Button-4>", _on_linux_scroll)
canvas.bind("<Button-5>", _on_linux_scroll)

cell_manager = CellManager()

# Plotting ----------------------------------------------------------------
plotting = tk.LabelFrame(
    root,
    text="Plotting",
    bd=1,
    relief="solid",
)
plotting.pack(
    anchor="w",
    padx=10,
    pady=5,
    fill="x",
)

title_var = tk.StringVar()
title_frame = tk.LabelFrame(
    plotting,
    text="Title",
    bd=1,
    relief="solid",
    width=100,
    height=45,
)
title_frame.pack(side="left", padx=5, pady=5)
title_frame.pack_propagate(False)
title_entry = tk.Entry(
    title_frame,
    textvariable=title_var,
)
title_entry.pack(padx=5, pady=5, fill="x")

xlabel_var = tk.StringVar()
xlabel_frame = tk.LabelFrame(
    plotting,
    text="Xlabel",
    bd=1,
    relief="solid",
    width=100,
    height=45,
)
xlabel_frame.pack(side="left", padx=5, pady=5)
xlabel_frame.pack_propagate(False)
xlabel_entry = tk.Entry(
    xlabel_frame,
    textvariable=xlabel_var,
)
xlabel_entry.pack(padx=5, pady=5, fill="x")

ylabel_var = tk.StringVar()
ylabel_frame = tk.LabelFrame(
    plotting,
    text="Ylabel",
    bd=1,
    relief="solid",
    width=100,
    height=45,
)
ylabel_frame.pack(side="left", padx=5, pady=5)
ylabel_frame.pack_propagate(False)
ylabel_entry = tk.Entry(
    ylabel_frame,
    textvariable=ylabel_var,
)
ylabel_entry.pack(padx=5, pady=5, fill="x")

legend_grid_frame = tk.Frame(plotting)
legend_grid_frame.pack(side="left", padx=5, pady=5)

legend_var = tk.BooleanVar(value=False)
legend_checkbutton = tk.Checkbutton(
    legend_grid_frame,
    text="Show legend",
    variable=legend_var,
)
legend_checkbutton.pack(anchor="w")

grid_var = tk.BooleanVar(value=False)
grid_checkbutton = tk.Checkbutton(
    legend_grid_frame,
    text="Show grid",
    variable=grid_var,
)
grid_checkbutton.pack(anchor="w")

plot_button = tk.Button(
    plotting,
    text="Plot",
    command=cell_manager.show,
    bg="orange",
    width=10,
    height=2,
)
plot_button.pack(side="left", padx=10, pady=5)

# Status Bar --------------------------------------------------------------
status_frame = tk.LabelFrame(
    root,
    text="Status",
    bd=1,
    relief="solid",
)
status_frame.pack(padx=10, pady=5, fill="x")

scrollbar = tk.Scrollbar(status_frame)
scrollbar.pack(side="right", fill="y")

status_text = tk.Text(
    status_frame,
    wrap="word",
    height=4,
    width=50,
    bg="white",
    yscrollcommand=scrollbar.set,
    state="disabled",
)
status_text.pack(padx=10, pady=5, fill="x")

scrollbar.config(command=status_text.yview)


# Function to add text to the status bar
def add_status_text(text: str):
    current_time = datetime.now().strftime("[%H:%M:%S]")
    status_text.config(state="normal")
    status_text.insert(tk.END, f"{current_time} {text}\n")
    status_text.config(state="disabled")
    status_text.yview(tk.END)


add_status_text("Welcome to the plotting app!")

if __name__ == "__main__":
    root.mainloop()
