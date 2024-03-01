from tkinter import *
import tensorflow as tf
from PIL import ImageGrab


class Paint(object):

    DEFAULT_PEN_SIZE = 10.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(
            self.root, text='Pen', command=self.use_pen
        )
        self.pen_button.grid(row=0, column=0)

        self.eraser_button = Button(
            self.root, text='Eraser', command=self.use_eraser
        )
        self.eraser_button.grid(row=0, column=2)

        self.recognize_button = Button(
            self.root, text='Recognize', command=self.recognize
        )
        self.recognize_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.DEFAULT_PEN_SIZE
        paint_color = 'white' if self.eraser_on else self.color

        if self.old_x and self.old_y:
            self.c.create_line(
                self.old_x, self.old_y, event.x, event.y,
                width=self.line_width, fill=paint_color,
                capstyle=ROUND, smooth=TRUE, splinesteps=36
            )

        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def save_image(self):
        x = self.root.winfo_rootx() + self.c.winfo_x()
        y = self.root.winfo_rooty() + self.c.winfo_y()
        x1 = x + self.c.winfo_width()
        y1 = y + self.c.winfo_height()
        
        ImageGrab.grab().crop((x, y, x1, y1)).save('.\\imgaes_to_recognize\\img.png')

    def recognize(self):
        model = tf.keras.models.load_model('paint_percep')

        self.save_image()


if __name__ == '__main__':
    Paint()
