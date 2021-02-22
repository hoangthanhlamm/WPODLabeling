from tkinter import *
from PIL import Image, ImageTk
import cv2

from os.path import splitext, basename, isfile

from utils import resize


class GUI:
    def __init__(self, img_path):
        self.img_path = img_path
        img = cv2.imread(self.img_path)
        (self.w, self.h), self.ratio = resize(img.shape[1], img.shape[0])

        self.points = []
        self.lines = []
        self.history = []
        self.tmp_reset = None

        self.root = Tk()
        self.frame = Frame(self.root, bd=2, relief=SUNKEN)
        self.canvas = Canvas(self.frame, bd=0)
        self.build()

        self.quit = 'n'

    def build(self):
        size = str(self.w) + 'x' + str(self.h)
        self.root.geometry(size)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        # x_scroll = Scrollbar(self.frame, orient=HORIZONTAL)
        # x_scroll.grid(row=1, column=0, sticky=E + W)
        # y_scroll = Scrollbar(self.frame)
        # y_scroll.grid(row=0, column=1, sticky=N + S)
        # self.canvas = self.canvas(self.frame, bd=0, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)

        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)
        # x_scroll.config(command=self.canvas.xview)
        # y_scroll.config(command=self.canvas.yview)
        self.frame.pack(fill=BOTH, expand=1)

    def check_labeled(self):
        text_file = splitext(self.img_path)[0] + '.txt'
        print(text_file)
        if isfile(text_file):
            with open(text_file, 'r') as f:
                line = f.read().split(',')
                n_pts = int(line[0])
                for i in range(n_pts):
                    self.points.append([float(line[i + 1]), float(line[n_pts + i + 1])])
            return True
        return False

    def get_points(self):
        return self.points

    def print_points(self):
        print(self.points)
    
    def click_coord(self, event):
        # outputting x and y points to console
        x = round(event.x / self.w, 6)
        y = round(event.y / self.h, 6)
        if len(self.points) > 0:
            last = self.points[-1]
            line_id = self.canvas.create_line(last[0] * self.w, last[1] * self.h, event.x, event.y, fill='#f11')
            self.lines.append(line_id)
        self.points.append([x, y])
        self.history.append('p')
        print("\tNew points: " + str(x) + ", " + str(y))

    def draw(self):
        print("\tDraw labeled")
        pre = self.points[0]
        for pts in self.points[1:]:
            line_id = self.canvas.create_line(pre[0] * self.w, pre[1] * self.h, pts[0] * self.w, pts[1] * self.h, fill='#1f1')
            pre = pts
            self.lines.append(line_id)
        line_id = self.canvas.create_line(pre[0] * self.w, pre[1] * self.h, self.points[0][0] * self.w, self.points[0][1] * self.h, fill='#1f1')
        self.lines.append(line_id)

    def cycle(self, event):
        if len(self.points) > 2 and len(self.points) != len(self.lines):
            print("\tCycled")
            first = self.points[0]
            last = self.points[-1]
            line_id = self.canvas.create_line(last[0] * self.w, last[1] * self.h, first[0] * self.w, first[1] * self.h, fill='#f11')
            self.lines.append(line_id)
            self.history.append('c')
        else:
            print("\tNothing to cycled")

    def reset(self, event):
        print("\tReset")
        self.tmp_reset = {
            'points': self.points.copy(),
            'lines': self.lines.copy()
        }
        self.points.clear()

        for line in self.lines:
            self.canvas.delete(line)
        self.lines.clear()
        self.history.append('r')

    def save(self, event):
        print("\tSaved")
        dest = splitext(self.img_path)[0] + '.txt'
        n_pts = len(self.points)
        label = str(n_pts) + ','
        for idx in range(2):
            for pts in self.points:
                label += str(pts[idx]) + ','
        label += ','

        with open(dest, 'w') as f:
            f.write(label)
            f.write('\n')

    def undo(self, event):
        if self.history:
            c = self.history.pop()
            if c == 'p':
                print("\tUndo click point")
                self.points.pop()
                if len(self.points) > 0:
                    line = self.lines.pop()
                    self.canvas.delete(line)
            elif c == 'c':
                print("\tUndo cycled")
                if len(self.points) > 2:
                    line = self.lines.pop()
                    self.canvas.delete(line)
            elif c == 'r':
                print("\tUndo reset")
                if self.tmp_reset:
                    self.points = self.tmp_reset['points'].copy()
                    self.lines = self.tmp_reset['lines'].copy()
                    pre = self.points[0]
                    for pts in self.points[1:]:
                        self.canvas.create_line(pre[0] * self.w, pre[1] * self.h, pts[0] * self.w, pts[1] * self.h, fill='#f11')
                        pre = pts
                    if len(self.points) == len(self.lines):
                        self.canvas.create_line(pre[0] * self.w, pre[1] * self.h, self.points[0][0] * self.w, self.points[0][1] * self.h, fill='#f11')

        else:
            print("\tNothing to undo")

    def previous(self, event):
        self.quit = 'p'
        self.root.destroy()

    def all_quit(self, event):
        self.quit = 'x'
        print("Exit...")
        self.root.destroy()

    def run(self):
        print("Image", basename(self.img_path))
        image = Image.open(self.img_path)
        image = image.resize((self.w, self.h), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=img, anchor="nw")
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

        if self.check_labeled():
            self.draw()

        # mouseclick event
        self.canvas.bind("<Button 1>", self.click_coord)

        # keyboard event
        self.root.bind('c', self.cycle)
        self.root.bind('r', self.reset)
        self.root.bind('s', self.save)
        self.root.bind('z', self.undo)
        self.root.bind('p', self.previous)
        self.root.bind('x', self.all_quit)
        self.root.bind('q', lambda event: self.root.destroy())

        self.root.mainloop()

        print()
        return self.points, self.quit


if __name__ == '__main__':
    gui = GUI('/home/vegeta/Desktop/PrepareDataVnOCR/data/00029.jpg')
    _, c = gui.run()
    gui.print_points()
    if c == 'p':
        print('previous')
    elif c == 'n':
        print('next')
