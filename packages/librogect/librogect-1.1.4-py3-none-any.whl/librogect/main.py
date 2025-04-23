def lib():

    from tkinter import Tk,Label,Entry,Canvas, Button, LAST

    window = Tk()
    window.title("Калькулятор квадратных уравнений")
    window.geometry('700x250')
    window.configure(bg="#8dd3f7")
    lbl = Label(window, text="Введите пример:")
    lbl.grid(column=0, row=0)
    lbl = Label(window, text="f(x)=")
    lbl.grid(column=2, row=0)
    txt = Entry(window, width=10)
    txt.grid(column=1, row=0)
    f = Entry(window, width=10)
    f.grid(column=3, row=0)
    def btn1():
        def btn3():  # Очистка ответа и примера
            btn3.destroy()
            btn5.destroy()

        import math
        y = txt.get()
        x_in_1 = y.rfind('x')
        x_in_2 = y.find('x')

        if y.find('-', 0, x_in_2) == -1:  # фигня для поиска '-' у а
            kol_a = 1
            kola = 0
            a = y[kola]
            for i in range(1, x_in_2):
                a += y[kol_a]
                kol_a += 1
            a = int(a)
        else:
            kol_a = 3
            kola = 2
            a = y[kola]
            for i in range(3, x_in_2):
                a += y[kol_a]
                kol_a += 1
            a = (-1) * int(a)
        if y.find('-', x_in_2, x_in_1) == -1:  # фигня для поиска '-' у b
            kol_b = x_in_2 + 7
            kolb = x_in_2 + 6
            b = y[kolb]
            for i in range(x_in_2 + 7, x_in_1):
                b += y[kol_b]
                kol_b += 1
            b = int(b)
        else:
            kol_b = x_in_2 + 7
            kolb = x_in_2 + 6
            b = y[kolb]
            for i in range(x_in_2 + 7, x_in_1):
                b += y[kol_b]
                kol_b += 1
            b = (-1) * int(b)

        if y.find('-', x_in_1, y.find('=')) == -1:  # фигня для поиска '-' у c
            kol_c = x_in_1 + 4
            kolc = x_in_1 + 3
            c = y[kolc]
            for i in range(x_in_1 + 3, y.find('=') - 1):
                c += y[kol_c]
                kol_c += 1
            c = int(c)
        else:
            kol_c = x_in_1 + 4
            kolc = x_in_1 + 3
            c = y[kolc]
            for i in range(x_in_1 + 3, y.find('=') - 1):
                c += y[kol_c]
                kol_c += 1
            c = (-1) * int(c)
        D = b * b - 4 * a * c
        if D >= 0:
            d = (math.sqrt(D))
        if D > 0:
            imp = 'x1 =', (((-1) * b) - d) / (2 * a), 'x2 =', (((-1) * b) + d) / (2 * a)
        elif D == 0:

            imp = ('x =', ((-1) * b) / (2 * a))
        else:
            imp = ('Корней нет(((')
        btn5 = Button(window, text="Ответ: "+str(imp),bg = '#8dd3f7')
        btn5.grid(column=0, row=2)


        btn3 = Button(window, text="Очистить!", command=btn3)
        btn3.grid(column=0, row=1)

    def btn2():
        lbl = Label(window, text="Введите минимальные и максимальные точки осей Ох и Оу")
        lbl.grid(column=3, row=3)
        xMin = Entry(window, width=10)
        xMin.grid(column=3, row=4)
        xMax = Entry(window, width=10)
        xMax.grid(column=3, row=5)
        yMin = Entry(window, width=10)
        yMin.grid(column=3, row=6)
        yMax = Entry(window, width=10)
        yMax.grid(column=3, row=7)
        lbl = Label(window, text="X минимальное:")
        lbl.grid(column=2, row=4)
        lbl = Label(window, text="Х максимальное:")
        lbl.grid(column=2, row=5)
        lbl = Label(window, text="У минимальное:")
        lbl.grid(column=2, row=6)
        lbl = Label(window, text="У максимальное:")
        lbl.grid(column=2, row=7)

        def btn4():
            root = Tk()
            root.title('График функции')
            xfull = int(xMax.get()) - int(xMin.get())
            yfull = int(yMax.get()) - int(yMin.get())
            canv = Canvas(root, width=int(xfull), height=int(yfull), bg="white", cursor="pencil")
            root.geometry(str(xfull) + 'x' + str(yfull))
            canv.create_line(0, int(yMax.get()), 2 * int(xMax.get()), int(yMax.get()), width=2, arrow=LAST,arrowshape='8 15 5')
            canv.create_line(int(xMax.get()), 2 * int(yMax.get()), int(xMax.get()), 0, width=2, arrow=LAST,arrowshape='8 15 5')
            g = int(xMax.get()) - int(xMin.get())
            x = int(xMin.get())
            canv.pack()
            z = f.get()
            r = xMin.get()
            x = int(r)
            while x <= int(2 * xMax.get()):
                try:
                    new_f = z.replace('x', str(x))
                    new_f2 = z.replace('x', str(x + 1))
                    y = -eval(new_f) + 2 * int(xMax.get())
                    y_2 = -eval(new_f2) + 2 * int(xMax.get())
                    canv.create_line(x + int(xMax.get()), y - int(yMax.get()), x + 1 + int(xMax.get()),
                                    y_2 - int(yMax.get()), width=4)
                except:
                    pass
                x += 1

            canv.pack()
            root.mainloop()

        btn4 = Button(window, text="Построить график!", command=btn4)
        btn4.grid(column=2, row=8)

    btn1 = Button(window, text="Решить!", command=btn1)
    btn1.grid(column=0, row=1)
    btn2 = Button(window, text="Построить график!", command=btn2)
    btn2.grid(column=2, row=1)

    window.mainloop()

