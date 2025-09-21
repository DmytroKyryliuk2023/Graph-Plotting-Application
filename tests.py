import tkinter as tk
import unittest

import course as crs


# Блокування спливаючих вікон графіків
crs.plt.show = lambda *args, **kwargs: None


# Глобальна функція для перевірки вмісту статусного вікна
def ends_with(text: str) -> bool:
    content = crs.status_text.get("1.0", tk.END).strip()
    return content.endswith(text)


# Тести для функцій
class TestFunctions(unittest.TestCase):
    def test_get_list(self):
        self.assertEqual(crs.get_list(tk.StringVar(value="")), [])
        self.assertEqual(
            crs.get_list(tk.StringVar(value="1, 2, 3")), [1, 2, 3]
        )
        self.assertEqual(
            crs.get_list(tk.StringVar(value="1, 2, 3, ")), [1, 2, 3]
        )
        self.assertEqual(
            crs.get_list(tk.StringVar(value="1.5, 2.5, 3.5")), [1.5, 2.5, 3.5]
        )
        self.assertEqual(
            crs.get_list(tk.StringVar(value="1.5, 2.5, 3.5, ")),
            [1.5, 2.5, 3.5],
        )
        self.assertEqual(
            crs.get_list(tk.StringVar(value="A, B, C")), ["A", "B", "C"]
        )
        self.assertEqual(
            crs.get_list(tk.StringVar(value="A, B, C, ")), ["A", "B", "C"]
        )

    def test_add_status_text(self):
        text = "Hello"
        crs.add_status_text(text)
        self.assertTrue(ends_with(text))


# Тести створення та видалення графіків
class TestCellsManipulation(unittest.TestCase):
    def test_create_cell(self):
        menu = crs.graph_option_menu["menu"]
        for graph_type in crs.GRAPH_TYPES:
            crs.cell_manager.create_cell(graph_type)
            # Перевірка, що графік створено
            self.assertTrue(len(crs.cell_manager.cells) == 1)
            # Перевірка правильного блокування меню
            if graph_type == "pie":
                for i in range(menu.index("end") + 1):
                    self.assertTrue(menu.entrycget(i, "state") == "disabled")
            else:
                index = crs.GRAPH_TYPES.index("pie")
                self.assertTrue(menu.entrycget(index, "state") == "disabled")

            # Очищення графіків і скидання меню
            for i in range(menu.index("end") + 1):
                menu.entryconfig(i, state="normal")
            crs.cell_manager.cells.clear()

    def test_delete_cell(self):
        menu = crs.graph_option_menu["menu"]
        # Імітація створення графіка
        id = 0
        crs.cell_manager.cells[id] = crs.PlotCell(tk.LabelFrame())
        menu.entryconfig(id + 1, state="disabled")

        crs.cell_manager.delete_cell(id)

        # Перевірка, що графік видалено
        self.assertTrue(not crs.cell_manager.cells)
        self.assertTrue(menu.entrycget(id + 1, "state") == "normal")

        # Очищення графіків і скидання меню
        for i in range(menu.index("end") + 1):
            menu.entryconfig(i, state="normal")
        crs.cell_manager.cells.clear()


# Тести виводу графіків
class TestGraphsOutput(unittest.TestCase):
    def test_output_without_graphs(self):
        crs.cell_manager.show()
        self.assertTrue(ends_with("No cells to plot!"))

    def test_output_plot(self):
        crs.cell_manager.create_cell("plot")
        id, cell = next(iter(crs.cell_manager.cells.items()))
        cell.x.set("1, 2, 3")
        cell.y.set("4, 5, 6")

        crs.cell_manager.show()
        self.assertTrue(ends_with("Successfully plotted!"))
        crs.plt.close()
        crs.cell_manager.delete_cell(id)

    def test_output_scatter(self):
        crs.cell_manager.create_cell("scatter")
        id, cell = next(iter(crs.cell_manager.cells.items()))
        cell.x.set("1, 2, 3")
        cell.y.set("4, 5, 6")

        crs.cell_manager.show()
        self.assertTrue(ends_with("Successfully plotted!"))
        crs.plt.close()
        crs.cell_manager.delete_cell(id)

    def test_output_bar(self):
        crs.cell_manager.create_cell("bar")
        id, cell = next(iter(crs.cell_manager.cells.items()))
        cell.x.set("1, 2, 3")
        cell.y.set("4, 5, 6")

        crs.cell_manager.show()
        self.assertTrue(ends_with("Successfully plotted!"))
        crs.plt.close()
        crs.cell_manager.delete_cell(id)

    def test_output_hist(self):
        crs.cell_manager.create_cell("histogram")
        id, cell = next(iter(crs.cell_manager.cells.items()))
        cell.data.set("1, 1, 2")
        cell.bins.set("2")

        crs.cell_manager.show()
        self.assertTrue(ends_with("Successfully plotted!"))
        crs.plt.close()
        crs.cell_manager.delete_cell(id)

    def test_output_pie(self):
        crs.cell_manager.create_cell("pie")
        id, cell = next(iter(crs.cell_manager.cells.items()))
        cell.data.set("50, 30, 20")

        crs.cell_manager.show()
        self.assertTrue(ends_with("Successfully plotted!"))
        crs.plt.close()
        crs.cell_manager.delete_cell(id)


# Тести при вводі некоректних даних
class TestIncorrectInput(unittest.TestCase):
    def test_incorrect_input(self):
        test_data = [
            ("1, 2, 3, 4, 5, 6", "4, 5, 6"),
            ("1;2;3", "4, 5, 6"),
            ("1 / 2 / 3", "4, 5, 6"),
        ]
        for x, y in test_data:
            crs.cell_manager.create_cell("plot")
            id, value = next(iter(crs.cell_manager.cells.items()))
            value.x.set(x)
            value.y.set(y)
            crs.cell_manager.show()
            self.assertFalse(ends_with("Successfully plotted!"))
            crs.cell_manager.delete_cell(id)


# Тести фарбування рамок графіків
class TestColoring(unittest.TestCase):
    def test_color(self):
        crs.cell_manager.create_cell("plot")
        id, cell = next(iter(crs.cell_manager.cells.items()))
        cell.x.set("1, 2, 3, 4, 5, 6")
        cell.y.set("4, 5, 6")

        crs.cell_manager.show()
        self.assertTrue(cell.frame.cget("bg") == "#FFCCCC")

        cell.x.set("1, 2, 3")
        crs.cell_manager.show()
        self.assertFalse(cell.frame.cget("bg") == "#FFCCCC")
        crs.plt.close()

        crs.cell_manager.delete_cell(id)


# Тести заборони створення графіків, досягнувши максимальний ліміт
class TestMaxGraphs(unittest.TestCase):
    def test_max_graphs(self):
        for i in range(crs.MAX_CELL_NUMBER):
            crs.cell_manager.create_cell("plot")

        self.assertFalse(ends_with("Max number of cells reached!"))

        crs.cell_manager.create_cell("plot")
        self.assertTrue(ends_with("Max number of cells reached!"))

        crs.cell_manager.cells.clear()


if __name__ == "__main__":
    unittest.main()
