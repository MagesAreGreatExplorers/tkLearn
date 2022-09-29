import math
import tkinter as tk
from math import sqrt
import random
from pyautogui import position
from ctypes import *
import icon


class WindowController(object):
    def __init__(self, win, drag_able_height):
        win.overrideredirect(True)
        self.__win = win
        self.__drag_able_height = drag_able_height
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

    # noinspection PyUnusedLocal    event
    def __move(self, event):
        ex, ey = position()
        if ey - self.__win.winfo_y() < self.__drag_able_height:
            x, y = ex - self.click_x, ey - self.click_y
            self.__win.geometry(f'+{x}+{y if y > 0 else 0}')
        '''
        principle: 
            x = event.x - self.__click_x + self.__win.winfo_x()
            y = event.y - self.__click_y + self.__win.winfo_y()
            self.__win.geometry(f'+{x}+{y}')
        '''

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
        self.__root = tk.Tk()
        self.__height = self.__root.winfo_screenheight() - 200
        self.__width = self.__root.winfo_screenwidth() - 200
        self.__root.title('graph')
        self.__mfg = '#00FFFF'
        self.__root.configure(bg=self.__mfg)
        icon.set_icon(self.__root)
        tk.Button(self.__root, background=self.__mfg, text='EXIT', foreground='#783CB4',
                  activeforeground=self.__mfg, highlightbackground=self.__mfg,
                  activebackground='#783CB4', relief='ridge',
                  command=lambda: self.__root.destroy()).pack(side='top')
        self.__cv = tk.Canvas(self.__root, bg='#001020',
                              width=self.__width, height=self.__height,
                              highlightbackground=self.__mfg, highlightcolor=self.__mfg)
        self.__cv.pack(side='bottom')
        self.__cv.update()
        self.__cv_winfo_y = self.__cv.winfo_y()
        self.__cv_winfo_x = self.__cv.winfo_x()
        self.__root_controller = WindowController(self.__root, self.__cv_winfo_y)
        self.__root.geometry(
            f'+'
            f'{(self.__root.winfo_screenwidth() - self.__width) >> 1}+'
            f'{(self.__root.winfo_screenheight() - self.__height - self.__cv_winfo_y) >> 1}'
        )
        self.__undirected = False
        self.__null_edge = 0
        self.__distance_y_text_node = 20
        self.__node_radius = 7
        self.__node_line = 2
        self.__arc_distance_to_midpoint = 100
        self.__node_color = '#2E75B5'
        self.__node_text_color = '#00FF00'
        # test___________________________________________
        a = []
        for i in range(4):
            s = []
            for j in range(4):
                s.append(random.randint(0, 2))
            a.append(s)
        # test___________________________________________
        self.__matrix = a
        self.__node_num = 4
        self.__node_positions = []
        self.__undirected_edges = []
        self.__in_edge = []
        self.__out_edge = []
        for i in range(self.__node_num):
            self.__undirected_edges.append([])
            self.__in_edge.append([])
            self.__out_edge.append([])
        self.__init_node_positions()
        self.__show_graph()
        self.__root.mainloop()

    def __init_node_positions(self):
        self.__node_positions = []
        i = 0
        # example: 50__*____*____*__50
        max_section_y = self.__height - 50
        grid_length_y = (self.__height - 100) // self.__node_num
        min_section_y = 50 + (grid_length_y >> 1)
        max_section_x = self.__width - 50
        grid_length_x = (self.__width - 100) // self.__node_num
        min_section_x = 50 + (grid_length_x >> 1)
        while i < self.__node_num:
            xi = random.randrange(min_section_x, max_section_x, grid_length_x)
            yi = random.randrange(min_section_y, max_section_y, grid_length_y)
            pos = (xi, yi)
            if pos in self.__node_positions:
                continue
            i += 1
            self.__node_positions.append(pos)
        new_sec_y = grid_length_y >> 2
        new_sec_x = grid_length_x >> 2
        self.__node_positions = [(e[0] + random.randint(-new_sec_x, new_sec_x),
                                  e[1] + random.randint(-new_sec_y, new_sec_y))
                                 for e in self.__node_positions]

    @staticmethod
    def get_points_in_mid_perpendicular(x1, y1, x2, y2, distance_to_midpoint):
        midpoint = (int(x1 + x2) >> 1, int(y1 + y2) >> 1)
        # orig_point rotate PI/2 around midpoint
        new1 = (midpoint[0] + midpoint[1] - y1, x1 + midpoint[1] - midpoint[0])
        new2 = (midpoint[0] + midpoint[1] - y2, x2 + midpoint[1] - midpoint[0])
        orig_distance_to_midpoint = int(sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)) >> 1
        times = distance_to_midpoint / orig_distance_to_midpoint
        return (
            (midpoint[0] + (new1[0] - midpoint[0]) * times,
             midpoint[1] + (new1[1] - midpoint[1]) * times),
            (midpoint[0] + (new2[0] - midpoint[0]) * times,
             midpoint[1] + (new2[1] - midpoint[1]) * times)
        )

    def __create_nodes(self, idx):
        self.__cv.create_oval(
            self.__node_positions[idx][0] - self.__node_radius, self.__node_positions[idx][1] - self.__node_radius,
            self.__node_positions[idx][0] + self.__node_radius, self.__node_positions[idx][1] + self.__node_radius,
            fill=self.__node_color, tags=f'node{idx}',
            outline=self.__mfg, width=self.__node_line
        )
        self.__cv.tag_bind(f'node{idx}', '<B1-Motion>',
                           lambda event, tags=f'node{idx}': self.__drag_to_move_node(tags))
        self.__cv.create_text(
            self.__node_positions[idx][0], self.__node_positions[idx][1] + self.__distance_y_text_node,
            tags=f'n_text{idx}',
            text=f'node{idx + 1}', fill=self.__node_text_color, font=('Times New Roman', 18))

    def __get_arc_edge_end_point(self, idx, jdx):
        pb = self.__node_positions[idx]
        pe = self.__node_positions[jdx]
        node_node_distance = math.sqrt((pb[1]-pe[1])**2+(pb[0]-pe[0])**2)
        times = (node_node_distance-self.__node_radius-self.__node_line)/node_node_distance
        return pb[0] + (pe[0] - pb[0]) * times, pb[1] + (pe[1] - pb[1]) * times

    def __get_arc_edge_mid_pos(self, idx, jdx):
        edge_midpoints = Graph.get_points_in_mid_perpendicular(
            self.__node_positions[idx][0], self.__node_positions[idx][1],
            self.__node_positions[jdx][0], self.__node_positions[jdx][1],
            self.__arc_distance_to_midpoint
        )
        edge_text_positions = (
            (edge_midpoints[0][0] + (int(edge_midpoints[1][0] - edge_midpoints[0][0]) >> 2),
             edge_midpoints[0][1] + (int(edge_midpoints[1][1] - edge_midpoints[0][1]) >> 2)),
            (edge_midpoints[1][0] + (int(edge_midpoints[0][0] - edge_midpoints[1][0]) >> 2),
             edge_midpoints[1][1] + (int(edge_midpoints[0][1] - edge_midpoints[1][1]) >> 2))
        )
        # edge_text_positions = Graph.get_points_in_mid_perpendicular(
        #     self.__node_positions[i][0], self.__node_positions[i][1],
        #     self.__node_positions[j][0], self.__node_positions[j][1],
        #     self.__arc_distance_to_midpoint >> 1
        # )
        return edge_midpoints, edge_text_positions

    def __drag_edge_end(self, idx):
        if self.__undirected:
            for i in self.__undirected_edges[idx]:
                edge_tag = self.__cv.itemcget(i, 'tags')
                separator_i = edge_tag.index('<')
                ia = int(edge_tag[4:separator_i])
                idx_ = ia if ia != idx else int(edge_tag[separator_i+1:])
                # noinspection PyTypeChecker
                self.__cv.coords(i,
                                 self.__node_positions[idx_][0],
                                 self.__node_positions[idx_][1],
                                 self.__node_positions[idx][0],
                                 self.__node_positions[idx][1]
                                 )
                self.__cv.moveto(f'e_text{edge_tag[4:]}',
                                 (self.__node_positions[idx][0]+self.__node_positions[idx_][0]) >> 1,
                                 (self.__node_positions[idx][1]+self.__node_positions[idx_][1]) >> 1
                                 )
        else:
            for i in self.__out_edge[idx]:
                edge_tag = self.__cv.itemcget(i, 'tags')
                separator_i = edge_tag.index('to')
                ia = int(edge_tag[4:separator_i])
                idx_ = ia if ia != idx else int(edge_tag[separator_i + 2:])
                arc_mid, mid_t = self.__get_arc_edge_mid_pos(idx, idx_)
                end_x, end_y = self.__get_arc_edge_end_point(idx, idx_)
                edge_pos = [
                    self.__node_positions[idx][0],
                    self.__node_positions[idx][1],
                    arc_mid[0][0], arc_mid[0][1],
                    end_x, end_y
                ] if self.__matrix[idx_][idx] != self.__null_edge else [
                    self.__node_positions[idx][0],
                    self.__node_positions[idx][1],
                    end_x, end_y
                ]
                # noinspection PyTypeChecker
                self.__cv.coords(i,
                                 edge_pos
                                 )
                text_pos = [mid_t[0][0], mid_t[0][1]
                            ] if self.__matrix[idx_][idx] != self.__null_edge else [
                    (self.__node_positions[idx][0]+self.__node_positions[idx_][0]) >> 1,
                    (self.__node_positions[idx][1]+self.__node_positions[idx_][1]) >> 1,
                ]
                self.__cv.moveto(f'e_text{edge_tag[4:]}',
                                 text_pos[0], text_pos[1]
                                 )
            for i in self.__in_edge[idx]:
                edge_tag = self.__cv.itemcget(i, 'tags')
                separator_i = edge_tag.index('to')
                ia = int(edge_tag[4:separator_i])
                idx_ = ia if ia != idx else int(edge_tag[separator_i + 2:])
                arc_mid, mid_t = self.__get_arc_edge_mid_pos(idx_, idx)
                end_x, end_y = self.__get_arc_edge_end_point(idx_, idx)
                edge_pos = [
                    self.__node_positions[idx_][0],
                    self.__node_positions[idx_][1],
                    arc_mid[0][0], arc_mid[0][1],
                    end_x, end_y
                ] if self.__matrix[idx][idx_] != 0 else [
                    self.__node_positions[idx_][0],
                    self.__node_positions[idx_][1],
                    end_x, end_y
                ]
                # noinspection PyTypeChecker
                self.__cv.coords(i,
                                 edge_pos
                                 )
                text_pos = [
                    mid_t[0][0], mid_t[0][1]
                ] if self.__matrix[idx][idx_] != 0 else [
                    (self.__node_positions[idx][0] + self.__node_positions[idx_][0]) >> 1,
                    (self.__node_positions[idx][1] + self.__node_positions[idx_][1]) >> 1,
                ]
                self.__cv.moveto(f'e_text{edge_tag[4:]}',
                                 text_pos[0], text_pos[1]
                                 )

    def __drag_to_move_node(self, tag):
        x, y = position()
        x -= self.__root.winfo_x()+self.__cv_winfo_x+self.__node_radius+self.__node_line
        y -= self.__root.winfo_y()+self.__cv_winfo_y+self.__node_radius + self.__node_line
        diameter = self.__node_radius << 1
        if 0 < x < self.__width - diameter and diameter < y < self.__height - diameter:
            cx = x + self.__node_radius+self.__node_line
            cy = y + self.__node_radius+self.__node_line
            self.__node_positions[int(tag[4:])] = (cx, cy)
            self.__cv.moveto(tag, x, y)
            tx_bbox = self.__cv.bbox(f'n_text{tag[4:]}')
            self.__cv.moveto(f'n_text{tag[4:]}',
                             cx - ((tx_bbox[2]-tx_bbox[0]) >> 1),
                             cy - ((tx_bbox[3]-tx_bbox[1]) >> 1)+self.__distance_y_text_node)
            self.__drag_edge_end(int(tag[4:]))

    def __show_graph(self):
        line_width = 3
        edge_text_color = '#00FFFF'
        edge_color = '#8030D0'
        if self.__undirected:  # tags naming rule: edge{i}<{j}, e_text{i}<{j}, n_text{i}
            for i in range(self.__node_num):
                for j in range(i + 1, self.__node_num):
                    if self.__matrix[i][j] != self.__null_edge:
                        edge = self.__cv.create_line(
                            self.__node_positions[i][0], self.__node_positions[i][1],
                            self.__node_positions[j][0], self.__node_positions[j][1],
                            width=line_width, fill=edge_color, tags=f'edge{i}<{j}')
                        self.__undirected_edges[i].append(edge)
                        self.__undirected_edges[j].append(edge)
                        self.__cv.create_text(
                            int(self.__node_positions[i][0] + self.__node_positions[j][0]) >> 1,
                            int(self.__node_positions[i][1] + self.__node_positions[j][1]) >> 1,
                            text=f'{self.__matrix[i][j]}', fill=edge_text_color, tags=f'e_text{i}<{j}',
                            font=('Times New Roman', 24))
                self.__create_nodes(i)
        else:  # tags naming rule: edge{i}to{j}, e_text{i}to{j}, n_text{i}
            for i in range(self.__node_num):
                for j in range(i + 1, self.__node_num):
                    edge_midpoints = None
                    edge_text_positions = None
                    if self.__matrix[i][j] != self.__null_edge or self.__matrix[j][i] != self.__null_edge:
                        edge_midpoints, edge_text_positions = self.__get_arc_edge_mid_pos(i, j)
                    if self.__matrix[i][j] != self.__null_edge:
                        end = self.__get_arc_edge_end_point(i, j)
                        edge_points = [self.__node_positions[i][0], self.__node_positions[i][1],
                                       edge_midpoints[0][0], edge_midpoints[0][1],
                                       end[0], end[1]] if self.__matrix[j][i] != self.__null_edge else [
                            self.__node_positions[i][0], self.__node_positions[i][1],
                            end[0], end[1]]
                        edge = self.__cv.create_line(edge_points, fill=edge_color, smooth=True,
                                                     width=line_width, tags=f'edge{i}to{j}', arrow=tk.LAST)
                        self.__in_edge[j].append(edge)
                        self.__out_edge[i].append(edge)
                        text_pos = [edge_text_positions[0][0], edge_text_positions[0][1]
                                    ] if self.__matrix[j][i] != self.__null_edge else [
                            (self.__node_positions[i][0]+self.__node_positions[j][0]) >> 1,
                            (self.__node_positions[i][1]+self.__node_positions[j][1]) >> 1]
                        self.__cv.create_text(text_pos,
                                              text=f'{self.__matrix[i][j]}', fill=edge_text_color,
                                              tags=f'e_text{i}to{j}',
                                              font=('Times New Roman', 24))
                    if self.__matrix[j][i] != self.__null_edge:
                        end = self.__get_arc_edge_end_point(j, i)
                        edge_points = [self.__node_positions[j][0], self.__node_positions[j][1],
                                       edge_midpoints[1][0], edge_midpoints[1][1],
                                       end[0], end[1]] if self.__matrix[i][j] != self.__null_edge else [
                            self.__node_positions[j][0], self.__node_positions[j][1],
                            end[0], end[1]]
                        edge = self.__cv.create_line(edge_points, fill=edge_color, smooth=True,
                                                     width=line_width,
                                                     tags=f'edge{j}to{i}', arrow=tk.LAST)
                        self.__in_edge[i].append(edge)
                        self.__out_edge[j].append(edge)
                        text_pos = [edge_text_positions[1][0], edge_text_positions[1][1]
                                    ] if self.__matrix[i][j] != self.__null_edge else [
                            (self.__node_positions[i][0] + self.__node_positions[j][0]) >> 1,
                            (self.__node_positions[i][1] + self.__node_positions[j][1]) >> 1]
                        self.__cv.create_text(text_pos,
                                              text=f'{self.__matrix[j][i]}', fill=edge_text_color,
                                              tags=f'e_text{j}to{i}',
                                              font=('Times New Roman', 24))
                self.__create_nodes(i)


if __name__ == '__main__':
    graph = Graph()
