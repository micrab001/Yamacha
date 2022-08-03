import math
import numpy as np
# -------------------------------------------------------------------------------------------
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk  # NavigationToolbar2TkAgg
# ------------------------------------------------------------------------------------------
import tkinter as tk

# ------------------------------------------------------------------------------------------


# mpl.rcParams['font.sans-serif'] = ['SimHei']  # Китайский дисплей
# mpl.rcParams['axes.unicode_minus'] = False  # отображение отрицательного знака


class From:
    def __init__(self):
        self.root = tk.Tk()  # Создать основную форму
        self.canvas = tk.Canvas()  # Создать холст для отображения графики
        self.figure = self.create_matplotlib()  # Возвращает объект фигуры фигуры, нарисованной matplotlib
        self.create_form(self.figure)  # Отображение рисунка над формой tkinter
        self.root.mainloop()

    def create_matplotlib(self):
        # Создание рисованного объекта f
        f = plt.figure(num=2, figsize=(16, 12), dpi=80, facecolor="pink", edgecolor='green', frameon=True)
        # Создать субкартинку
        fig1 = plt.subplot(1, 1, 1)

        x = np.arange(0, 2 * np.pi, 0.1)
        y1 = np.sin(x)
        y2 = np.cos(x)

        line1, = fig1.plot(x, y1, color='red', linewidth=3, linestyle='-')  # Рисовать первую строку

        line2, = fig1.plot(x, y2)
        plt.setp(line2, color='black', linewidth=8, linestyle='-', alpha=0.3)  # вторая строка

        fig1.set_title("Это первое изображение", loc = 'center', pad = 20, fontsize = 'xx-large', color = 'red')  # Установить название
        line1.set_label("Синусоида")  # Определить легенду
        fig1.legend(['Sine', 'Cosine'], loc='upper left', facecolor='green', frameon=True, shadow=True, framealpha=0.5,
                    fontsize='xx-large')

        fig1.set_xlabel('abscissa')  # Определить заголовок оси
        fig1.set_ylabel("ордината")
        fig1.set_yticks([-1, -1 / 2, 0, 1 / 2, 1])  # Установить масштаб координатной оси
        fig1.grid(which='major', axis='x', color='r', linestyle='-', linewidth=2)  # сетка

        return f


    def create_form(self, figure):
        # Отображение нарисованной графики в окне tkinter
        self.canvas = FigureCanvasTkAgg(figure, self.root)
        self.canvas.draw()  # В предыдущей версии использовался метод show (). После matplotlib 2.2 больше не рекомендуется использовать show () вместо draw, но использование show не сообщит об ошибке и отобразит предупреждение.


        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Отображение панели инструментов навигации, нарисованной matplotlib в окне tkinter
        toolbar = NavigationToolbar2Tk(self.canvas,
                                       self.root)  # matplotlib версии 2.2 рекомендуется использовать NavigationToolbar2Tk, если вы используете NavigationToolbar2TkAgg предупредит
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    form = From()



# пример программы
# from tkinter import *
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# root = Tk()
# root.geometry('600x500+10+10')
#
# def do_plot(x, y):
#     [ax[x].clear() for x in range(4)]
#     ax[1].plot(x,y)
#     canvas.draw()
#
# frame1 = Frame(root); frame1.place(x=0, y=0, width=500, height=500)
# figure = plt.Figure(figsize=(5,5), facecolor='yellow')
# canvas = FigureCanvasTkAgg(figure, frame1)
# canvas.get_tk_widget().place(x=0,y=0,width=500,height=500)
# ax = [figure.add_subplot(2, 2, x+1) for x in range(4)]
#
# frame2 = Frame(root); frame2.place(x=500, y=0, width=100, height=400)
# btplot1 = Button(frame2, text='plot 1', command= lambda: do_plot([0,1,2],[5,3,7]))
# btplot1.place(x=0, y=50, width=50, height=20)
# btplot2 = Button(frame2, text='plot 2', command= lambda: do_plot([5,6,7],[3,8,2]))
# btplot2.place(x=0, y=100, width=50, height=20)
#
# root.mainloop()





# это другой пример с комментариями
# from tkinter import *
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
#                                                NavigationToolbar2Tk)
#
#
# # plot function is created for
# # plotting the graph in
# # tkinter window
# def plot():
#
#     # the figure that will contain the plot
#     fig = Figure(figsize=(3, 3),
#                  dpi=100)
#
#     # list of squares
#     y = [i ** 2 for i in range(101)]
#
#     # adding the subplot
#     plot1 = fig.add_subplot(111)
#
#     # plotting the graph
#     plot1.plot(y)
#
#     # creating the Tkinter canvas
#     # containing the Matplotlib figure
#     canvas = FigureCanvasTkAgg(fig,
#                                master=window)
#     canvas.draw()
#
#     # placing the canvas on the Tkinter window
#     canvas.get_tk_widget().pack()
#
#     # creating the Matplotlib toolbar
#     toolbar = NavigationToolbar2Tk(canvas,
#                                    window)
#     toolbar.update()
#
#     # placing the toolbar on the Tkinter window
#     canvas.get_tk_widget().pack()
#
#
# # the main Tkinter window
# window = Tk()
#
# # setting the title
# window.title("Plotting in Tkinter")
#
# # dimensions of the main window
# window.geometry("500x500")
#
# # button that displays the plot
# plot_button = Button(master=window,
#                      command=plot,
#                      height=2,
#                      width=10,
#                      text="Plot")
#
# # place the button
# # in main window
# plot_button.pack()
#
# # run the gui
# window.mainloop()
#
