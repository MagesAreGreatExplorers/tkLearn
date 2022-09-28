import tkinter as tk
import math
import random
from ctypes import *


class WindowController(object):
    def __init__(self, win):
        win.overrideredirect(True)
        self.__win = win
        self.click_x = 0
        self.click_y = 0
        self.life = True
        self.__win.bind('<Button-1>', self.__get_click_pos)
        self.__win.bind('<B1-Motion>', self.__move)
        self.__win.bind('<KeyPress-Escape>', self.__drop_out)
        self.__win.after(100, lambda: self.__set_win())

    def __get_click_pos(self, event):
        self.click_x = event.x
        self.click_y = event.y

    def __move(self, event):
        x = event.x - self.click_x + self.__win.winfo_x()
        y = event.y - self.click_y + self.__win.winfo_y()
        self.__win.geometry(f'+{x}+{y}')

    # noinspection PyUnusedLocal    event
    def __drop_out(self, event):
        self.__win.destroy()
        self.life = False

    # display in the taskbar
    def __set_win(self):
        hwnd = windll.user32.GetParent(self.__win.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, -20)
        style &= ~0x80
        style |= 0x40000
        windll.user32.SetWindowLongW(hwnd, -20, style)
        self.__win.wm_withdraw()
        self.__win.wm_deiconify()


