import math
import random
import tkinter as tk
from math import sqrt

import icon


class Graph(object):
    def __init__(self, matrix, null_edge=0, undirected=False):
        #
        self.__root_bg = '#783CB4'
        self.__node_fill = '#2E75B5'
        self.__node_outline = '#00FFFF'
        self.__node_tag_color = '#783CB4'
        self.__edge_fill = '#00FF00'
        self.__edge_tag_color = '#00FFFF'
        #
        self.__vertical_distance_node_tag = 20
        self.__node_radius = 7
        self.__node_line_width = 3
        self.__arc_edge_sagitta = 100
        self.__edge_line_width = 2
        #
        self.__undirected = undirected
        self.__null_edge = null_edge
        max_row = len(matrix)
        max_div = max(max_row, max([len(col) for col in matrix]))
        self.__node_num = max_div
        self.__matrix = list(matrix)
        for row_i in range(max_div):
            if row_i >= max_row:
                self.__matrix.append([])
            else:
                self.__matrix[row_i] = list(self.__matrix[row_i])
            for col_j in range(max_div):
                if col_j >= len(self.__matrix[row_i]):
                    self.__matrix[row_i].append(self.__null_edge)
        self.__node_positions = []
        self.__undirected_edges = []
        self.__in_edges = []
        self.__out_edges = []
        self.__node_names = []
        for row_i in range(self.__node_num):
            self.__undirected_edges.append([])
            self.__in_edges.append([])
            self.__out_edges.append([])
            self.__node_names.append(f'N{row_i + 1}')
        #
        self.__root = tk.Tk()
        self.__root.title('Graph')
        icon.set_icon(self.__root)
        self.__init_height = self.__root.winfo_screenheight() >> 1
        self.__init_width = self.__root.winfo_screenwidth() >> 1
        self.__root.configure(bg=self.__root_bg)
        self.__cv = tk.Canvas(self.__root, bg='#001020',
                              width=self.__init_width, height=self.__init_height,
                              highlightbackground=self.__root_bg, highlightcolor=self.__root_bg)
        self.__cv.pack(fill="both", expand=True)
        self.__cv.update()
        self.__root.bind('<KeyPress-Escape>', lambda event: self.__root.destroy())
        self.__init_node_positions()
        self.__init_graph()
        self.__root.mainloop()

    def __init_node_positions(self):
        self.__node_positions = []
        node_i = 0
        # example: 50__*____*____*__50
        max_section_y = self.__init_height - 50
        grid_length_y = (self.__init_height - 100) // self.__node_num
        min_section_y = 50 + (grid_length_y >> 1)
        max_section_x = self.__init_width - 50
        grid_length_x = (self.__init_width - 100) // self.__node_num
        min_section_x = 50 + (grid_length_x >> 1)
        while node_i < self.__node_num:
            xi = random.randrange(min_section_x, max_section_x, grid_length_x)
            yi = random.randrange(min_section_y, max_section_y, grid_length_y)
            pos = (xi, yi)
            if pos in self.__node_positions:
                continue
            node_i += 1
            self.__node_positions.append(pos)
        new_sec_y = grid_length_y >> 2
        new_sec_x = grid_length_x >> 2
        self.__node_positions = [(e[0] + random.randint(-new_sec_x, new_sec_x),
                                  e[1] + random.randint(-new_sec_y, new_sec_y))
                                 for e in self.__node_positions]

    @staticmethod
    def __get_points_in_mid_perpendicular(x1, y1, x2, y2, distance_to_midpoint):
        midpoint = (int(x1 + x2) >> 1, int(y1 + y2) >> 1)
        # orig_point rotate PI/2 around midpoint
        new1 = (midpoint[0] + midpoint[1] - y1, x1 + midpoint[1] - midpoint[0])
        new2 = (midpoint[0] + midpoint[1] - y2, x2 + midpoint[1] - midpoint[0])
        orig_distance_to_midpoint = int(sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)) >> 1
        times = distance_to_midpoint / orig_distance_to_midpoint \
            if orig_distance_to_midpoint != 0 else 1
        return (
            (midpoint[0] + (new1[0] - midpoint[0]) * times,
             midpoint[1] + (new1[1] - midpoint[1]) * times),
            (midpoint[0] + (new2[0] - midpoint[0]) * times,
             midpoint[1] + (new2[1] - midpoint[1]) * times)
        )

    def __create_node(self, idx):
        self.__cv.create_oval(
            self.__node_positions[idx][0] - self.__node_radius,
            self.__node_positions[idx][1] - self.__node_radius,
            self.__node_positions[idx][0] + self.__node_radius,
            self.__node_positions[idx][1] + self.__node_radius,
            fill=self.__node_fill, tags=f'node{idx}',
            outline=self.__node_outline, width=self.__node_line_width
        )
        self.__cv.tag_bind(f'node{idx}', '<B1-Motion>',
                           lambda event, tags=f'node{idx}': self.__drag_to_move_node(event, tags))
        self.__cv.create_text(
            self.__node_positions[idx][0],
            self.__node_positions[idx][1] + self.__vertical_distance_node_tag,
            tags=f'n_text{idx}',
            text=self.__node_names[idx], fill=self.__node_tag_color, font=('Times New Roman', 18))

    def __get_last_point_position_of_arc_edge(self, ix, iy, jdx):
        pb = (ix, iy)
        pe = self.__node_positions[jdx]
        node_node_distance = math.sqrt((pb[1] - pe[1]) ** 2 + (pb[0] - pe[0]) ** 2)
        times = (
                        node_node_distance - self.__node_radius - self.__node_line_width
                ) / node_node_distance if node_node_distance != 0 else 1
        return pb[0] + (pe[0] - pb[0]) * times, pb[1] + (pe[1] - pb[1]) * times

    def __get_mid_positions_of_arc_edges_symmetric(self, idx, jdx):
        edge_midpoints = Graph.__get_points_in_mid_perpendicular(
            self.__node_positions[idx][0], self.__node_positions[idx][1],
            self.__node_positions[jdx][0], self.__node_positions[jdx][1],
            self.__arc_edge_sagitta
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

    def __reset_arc_edge_point_positions(self, idx):
        if self.__undirected:
            for edge_i in self.__undirected_edges[idx]:
                edge_tag = self.__cv.itemcget(edge_i, 'tags')
                separator_i = edge_tag.index('<')
                ia = int(edge_tag[4:separator_i])
                idx_ = ia if ia != idx else int(edge_tag[separator_i + 1:])
                # noinspection PyTypeChecker
                self.__cv.coords(edge_i,
                                 self.__node_positions[idx_][0],
                                 self.__node_positions[idx_][1],
                                 self.__node_positions[idx][0],
                                 self.__node_positions[idx][1]
                                 )
                self.__cv.moveto(f'e_text{edge_tag[4:]}',
                                 (self.__node_positions[idx][0] + self.__node_positions[idx_][0]) >> 1,
                                 (self.__node_positions[idx][1] + self.__node_positions[idx_][1]) >> 1
                                 )
        else:
            for edge_i in self.__out_edges[idx]:
                edge_tag = self.__cv.itemcget(edge_i, 'tags')
                separator_i = edge_tag.index('to')
                ia = int(edge_tag[4:separator_i])
                idx_ = ia if ia != idx else int(edge_tag[separator_i + 2:])
                arc_mid, mid_t = self.__get_mid_positions_of_arc_edges_symmetric(idx, idx_)
                if self.__matrix[idx_][idx] != self.__null_edge:
                    end_x, end_y = self.__get_last_point_position_of_arc_edge(
                        arc_mid[0][0], arc_mid[0][1], idx_
                    )
                    edge_pos = [
                        self.__node_positions[idx][0],
                        self.__node_positions[idx][1],
                        arc_mid[0][0], arc_mid[0][1],
                        end_x, end_y]
                    text_pos = [mid_t[0][0], mid_t[0][1]]
                else:
                    end_x, end_y = self.__get_last_point_position_of_arc_edge(
                        self.__node_positions[idx][0], self.__node_positions[idx][1], idx_)
                    edge_pos = [self.__node_positions[idx][0], self.__node_positions[idx][1],
                                end_x, end_y]
                    text_pos = [(self.__node_positions[idx][0] + self.__node_positions[idx_][0]) >> 1,
                                (self.__node_positions[idx][1] + self.__node_positions[idx_][1]) >> 1
                                ]
                # noinspection PyTypeChecker
                self.__cv.coords(edge_i,
                                 edge_pos
                                 )
                self.__cv.moveto(f'e_text{edge_tag[4:]}',
                                 text_pos[0], text_pos[1]
                                 )
            for edge_i in self.__in_edges[idx]:
                edge_tag = self.__cv.itemcget(edge_i, 'tags')
                separator_i = edge_tag.index('to')
                ia = int(edge_tag[4:separator_i])
                idx_ = ia if ia != idx else int(edge_tag[separator_i + 2:])
                arc_mid, mid_t = self.__get_mid_positions_of_arc_edges_symmetric(idx_, idx)
                if self.__matrix[idx][idx_] != 0:
                    end_x, end_y = self.__get_last_point_position_of_arc_edge(
                        arc_mid[0][0], arc_mid[0][1], idx
                    )
                    edge_pos = [self.__node_positions[idx_][0], self.__node_positions[idx_][1],
                                arc_mid[0][0], arc_mid[0][1], end_x, end_y]
                    text_pos = [mid_t[0][0], mid_t[0][1]]
                else:
                    end_x, end_y = self.__get_last_point_position_of_arc_edge(
                        self.__node_positions[idx_][0], self.__node_positions[idx_][1], idx)
                    edge_pos = [self.__node_positions[idx_][0],
                                self.__node_positions[idx_][1], end_x, end_y]
                    text_pos = [
                        (self.__node_positions[idx][0] + self.__node_positions[idx_][0]) >> 1,
                        (self.__node_positions[idx][1] + self.__node_positions[idx_][1]) >> 1]
                # noinspection PyTypeChecker
                self.__cv.coords(edge_i, edge_pos)
                self.__cv.moveto(f'e_text{edge_tag[4:]}', text_pos[0], text_pos[1])

    def __drag_to_move_node(self, event, tag):
        x, y = event.x, event.y
        x -= self.__node_radius + self.__node_line_width
        y -= self.__node_radius + self.__node_line_width
        diameter = self.__node_radius << 1
        if 0 < x < self.__cv.winfo_width() - diameter \
                and 0 < y < self.__cv.winfo_height() - diameter:
            cx = x + self.__node_radius + self.__node_line_width
            cy = y + self.__node_radius + self.__node_line_width
            self.__node_positions[int(tag[4:])] = (cx, cy)
            self.__cv.moveto(tag, x, y)
            tx_bbox = self.__cv.bbox(f'n_text{tag[4:]}')
            self.__cv.moveto(f'n_text{tag[4:]}',
                             cx - ((tx_bbox[2] - tx_bbox[0]) >> 1),
                             cy - ((tx_bbox[3] - tx_bbox[1]) >> 1)
                             + self.__vertical_distance_node_tag
                             )
            self.__reset_arc_edge_point_positions(int(tag[4:]))

    def __drag_to_move_edge(self, event, idx, tag):
        x, y = event.x, event.y
        self.__cv.moveto(f'e_text{tag[4:]}', x, y)
        if self.__undirected:
            start_pos = self.__node_positions[int(tag[4:tag.index('<')])]
            end_pos = self.__node_positions[int(tag[tag.index('<') + 1:])]
            ex = (x << 1) - ((start_pos[0] + end_pos[0]) >> 1)
            ey = (y << 1) - ((start_pos[1] + end_pos[1]) >> 1)
            self.__cv.coords(idx, start_pos[0], start_pos[1], ex, ey,
                             end_pos[0], end_pos[1], )
        else:
            start_pos = self.__node_positions[int(tag[4:tag.index('to')])]
            end_pos = self.__node_positions[int(tag[tag.index('to') + 2:])]
            ex = (x << 1) - ((start_pos[0] + end_pos[0]) >> 1)
            ey = (y << 1) - ((start_pos[1] + end_pos[1]) >> 1)
            end_x, end_y = self.__get_last_point_position_of_arc_edge(
                ex, ey, int(tag[tag.index('to') + 2:]))
            self.__cv.coords(idx, start_pos[0], start_pos[1], ex, ey,
                             end_x, end_y)

    def __init_graph(self):
        if self.__undirected:  # tags naming rule: edge{i}<{j}, e_text{i}<{j}, n_text{i}
            for node_i in range(self.__node_num):
                for node_j in range(node_i + 1, self.__node_num):
                    if self.__matrix[node_i][node_j] != self.__null_edge:
                        edge = self.__cv.create_line(
                            self.__node_positions[node_i][0], self.__node_positions[node_i][1],
                            self.__node_positions[node_j][0], self.__node_positions[node_j][1],
                            width=self.__edge_line_width, fill=self.__edge_fill,
                            smooth=True, tags=f'edge{node_i}<{node_j}')
                        self.__undirected_edges[node_i].append(edge)
                        self.__undirected_edges[node_j].append(edge)
                        self.__cv.tag_bind(f'edge{node_i}<{node_j}', '<B1-Motion>',
                                           lambda event, edge_id=edge, tags=f'edge{node_i}<{node_j}':
                                           self.__drag_to_move_edge(event, edge_id, tags))
                        self.__cv.create_text(
                            int(self.__node_positions[node_i][0]
                                + self.__node_positions[node_j][0]) >> 1,
                            int(self.__node_positions[node_i][1]
                                + self.__node_positions[node_j][1]) >> 1,
                            text=f'{self.__matrix[node_i][node_j]}',
                            fill=self.__edge_tag_color, tags=f'e_text{node_i}<{node_j}',
                            font=('Times New Roman', 24))
                self.__create_node(node_i)
        else:  # tags naming rule: edge{i}to{j}, e_text{i}to{j}, n_text{i}
            for node_i in range(self.__node_num):
                for node_j in range(node_i + 1, self.__node_num):
                    edge_midpoints = None
                    edge_text_positions = None
                    if self.__matrix[node_i][node_j] != self.__null_edge \
                            or self.__matrix[node_j][node_i] != self.__null_edge:
                        edge_midpoints, edge_text_positions = \
                            self.__get_mid_positions_of_arc_edges_symmetric(node_i, node_j)
                    if self.__matrix[node_i][node_j] != self.__null_edge:
                        if self.__matrix[node_j][node_i] != self.__null_edge:
                            end = self.__get_last_point_position_of_arc_edge(
                                edge_midpoints[0][0], edge_midpoints[0][1], node_j)
                            edge_points = [self.__node_positions[node_i][0],
                                           self.__node_positions[node_i][1],
                                           edge_midpoints[0][0], edge_midpoints[0][1],
                                           end[0], end[1]]
                            text_pos = [edge_text_positions[0][0], edge_text_positions[0][1]]
                        else:
                            end = self.__get_last_point_position_of_arc_edge(
                                self.__node_positions[node_i][0],
                                self.__node_positions[node_i][1], node_j
                            )
                            edge_points = [self.__node_positions[node_i][0],
                                           self.__node_positions[node_i][1], end[0], end[1]]
                            text_pos = [(self.__node_positions[node_i][0]
                                         + self.__node_positions[node_j][0]) >> 1,
                                        (self.__node_positions[node_i][1]
                                         + self.__node_positions[node_j][1]) >> 1]
                        edge = self.__cv.create_line(edge_points, fill=self.__edge_fill, smooth=True,
                                                     width=self.__edge_line_width,
                                                     tags=f'edge{node_i}to{node_j}', arrow=tk.LAST)
                        self.__in_edges[node_j].append(edge)
                        self.__out_edges[node_i].append(edge)
                        self.__cv.tag_bind(f'edge{node_i}to{node_j}', '<B1-Motion>',
                                           lambda event, edge_id=edge, tags=f'edge{node_i}to{node_j}':
                                           self.__drag_to_move_edge(event, edge_id, tags))
                        self.__cv.create_text(text_pos,
                                              text=f'{self.__matrix[node_i][node_j]}',
                                              fill=self.__edge_tag_color,
                                              tags=f'e_text{node_i}to{node_j}',
                                              font=('Times New Roman', 24))
                    if self.__matrix[node_j][node_i] != self.__null_edge:
                        if self.__matrix[node_i][node_j] != self.__null_edge:
                            end = self.__get_last_point_position_of_arc_edge(
                                edge_midpoints[1][0], edge_midpoints[1][1], node_i)
                            edge_points = [self.__node_positions[node_j][0],
                                           self.__node_positions[node_j][1],
                                           edge_midpoints[1][0], edge_midpoints[1][1],
                                           end[0], end[1]]
                            text_pos = [edge_text_positions[1][0], edge_text_positions[1][1]]
                        else:
                            end = self.__get_last_point_position_of_arc_edge(
                                self.__node_positions[node_j][0], self.__node_positions[node_j][1], node_i)
                            edge_points = [self.__node_positions[node_j][0],
                                           self.__node_positions[node_j][1], end[0], end[1]]
                            text_pos = [
                                (self.__node_positions[node_i][0] + self.__node_positions[node_j][0]) >> 1,
                                (self.__node_positions[node_i][1] + self.__node_positions[node_j][1]) >> 1
                            ]
                        edge = self.__cv.create_line(edge_points, fill=self.__edge_fill, smooth=True,
                                                     width=self.__edge_line_width,
                                                     tags=f'edge{node_j}to{node_i}', arrow=tk.LAST)
                        self.__in_edges[node_i].append(edge)
                        self.__out_edges[node_j].append(edge)
                        self.__cv.tag_bind(f'edge{node_j}to{node_i}', '<B1-Motion>',
                                           lambda event, edge_id=edge, tags=f'edge{node_j}to{node_i}':
                                           self.__drag_to_move_edge(event, edge_id, tags))
                        self.__cv.create_text(text_pos,
                                              text=f'{self.__matrix[node_j][node_i]}', fill=self.__edge_tag_color,
                                              tags=f'e_text{node_j}to{node_i}',
                                              font=('Times New Roman', 24))
                self.__create_node(node_i)


if __name__ == '__main__':
    a = []
    for i in range(random.randint(5, 8)):
        b = []
        for j in range(random.randint(2, 4)):
            b.append(random.randint(0, 100))
        a.append(b)

    graph = Graph(a)