class Graph(object):
    def __init__(self):
        root = tk.Tk()
        self.__root_controller = WindowController(root)
        scr_h = root.winfo_screenheight()
        self.__length_of_side = scr_h - 100
        self.__mfg = '#00FFFF'
        self.__mbg = '#001020'
        TRANSCOLOUR = 'gray'
        root.wm_attributes('-transparentcolor', TRANSCOLOUR)
        root.geometry(
            f'{self.__length_of_side}x{self.__length_of_side}+'
            f'{(root.winfo_screenwidth() - self.__length_of_side) >> 1}+50'
        )
        self.__cv = tk.Canvas(root, bg=self.__mbg,
                              width=self.__length_of_side, height=self.__length_of_side,
                              highlightbackground=self.__mfg, highlightcolor=self.__mfg)
        self.__cv.pack()
        self.__node_positions = []
        self.__node_pitched_on = False
        self.__matrix = ((1, 0, 0, 0, 7, 0, 0), (0, 19, 0, 0, 0, 0, 0), (1, 0, 0, 0, 7, 0, 0), (1, 0, 0, 0, 0, 7, 0),
                         (0, 0, 0, 0, 4, 0, 9), (0, 0, 0, 0, 0, 7, 6), (10, 0, 0, 12, 0, 0, 6))
        self.__node_num = 7
        self.__init_node_positions()
        self.__show_graph(False)
        root.mainloop()

    @staticmethod
    def get_points_in_mid_perpendicular(x1, y1, x2, y2, distance_to_midpoint):
        midpoint = (int(x1 + x2) >> 1, int(y1 + y2) >> 1)
        # orig_point rotate PI/2 around midpoint
        new1 = (midpoint[0] + midpoint[1] - y1, x1 + midpoint[1] - midpoint[0])
        new2 = (midpoint[0] + midpoint[1] - y2, x2 + midpoint[1] - midpoint[0])
        orig_distance_to_midpoint = int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)) >> 1
        times = distance_to_midpoint / orig_distance_to_midpoint
        return (
            (midpoint[0] + (new1[0] - midpoint[0]) * times,
             midpoint[1] + (new1[1] - midpoint[1]) * times),
            (midpoint[0] + (new2[0] - midpoint[0]) * times,
             midpoint[1] + (new2[1] - midpoint[1]) * times)
        )

    def __init_node_positions(self, circular_distribution=False):
        self.__node_positions = []
        # init nodes and get their positions
        if circular_distribution:
            r = (self.__length_of_side - 100) >> 1
            center_x = self.__length_of_side >> 1
            d_ag = math.pi * 2 / self.__node_num
            for i in range(self.__node_num):
                ag = d_ag * i
                xi = center_x + r * math.cos(ag)
                yi = center_x + r * math.sin(ag)
                self.__node_positions.append((xi, yi))
        else:
            i = 0
            # __*____*____*__
            max_section = self.__length_of_side - 50
            grid_length = (self.__length_of_side - 100) // self.__node_num
            min_section = 50 + (grid_length >> 1)
            while i < self.__node_num:
                xi = random.randrange(min_section, max_section, grid_length)
                yi = random.randrange(min_section, max_section, grid_length)
                pos = (xi, yi)
                if pos in self.__node_positions:
                    continue
                i += 1
                self.__node_positions.append(pos)
            new_sec = grid_length >> 2
            self.__node_positions = [(e[0] + random.randint(-new_sec, new_sec),
                                      e[1] + random.randint(-new_sec, new_sec))
                                     for e in self.__node_positions]

    def __show_graph(self, undirected=True, null_edge=0):
        def click_node(event):
            print(event.x, event.y)
        node_radius = 7
        line_width = 3
        node_text_color = '#00FF00'
        edge_text_color = '#00FFFF'
        node_color = '#2E75B5'
        edge_color = '#8030D0'
        if undirected:
            for i in range(self.__node_num):
                for j in range(i + 1, self.__node_num):
                    if self.__matrix[i][j] != null_edge:
                        self.__cv.create_line(
                            self.__node_positions[i][0], self.__node_positions[i][1],
                            self.__node_positions[j][0], self.__node_positions[j][1],
                            width=line_width, fill=edge_color)
                        self.__cv.create_text(
                            int(self.__node_positions[i][0] + self.__node_positions[j][0]) >> 1,
                            int(self.__node_positions[i][1] + self.__node_positions[j][1]) >> 1,
                            text=f'{self.__matrix[i][j]}', fill=edge_text_color,
                            font=('Times New Roman', 24))
                self.__cv.create_oval(
                    self.__node_positions[i][0] - node_radius, self.__node_positions[i][1] - node_radius,
                    self.__node_positions[i][0] + node_radius, self.__node_positions[i][1] + node_radius,
                    fill=node_color, tags=f'node{i+1}',
                    outline=self.__mfg, width=2
                )
                self.__cv.tag_bind(f'node{i+1}', '<Button-1>', click_node)
                self.__cv.create_text(
                    self.__node_positions[i][0], self.__node_positions[i][1] + 20,
                    text=f'node{i + 1}', fill=node_text_color, font=('Times New Roman', 18))
        else:
            for i in range(self.__node_num):
                for j in range(i + 1, self.__node_num):
                    edge_midpoints = Graph.get_points_in_mid_perpendicular(
                        self.__node_positions[i][0], self.__node_positions[i][1],
                        self.__node_positions[j][0], self.__node_positions[j][1],
                        100
                    )
                    edge_text_positions = Graph.get_points_in_mid_perpendicular(
                        self.__node_positions[i][0], self.__node_positions[i][1],
                        self.__node_positions[j][0], self.__node_positions[j][1],
                        50
                    )
                    if self.__matrix[i][j] != null_edge:
                        edge_points = [self.__node_positions[i][0], self.__node_positions[i][1],
                                       edge_midpoints[0][0], edge_midpoints[0][1],
                                       self.__node_positions[j][0], self.__node_positions[j][1]]
                        self.__cv.create_line(edge_points, fill=edge_color, smooth=True, width=line_width)
                        self.__cv.create_text(edge_text_positions[0][0], edge_text_positions[0][1],
                                              text=f'{self.__matrix[i][j]}', fill=edge_text_color,
                                              font=('Times New Roman', 24))
                    if self.__matrix[j][i] != null_edge:
                        edge_points = [self.__node_positions[j][0], self.__node_positions[j][1],
                                       edge_midpoints[1][0], edge_midpoints[1][1],
                                       self.__node_positions[i][0], self.__node_positions[i][1]]
                        self.__cv.create_line(edge_points, fill=edge_color, smooth=True, width=line_width)
                        self.__cv.create_text(edge_text_positions[1][0], edge_text_positions[1][1],
                                              text=f'{self.__matrix[j][i]}', fill=edge_text_color,
                                              font=('Times New Roman', 24))
                self.__cv.create_oval(
                    self.__node_positions[i][0] - node_radius, self.__node_positions[i][1] - node_radius,
                    self.__node_positions[i][0] + node_radius, self.__node_positions[i][1] + node_radius,
                    fill=node_color, tags=f'node{i + 1}',
                    outline=self.__mfg, width=2
                )
                self.__cv.tag_bind(f'node{i + 1}', '<Button-1>', click_node)
                self.__cv.create_text(
                    self.__node_positions[i][0], self.__node_positions[i][1] + 20,
                    text=f'node{i + 1}', fill=node_text_color, font=('Times New Roman', 18))

    def __move_node(self):
        pass


if __name__ == '__main__':
    graph = Graph()
