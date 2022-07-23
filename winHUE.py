from tkinter import *
from ctypes import *
import os
from base64 import b64decode
from PIL import ImageTk, Image
from pyautogui import position
from keyboard import wait
from re import findall
import image


class ThemColor(object):
    def __init__(self):
        self.main_bg = '#001F3A'
        self.main_fg = '#00E2F2'
        self.bg_text = '#001F3A'
        self.fg_text = '#00E2F2'
        self.bg_entry = '#203864'
        self.fg_entry = '#00E2F2'
        self.fg_butt = '#00E2F2'
        self.active_fg_butt = '#67E73D'
        self.set_them_id = 1

    def set_them1(self):
        self.main_bg = '#001F3A'
        self.main_fg = '#00E2F2'
        self.bg_text = '#001F3A'
        self.fg_text = '#00E2F2'
        self.bg_entry = '#203864'
        self.fg_entry = '#00E2F2'
        self.fg_butt = '#00E2F2'
        self.active_fg_butt = '#67E73D'
        self.set_them_id = 1

    def set_them2(self):
        self.main_bg = '#CCBFE5'
        self.main_fg = '#7030A0'
        self.bg_text = '#CCBFE5'
        self.fg_text = '#7030A0'
        self.bg_entry = '#E5E0EB'
        self.fg_entry = '#7030A0'
        self.fg_butt = '#7030A0'
        self.active_fg_butt = '#A32D9B'
        self.set_them_id = 2


class ColorConverter(object):
    @staticmethod
    def __crt(num, n_max):
        if num > n_max:
            return n_max
        elif num < 0:
            return 0
        return num

    @staticmethod
    def get_input(string, v_type='dft'):
        if v_type == 'hex':
            data_list = findall(r'[0-9a-fA-F]+', string)
            if len(data_list) < 1:
                return None
            if len(data_list[0]) < 6:
                return None
            return data_list[0][:6]
        data_list = findall(r'\d*\.\d+|\d+', string)
        if len(data_list) < 3:
            return None
        return float(data_list[0]), float(data_list[1]), float(data_list[2])

    @staticmethod
    def rgb_to_rgb(r_, g_, b_, f_='.3f', form_='dft'):
        if form_ == 'hs':
            r, g, b = r_ / 255, g_ / 255, b_ / 255
            r, g, b = ColorConverter.__crt(r, 1), ColorConverter.__crt(g, 1), ColorConverter.__crt(b, 1)
            return f'({format(r, f_)}, {format(g, f_)}, {format(b, f_)})'
        else:
            r, g, b = ColorConverter.__crt(r_, 255), ColorConverter.__crt(g_, 255), ColorConverter.__crt(b_, 255)
            return f"({format(r, '.0f')}, {format(g, '.0f')}, {format(b, '.0f')})"

    @staticmethod
    def rgb_to_hex(r_, g_, b_, form_hex='dft'):
        def get_hex_e(d_):
            return '0' + f'{hex(d_)}'[2:] if d_ < 16 else f'{hex(d_)}'[2:]

        r_, g_, b_ = ColorConverter.__crt(r_, 255), ColorConverter.__crt(g_, 255), ColorConverter.__crt(b_, 255)
        r_, g_, b_ = int(format(r_, '.0f')), int(format(g_, '.0f')), int(format(b_, '.0f'))
        if form_hex == 'low':
            return '#' + get_hex_e(r_) + get_hex_e(g_) + get_hex_e(b_)
        return ('#' + get_hex_e(r_) + get_hex_e(g_) + get_hex_e(b_)).upper()

    @staticmethod
    def hex_to_rgb(hex_string):
        return int(hex_string[0:2], 16), int(hex_string[2:4], 16), int(hex_string[4:6], 16)

    @staticmethod
    def rgb_to_hsl(r_, g_, b_, hf='.1f', sf='.2f', lf='.2f', h_form='dft'):
        r_, g_, b_ = ColorConverter.__crt(r_, 255), ColorConverter.__crt(g_, 255), ColorConverter.__crt(b_, 255)
        c_max = max(r_, g_, b_)
        c_min = min(r_, g_, b_)
        delta = c_max - c_min
        # calculate hue
        if delta == 0:
            h = 0
        elif c_max == r_:
            h = (g_ - b_) / delta * 60
        elif c_max == g_:
            h = (b_ - r_) / delta * 60 + 120
        else:
            h = (r_ - g_) / delta * 60 + 240
        h = h + 360 if h < 0 else h  # be positive
        if h_form == 'rs':  # radian system
            pi = 3.141592653589793
            h *= pi / 180
        elif h_form == 'hs':  # hundred-mark system
            h /= 360
        # calculate
        l_ = (c_max + c_min) / 510
        # calculate saturation
        if delta == 0:
            s = 0
        elif l_ <= 0.5:
            s = delta / (c_max + c_min)
        else:
            s = delta / (510 - c_max - c_min)

        return f'({format(h, hf)}, {format(s, sf)}, {format(l_, lf)})'

    @staticmethod
    def hsl_to_rgb(h_, s_, l_, h_form='dft'):
        s_, l_ = ColorConverter.__crt(s_, 1), ColorConverter.__crt(l_, 1)
        if h_form == 'rs':  # radian system
            pi = 3.141592653589793
            h_ *= 180 / pi
        elif h_form == 'hs':  # hundred-mark system
            h_ *= 360
        h_ = ColorConverter.__crt(h_, 359.999999999)
        t = s_ * (1 - abs(2 * l_ - 1))
        c = 255 * (t / 2 + l_)
        x = 255 * (t * (0.5 - abs((h_ / 60) % 2 - 1)) + l_)
        m = 255 * (l_ - t / 2)
        if h_ < 60:
            r, g, b = c, x, m
        elif h_ < 120:
            r, g, b = x, c, m
        elif h_ < 180:
            r, g, b = m, c, x
        elif h_ < 240:
            r, g, b = m, x, c
        elif h_ < 300:
            r, g, b = x, m, c
        else:
            r, g, b = c, m, x
        return r, g, b

    @staticmethod
    def rgb_to_hsv(r_, g_, b_, hf='.1f', sf='.2f', vf='.2f', h_form='dft'):
        r_, g_, b_ = ColorConverter.__crt(r_, 255), ColorConverter.__crt(g_, 255), ColorConverter.__crt(b_, 255)
        c_max = max(r_, g_, b_)
        c_min = min(r_, g_, b_)
        delta = c_max - c_min
        # calculate hue
        if delta == 0:
            h = 0
        elif c_max == r_:
            h = (g_ - b_) / delta * 60
        elif c_max == g_:
            h = (b_ - r_) / delta * 60 + 120
        else:
            h = (r_ - g_) / delta * 60 + 240
        h = h + 360 if h < 0 else h  # be positive
        if h_form == 'rs':  # radian system
            pi = 3.141592653589793
            h *= pi / 180
        elif h_form == 'hs':  # hundred-mark system
            h /= 360
        # calculate saturation
        s = 0 if c_max == 0.0 else delta / c_max
        return f'({format(h, hf)}, {format(s, sf)}, {format(c_max / 255, vf)})'

    @staticmethod
    def hsv_to_rgb(h_, s_, v_, h_form='dft'):
        s_, v_ = ColorConverter.__crt(s_, 1), ColorConverter.__crt(v_, 1)
        if h_form == 'rs':  # radian system
            pi = 3.141592653589793
            h_ *= 180 / pi
        elif h_form == 'hs':  # hundred-mark system
            h_ *= 360
        h_ = ColorConverter.__crt(h_, 359.999999999)
        c = 255 * v_
        x = 255 * v_ * (1 - s_ * abs((h_ / 60) % 2 - 1))
        m = 255 * v_ * (1 - s_)
        if h_ < 60:
            r, g, b = c, x, m
        elif h_ < 120:
            r, g, b = x, c, m
        elif h_ < 180:
            r, g, b = m, c, x
        elif h_ < 240:
            r, g, b = m, x, c
        elif h_ < 300:
            r, g, b = x, m, c
        else:
            r, g, b = c, m, x
        return r, g, b


class TkORRwinController(object):
    def __init__(self, win, ban_xs=(0, 0), ban_ys=(0, 0)):
        self.__ban_xs, self.__ban_ys = ban_xs, ban_ys
        self.__win = win
        self.__click_x = 0
        self.__click_y = 0
        self.life = True
        self.__icon = Main.load_image(image.icon, 'ico')
        self.__win.iconbitmap(self.__icon)
        os.remove(self.__icon)
        self.__win.title('winHUE')
        # self.__win.overrideredirect(True)
        self.__win.bind('<Button-1>', self.__get_click_pos)
        self.__win.bind('<B1-Motion>', self.__move)
        self.__win.bind('<Triple-KeyPress-Escape>', self.__drop_out)
        # self.__win.bind('<Triple-Button-1>', self.__drop_out)
        self.__win.after(100, lambda: self.__set_win())
        self.__top_type = None

    # noinspection PyUnusedLocal    event
    def __get_click_pos(self, event):
        clc_x, clc_y = position()
        self.__click_x, self.__click_y = clc_x - self.__win.winfo_x(), clc_y - self.__win.winfo_y()
        '''
        principle: self.__click_x, self.__click_y = event.x, event.y,
        
        The purpose of using the event is to get the position of 
        the mouse relative to the Tkinter window. 
        but the event works for all widgets.
        '''

    # noinspection PyUnusedLocal    event
    def __move(self, event):
        if not (self.__ban_xs[0] < self.__click_x < self.__ban_xs[1]
                and self.__ban_ys[0] < self.__click_y < self.__ban_ys[1]):
            ex, ey = position()
            x, y = ex - self.__click_x, ey - self.__click_y
            self.__win.geometry(f'+{x}+{y}')
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


class Main(object):
    def __init__(self):
        self.__win = Tk()
        self.__win.overrideredirect(True)
        self.__key_press = 'ctrl'
        self.__r_, self.__g_, self.__b_ = None, None, None
        self.__form_ = 'dft'
        self.__f_ = '.3f'
        self.__form_hex = 'dft'
        self.__lh_form, self.__vh_form = 'dft', 'dft'
        self.__lhf, self.__lsf, self.__lf = '.1f', '.2f', '.2f'
        self.__vhf, self.__vsf, self.__vf = '.1f', '.2f', '.2f'
        self.__type = 'rgb'
        self.__them = ThemColor()
        scr_w = self.__win.winfo_screenwidth()
        scr_h = self.__win.winfo_screenheight()
        self.__win.geometry(f'445x720+{scr_w // 2 - 223}+{scr_h // 2 - 360}')
        self.__win.configure(bg=self.__them.main_bg)
        self.__win.attributes('-transparentcolor', '#000000')
        self.__b2list = None
        self.__b3list = None
        self.__b5list = None
        self.__b6list = None
        self.__b7list = None
        self.__b8list = None
        self.__fd = Main.load_image(image.dark)
        self.__fl = Main.load_image(image.light)
        # canvases for hiding corners
        self.__tc_corners = []
        for filler_i in range(4):
            self.__tc_corners.append(Canvas(self.__win, bg=self.__them.main_fg,
                                            width=50, height=50, bd=0, highlightthickness=0))
        self.__tc_corners[0].place(x=0, y=0)
        self.__tc_corners[1].place(x=395, y=0)
        self.__tc_corners[2].place(x=395, y=670)
        self.__tc_corners[3].place(x=0, y=670)
        self.__cut_corners(30)
        # the first filler
        self.__t_fillers = []
        self.__t_fillers.append(Canvas(self.__win, bg=self.__them.main_bg,
                                       width=200, height=20, bd=0, highlightthickness=0))
        self.__t_fillers[-1].pack(side='top')  # **************************************************filler0
        # Frame for exit Button
        self.__t_frames = []
        self.__t_frames.append(Frame(self.__win, bg=self.__them.main_bg))
        self.__t_frames[-1].pack(side='top')  # ************************************************Frame0
        # filler on the left of exit Button
        self.__t_fillers.append(Canvas(self.__t_frames[-1], bg=self.__them.main_bg,
                                       width=280, height=40, bd=0, highlightthickness=0))
        self.__t_fillers[-1].pack(side='left')
        # exit Button
        self.__t_buttons = []
        self.__t_buttons.append(Button(self.__t_frames[-1], text='exit', bd=0,
                                       bg=self.__them.main_bg, fg=self.__them.fg_butt,
                                       font=('Microsoft YaHei', 13), width=5,
                                       activebackground=self.__them.main_bg,
                                       activeforeground=self.__them.active_fg_butt,
                                       command=lambda: self.__win.destroy()
                                       ))
        self.__t_buttons[-1].pack(side='left')
        # Canvas for displaying color
        self.__tc_displayer_col = Canvas(self.__win, bg=self.__them.main_bg,
                                         width=401, height=150, bd=0, highlightthickness=0)
        self.__tc_displayer_col.pack(side='top')
        self.__display_color_in_canvas()
        # Frame for eyedropper Button and appearance Button
        self.__t_frames.append(Frame(self.__win, bg=self.__them.main_bg))
        self.__t_frames[-1].pack(side='top')  # ************************************************Frame1
        # Button for eyedropper
        self.__t_buttons.append(Button(self.__t_frames[-1], text='eyedropper', bd=0,
                                       bg=self.__them.main_bg, fg=self.__them.fg_butt,
                                       font=('Microsoft YaHei', 13), width=11,
                                       activebackground=self.__them.main_bg,
                                       activeforeground=self.__them.active_fg_butt,
                                       command=lambda: self.__b1_eyedropper()
                                       ))
        self.__t_buttons[-1].pack(side='left')
        # Button for appearance
        self.__t_buttons.append(Button(self.__t_frames[-1], text='appearance', bd=0,
                                       bg=self.__them.main_bg, fg=self.__them.fg_butt,
                                       font=('Microsoft YaHei', 13), width=11,
                                       activebackground=self.__them.main_bg,
                                       activeforeground=self.__them.active_fg_butt,
                                       command=lambda: self.__b2_app()
                                       ))
        self.__t_buttons[-1].pack(side='left')
        # filler between Entry and the previous Frame for eyedropper Button and appearance Button
        self.__t_fillers.append(Canvas(self.__win, bg=self.__them.main_bg,
                                       width=200, height=15, bd=0, highlightthickness=0))
        self.__t_fillers[-1].pack(side='top')  # ************************************************filler1
        # Frame for Entry
        self.__t_frames.append(Frame(self.__win, bg=self.__them.main_bg))
        self.__t_frames[-1].pack(side='top')  # **********************************************Frame2
        # Button for input type
        self.__t_buttons.append(Button(self.__t_frames[-1], text=self.__type + ': ', bd=0,
                                       bg=self.__them.main_bg, fg=self.__them.fg_butt,
                                       font=('Microsoft YaHei', 13), width=4,
                                       activebackground=self.__them.main_bg,
                                       activeforeground=self.__them.active_fg_butt,
                                       command=lambda: self.__b3_type()
                                       ))
        self.__t_buttons[-1].pack(side='left')
        # Entry
        self.__t_entry = Entry(self.__t_frames[-1], bd=0, font=('Times New Roman', 16),
                               justify='center', bg=self.__them.bg_entry, fg=self.__them.fg_entry,
                               selectbackground=self.__them.main_fg, width=17,
                               selectforeground=self.__them.main_bg,
                               insertbackground=self.__them.fg_entry
                               )
        self.__t_entry.pack(side='left')
        self.__t_entry.bind('<Return>', lambda event: self.__b4_ok())
        # confirm Button
        self.__t_buttons.append(Button(self.__t_frames[-1], text='ok', bd=0,
                                       bg=self.__them.main_bg, fg=self.__them.fg_butt,
                                       font=('Microsoft YaHei', 13), width=3,
                                       activebackground=self.__them.main_bg,
                                       activeforeground=self.__them.active_fg_butt,
                                       command=lambda: self.__b4_ok()
                                       ))
        self.__t_buttons[-1].pack(side='left')
        # Texts for displaying color values
        self.__t_texts = []
        self.__init_text()
        # filler for show title
        self.__t_fillers.append(Canvas(self.__win, bg=self.__them.main_bg,
                                       width=218, height=90, bd=0, highlightthickness=0))
        self.__t_fillers[-1].create_image(110, 60, image=self.__fd)
        self.__t_fillers[-1].pack(side='top')
        # get the position of the top left corner of Entry-Frame
        self.__t_frames[2].update()
        ban_x1, ban_y1 = self.__t_frames[2].winfo_x(), self.__t_frames[2].winfo_y()
        # get the ordinate in the lower right corner of the last Text-Frame
        self.__t_fillers[-1].update()
        ban_y2 = self.__t_fillers[-1].winfo_y()
        # Controller
        self.__r_ctrlER = TkORRwinController(self.__win, (ban_x1, 445 - ban_x1), (ban_y1, ban_y2))
        self.__win.mainloop()

    @staticmethod
    def __black_instead(string):
        return '#010101' if string == '#000000' else string

    @staticmethod
    def __press_to_get_rgb(key_press):
        wait(key_press)
        p_x, p_y = position()
        user32 = windll.user32
        gdi32 = windll.gdi32
        hdc = user32.GetDC(None)
        dec_ = gdi32.GetPixel(hdc, p_x, p_y)
        return dec_ & 255, dec_ >> 8 & 255, dec_ >> 16

    @staticmethod
    def load_image(var_name, img_type='png'):
        img_path = f'temporary_files_of_pic.{img_type}'
        if os.path.isfile(img_path):
            os.remove(img_path)
        img_file = open(img_path, 'wb')
        img_file.write(b64decode(var_name))
        img_file.close()
        if img_type == 'png':
            img = ImageTk.PhotoImage(Image.open(img_path))
            os.remove(img_path)
        else:
            img = img_path
        return img

    def __self_def_press_key(self, key_press):
        if key_press == 'ck':
            self.__key_press = 'ctrl'
        elif key_press == 'sk':
            self.__key_press = 'shift'
        else:
            self.__key_press = 'alt'

    def __display_color_in_canvas(self):
        if self.__r_ is not None and self.__g_ is not None and self.__b_ is not None:
            ri, gi, bi = self.__r_ / 230, self.__g_ / 230, self.__b_ / 230
            for line_i in range(20, 250):
                r, g, b = int((line_i - 20) * ri), int((line_i - 20) * gi), int((line_i - 20) * bi)
                self.__tc_displayer_col.create_line([line_i, 15, line_i, 55],
                                                    fill=Main.__black_instead(
                                                        ColorConverter.rgb_to_hex(self.__r_, g, b)
                                                    ))
                self.__tc_displayer_col.create_line([line_i, 55, line_i, 95],
                                                    fill=Main.__black_instead(
                                                        ColorConverter.rgb_to_hex(r, self.__g_, b)
                                                    ))
                self.__tc_displayer_col.create_line([line_i, 95, line_i, 135],
                                                    fill=Main.__black_instead(
                                                        ColorConverter.rgb_to_hex(r, g, self.__b_)
                                                    ))
            rgb = Main.__black_instead(ColorConverter.rgb_to_hex(self.__r_, self.__g_, self.__b_))
            self.__tc_displayer_col.create_rectangle(250, 15, 381, 135, fill=rgb, outline=rgb)
            # polygons for hiding corners
            self.__tc_displayer_col.create_polygon([20, 15, 50, 15, 20, 45, 20, 15],
                                                   fill=self.__them.main_bg, outline=self.__them.main_bg)
            self.__tc_displayer_col.create_polygon([351, 15, 381, 15, 381, 45, 351, 15],
                                                   fill=self.__them.main_bg, outline=self.__them.main_bg)
            self.__tc_displayer_col.create_polygon([351, 135, 381, 135, 381, 105, 351, 135],
                                                   fill=self.__them.main_bg, outline=self.__them.main_bg)
            self.__tc_displayer_col.create_polygon([20, 105, 20, 135, 50, 135, 20, 105],
                                                   fill=self.__them.main_bg, outline=self.__them.main_bg)
        else:
            self.__tc_displayer_col.create_rectangle(20, 15, 381, 135,
                                                     fill=self.__them.main_bg, outline=self.__them.main_bg)
        # border for self.__canvas
        pts = [20, 45, 50, 15, 351, 15, 381, 45, 381, 105, 351, 135, 50, 135, 20, 105, 20, 45]
        for line_i in range(0, 15, 2):
            self.__tc_displayer_col.create_line(pts[line_i:line_i + 4], fill=self.__them.main_fg, width=3)

    def __display_value_in_text(self):
        if self.__r_ is None or self.__g_ is None or self.__b_ is None:
            text_value = ('NONE', 'NONE', 'NONE', 'NONE')
        else:
            text_value = (ColorConverter.rgb_to_hex(
                self.__r_, self.__g_, self.__b_, self.__form_hex
            ),
                          ColorConverter.rgb_to_rgb(
                              self.__r_, self.__g_, self.__b_, self.__f_, self.__form_
                          ),
                          ColorConverter.rgb_to_hsl(
                              self.__r_, self.__g_, self.__b_,
                              self.__lhf, self.__lsf, self.__lf, self.__lh_form
                          ),
                          ColorConverter.rgb_to_hsv(
                              self.__r_, self.__g_, self.__b_,
                              self.__vhf, self.__vsf, self.__vf, self.__vh_form
                          ))
        for idx in range(4):
            self.__t_texts[idx].config(state='normal')
            self.__t_texts[idx].delete('1.0', END)
            self.__t_texts[idx].tag_configure('center', justify='center')
            self.__t_texts[idx].insert(END, text_value[idx], 'center')
            self.__t_texts[idx].config(state='disabled')

    def __cut_corners(self, aw_):
        pt_tuple = ([0, 0, aw_, 0, 0, aw_, 0, 0], [50 - aw_, 0, 50, 0, 50, aw_, 50 - aw_, 0],
                    [50 - aw_, 50, 50, 50 - aw_, 50, 50, 50 - aw_, 50], [0, 50 - aw_, 0, 50, aw_, 50, 0, 50 - aw_])
        for idx in range(4):
            self.__tc_corners[idx].create_rectangle(0, 0, 50, 50,
                                                    fill=self.__them.main_bg, outline=self.__them.main_bg)
            self.__tc_corners[idx].create_polygon(pt_tuple[idx], fill='#000000', outline='#000000')

    def __init_text(self):
        button_id = ('hex: ', 'rgb: ', 'hsl: ', 'hsv: ')
        if self.__r_ is None or self.__g_ is None or self.__b_ is None:
            text_value = ('NONE', 'NONE', 'NONE', 'NONE')
        else:
            text_value = (ColorConverter.rgb_to_hex(self.__r_, self.__g_, self.__b_),
                          ColorConverter.rgb_to_rgb(self.__r_, self.__g_, self.__b_),
                          ColorConverter.rgb_to_hsl(self.__r_, self.__g_, self.__b_),
                          ColorConverter.rgb_to_hsv(self.__r_, self.__g_, self.__b_),
                          )
        for idx in range(4):
            # filler before Frame for Texts
            self.__t_fillers.append(Canvas(self.__win, bg=self.__them.main_bg,
                                           width=200, height=15, bd=0, highlightthickness=0))
            self.__t_fillers[-1].pack(side='top')
            # Frame for setting Button and Text
            self.__t_frames.append(Frame(self.__win, bg=self.__them.main_bg))
            self.__t_frames[-1].pack(side='top')
            # Button for setting
            self.__t_buttons.append(Button(self.__t_frames[-1], text=button_id[idx], bd=0,
                                           bg=self.__them.main_bg, fg=self.__them.fg_butt,
                                           font=('Microsoft YaHei', 13), width=5,
                                           activebackground=self.__them.main_bg,
                                           activeforeground=self.__them.active_fg_butt,
                                           ))
            self.__t_buttons[-1].pack(side='left')
            # Text
            self.__t_texts.append(Text(self.__t_frames[-1], bd=0, font=('Times New Roman', 16),
                                       width=20, height=1,
                                       bg=self.__them.bg_text, fg=self.__them.fg_text,
                                       selectbackground=self.__them.main_fg,
                                       selectforeground=self.__them.main_bg,
                                       insertbackground=self.__them.fg_text,
                                       ))
            self.__t_texts[-1].tag_configure('center', justify='center')
            self.__t_texts[-1].insert(END, text_value[idx], 'center')
            self.__t_texts[-1].config(state='disabled')
            self.__t_texts[-1].pack(side='right')
        self.__t_buttons[5].configure(command=lambda: self.__b5_hex())
        self.__t_buttons[6].configure(command=lambda: self.__b6_rgb())
        self.__t_buttons[7].configure(command=lambda: self.__b7or8_hs(7))
        self.__t_buttons[8].configure(command=lambda: self.__b7or8_hs(8))

    def __b1_eyedropper(self):
        self.__win.withdraw()
        if self.__b3list is not None:
            self.__finish_b3(self.__type)
        if self.__b5list is not None:
            self.__finish_b5(self.__form_hex)
        if self.__b6list is not None:
            self.__finish_b6()
        if self.__b7list is not None:
            self.__finish_b7or8(7)
        if self.__b8list is not None:
            self.__finish_b7or8(8)
        self.__r_, self.__g_, self.__b_ = Main.__press_to_get_rgb(self.__key_press)
        self.__win.deiconify()
        self.__display_color_in_canvas()
        self.__display_value_in_text()

    def __b4_ok(self):
        inputs = self.__t_entry.get()
        self.__t_entry.delete(0, END)
        date = ColorConverter.get_input(inputs, self.__type)
        if date is None:
            self.__r_, self.__g_, self.__b_ = None, None, None
        else:
            if self.__type == 'rgb':
                if self.__form_ == 'hs':
                    self.__r_, self.__g_, self.__b_ = date[0] * 255, date[1] * 255, date[2] * 255
                else:
                    self.__r_, self.__g_, self.__b_ = date

            elif self.__type == 'hex':
                self.__r_, self.__g_, self.__b_ = ColorConverter.hex_to_rgb(date)
            elif self.__type == 'hsl':
                self.__r_, self.__g_, self.__b_ = ColorConverter.hsl_to_rgb(
                    date[0], date[1], date[2], self.__lh_form
                )
            elif self.__type == 'hsv':
                self.__r_, self.__g_, self.__b_ = ColorConverter.hsv_to_rgb(
                    date[0], date[1], date[2], self.__vh_form
                )
        self.__display_color_in_canvas()
        self.__display_value_in_text()

    def __b3_type(self):
        self.__b3list = []
        self.__t_buttons[3].config(state='disabled')
        self.__b3list.append(Toplevel())
        self.__b3list[0].overrideredirect(True)
        self.__b3list[0].configure(bg=self.__them.main_bg)
        Label(self.__b3list[0], text='\n    COLOR MODULES    \n',
              font=('Times New Roman', 16),
              bd=0, bg=self.__them.main_bg, fg=self.__them.main_fg).pack(side='top')
        fra = Frame(self.__b3list[0], bg=self.__them.main_bg)
        fra.pack(side='top')
        but_id = ('hex', 'rgb', 'hsl', 'hsv')
        butts = []
        for idx in range(4):
            butts.append(Button(fra, text=but_id[idx], bd=0,
                                bg=self.__them.main_bg,
                                font=('Microsoft YaHei', 13), width=5,
                                activebackground=self.__them.main_bg,
                                ))
            if but_id[idx] == self.__type:
                butts[idx].configure(fg=self.__them.active_fg_butt,
                                     activeforeground=self.__them.fg_butt, )
            else:
                butts[idx].configure(fg=self.__them.fg_butt,
                                     activeforeground=self.__them.active_fg_butt, )
            butts[idx].pack(side='left')
        butts[0].configure(command=lambda: self.__finish_b3('HEX'))
        butts[1].configure(command=lambda: self.__finish_b3('RGB'))
        butts[2].configure(command=lambda: self.__finish_b3('HSL'))
        butts[3].configure(command=lambda: self.__finish_b3('HSV'))
        self.__b3list[0].update()
        self.__b3list[0].geometry(
            f'+{self.__win.winfo_x() - self.__b3list[0].winfo_width() // 2}'
            f'+{self.__t_frames[2].winfo_y() + self.__win.winfo_y() - self.__b3list[0].winfo_height() // 2}'
        )
        self.__b3list.append(TkORRwinController(self.__b3list[0]))
        self.__b3list[0].mainloop()

    def __finish_b3(self, type_):
        if type_ == 'RGB':
            self.__type = 'rgb'
        elif type_ == 'HEX':
            self.__type = 'hex'
        elif type_ == 'HSL':
            self.__type = 'hsl'
        elif type_ == 'HSV':
            self.__type = 'hsv'
        self.__b3list[0].destroy()
        del self.__b3list[-1]
        self.__b3list = None
        self.__t_buttons[3].config(state='normal')
        self.__t_buttons[3].configure(text=self.__type + ': ')

    def __b5_hex(self):
        self.__b5list = []
        self.__t_buttons[5].config(state='disabled')
        self.__b5list.append(Toplevel())
        self.__b5list[0].overrideredirect(True)
        self.__b5list[0].configure(bg=self.__them.main_bg)
        Label(self.__b5list[0], text='\n    VALUE TYPES    \n',
              font=('Times New Roman', 16),
              bd=0, bg=self.__them.main_bg, fg=self.__them.main_fg).pack(side='top')
        fra = Frame(self.__b5list[0], bg=self.__them.main_bg)
        fra.pack(side='top')
        but_id = ('uppercase', 'lowercase')
        hex_form = ('dft', 'low')
        butts = []
        for idx in range(2):
            butts.append(Button(fra, text=but_id[idx], bd=0,
                                bg=self.__them.main_bg,
                                font=('Microsoft YaHei', 13), width=10,
                                activebackground=self.__them.main_bg,
                                ))
            if hex_form[idx] == self.__form_hex:
                butts[idx].configure(fg=self.__them.active_fg_butt,
                                     activeforeground=self.__them.fg_butt, )
            else:
                butts[idx].configure(fg=self.__them.fg_butt,
                                     activeforeground=self.__them.active_fg_butt, )
            butts[idx].pack(side='left')
        butts[0].configure(command=lambda: self.__finish_b5('dft'))
        butts[1].configure(command=lambda: self.__finish_b5('low'))
        self.__b5list[0].update()
        self.__b5list[0].geometry(
            f'+{self.__win.winfo_x() - self.__b5list[0].winfo_width() // 2}'
            f'+{self.__t_frames[3].winfo_y() + self.__win.winfo_y() - self.__b5list[0].winfo_height() // 2}'
        )
        self.__b5list.append(TkORRwinController(self.__b5list[0]))
        self.__b5list[0].mainloop()

    def __finish_b5(self, type_):
        if type_ == 'low':
            self.__form_hex = 'low'
        else:
            self.__form_hex = 'dft'
        self.__b5list[0].destroy()
        del self.__b5list[-1]
        self.__b5list = None
        self.__t_buttons[5].config(state='normal')

    def __b6_rgb(self):
        self.__b6list = []
        self.__t_buttons[6].config(state='disabled')
        self.__b6list.append(Toplevel())
        self.__b6list[0].overrideredirect(True)
        self.__b6list[0].configure(bg=self.__them.main_bg)
        Label(self.__b6list[0], text='\n    VALUE TYPES    \n',
              font=('Times New Roman', 16),
              bd=0, bg=self.__them.main_bg, fg=self.__them.main_fg).pack(side='top')
        fra = Frame(self.__b6list[0], bg=self.__them.main_bg)
        fra.pack(side='top')
        but_id = ('classic form', 'hundred-mark system')
        rgb_form = ('dft', 'hs')
        widths = (13, 19)
        butts = []
        for idx in range(2):
            butts.append(Button(fra, text=but_id[idx], bd=0,
                                bg=self.__them.main_bg, fg=self.__them.fg_butt,
                                font=('Microsoft YaHei', 13), width=widths[idx],
                                activebackground=self.__them.main_bg,
                                activeforeground=self.__them.active_fg_butt,
                                ))
            if rgb_form[idx] == self.__form_:
                butts[idx].configure(fg=self.__them.active_fg_butt,
                                     activeforeground=self.__them.fg_butt, )
            else:
                butts[idx].configure(fg=self.__them.fg_butt,
                                     activeforeground=self.__them.active_fg_butt, )
            butts[idx].pack(side='left')
        butts[0].configure(command=lambda: self.__set_b6('dft'))
        butts[1].configure(command=lambda: self.__set_b6('hs'))
        Label(self.__b6list[0], text='\n\n    DECIMAL PLACES    \n',
              font=('Times New Roman', 16),
              bd=0, bg=self.__them.main_bg, fg=self.__them.main_fg).pack(side='top')
        self.__b6list.append(Scale(self.__b6list[0], orient=HORIZONTAL, from_=1, to=9,
                                   resolution=1, length=270, sliderlength=20, bd=0,
                                   bg=self.__them.main_bg, fg=self.__them.main_fg,
                                   sliderrelief='flat', font=('Times New Roman', 11),
                                   takefocus=True, tickinterval=1,
                                   activebackground=self.__them.main_bg,
                                   troughcolor=self.__them.main_fg, highlightthickness=0))
        self.__b6list[1].set(value=int(self.__f_[1]))
        self.__b6list[1].pack(side='top')
        b = Button(self.__b6list[0], text='ok', bd=0,
                   bg=self.__them.main_bg, fg=self.__them.fg_butt,
                   font=('Microsoft YaHei', 13), width=3,
                   activebackground=self.__them.main_bg,
                   activeforeground=self.__them.active_fg_butt,
                   command=lambda: self.__finish_b6()
                   )
        b.pack(side='top')
        c = Canvas(self.__b6list[0], bg=self.__them.main_bg,
                   width=20, height=20, bd=0, highlightthickness=0)
        c.pack(side='top')
        self.__b6list[0].update()
        width = self.__b6list[0].winfo_width()
        self.__b6list[0].geometry(
            f'+{self.__win.winfo_x() - width // 2}'
            f'+{self.__t_frames[4].winfo_y() + self.__win.winfo_y() - self.__b6list[0].winfo_height() // 2}'
        )
        self.__b6list.append(butts)
        self.__b6list[1].update()
        ban_x1, ban_y1 = self.__b6list[1].winfo_x(), self.__b6list[1].winfo_y()
        b.update()
        ban_y2 = b.winfo_y()
        self.__b6list.append(TkORRwinController(self.__b6list[0], (ban_x1, width - ban_x1), (ban_y1, ban_y2)))
        self.__b6list[0].mainloop()

    def __set_b6(self, type_):
        self.__form_ = type_
        rgb_form = ('dft', 'hs')
        for idx in range(2):
            if rgb_form[idx] == self.__form_:
                self.__b6list[-2][idx].configure(fg=self.__them.active_fg_butt,
                                                 activeforeground=self.__them.fg_butt, )
            else:
                self.__b6list[-2][idx].configure(fg=self.__them.fg_butt,
                                                 activeforeground=self.__them.active_fg_butt, )

    def __finish_b6(self):
        self.__f_ = f'.{self.__b6list[1].get()}f'
        self.__b6list[0].destroy()
        del self.__b6list[-1]
        self.__b6list = None
        self.__t_buttons[6].config(state='normal')

    def __b7or8_hs(self, order):
        b7or8list = []
        self.__t_buttons[order].config(state='disabled')
        b7or8list.append(Toplevel())
        b7or8list[0].overrideredirect(True)
        b7or8list[0].configure(bg=self.__them.main_bg)
        Label(b7or8list[0], text='\n    VALUE TYPES FOR H    \n',
              font=('Times New Roman', 16),
              bd=0, bg=self.__them.main_bg, fg=self.__them.main_fg).pack(side='top')
        but_id = ('classic form', 'hundred-mark system', 'radian system')
        form = ('dft', 'hs', 'rs')
        h_form = self.__lh_form if order == 7 else self.__vh_form
        widths = (13, 19, 14)
        butts = []
        for idx in range(3):
            butts.append(Button(b7or8list[0], text=but_id[idx], bd=0,
                                bg=self.__them.main_bg, fg=self.__them.fg_butt,
                                font=('Microsoft YaHei', 13), width=widths[idx],
                                activebackground=self.__them.main_bg,
                                activeforeground=self.__them.active_fg_butt,
                                ))
            if form[idx] == h_form:
                butts[idx].configure(fg=self.__them.active_fg_butt,
                                     activeforeground=self.__them.fg_butt, )
            else:
                butts[idx].configure(fg=self.__them.fg_butt,
                                     activeforeground=self.__them.active_fg_butt, )
            butts[idx].pack(side='top')
        butts[0].configure(command=lambda: self.__set_b7or8(order, 'dft'))
        butts[1].configure(command=lambda: self.__set_b7or8(order, 'hs'))
        butts[2].configure(command=lambda: self.__set_b7or8(order, 'rs'))
        Label(b7or8list[0], text='\n\n    DECIMAL PLACES    \n',
              font=('Times New Roman', 16),
              bd=0, bg=self.__them.main_bg, fg=self.__them.main_fg).pack(side='top')
        fra = []
        v_id = ('H: ', 'S: ', 'L: ') if order == 7 else ('H: ', 'S: ', 'V: ')
        slide_value = (self.__lhf, self.__lsf, self.__lf) if order == 7 else (self.__vhf, self.__vsf, self.__vf)
        for idx in range(3):
            fra.append(Frame(b7or8list[0], bg=self.__them.main_bg))
            fra[idx].pack(side='top')
            Label(fra[idx], text=v_id[idx],
                  font=('Times New Roman', 13),
                  bd=0, bg=self.__them.main_bg, fg=self.__them.main_fg).pack(side='left')
            b7or8list.append(Scale(fra[idx], orient=HORIZONTAL, from_=1, to=9,
                                   resolution=1, length=270, sliderlength=20, bd=0,
                                   bg=self.__them.main_bg, fg=self.__them.main_fg,
                                   sliderrelief='flat', font=('Times New Roman', 11),
                                   takefocus=True, tickinterval=1,
                                   activebackground=self.__them.main_bg,
                                   troughcolor=self.__them.main_fg, highlightthickness=0))
            b7or8list[1 + idx].set(value=int(slide_value[idx][1]))
            b7or8list[1 + idx].pack(side='left')
        b = Button(b7or8list[0], text='ok', bd=0,
                   bg=self.__them.main_bg, fg=self.__them.fg_butt,
                   font=('Microsoft YaHei', 13), width=3,
                   activebackground=self.__them.main_bg,
                   activeforeground=self.__them.active_fg_butt,
                   command=lambda: self.__finish_b7or8(order)
                   )
        b.pack(side='top')
        c = Canvas(b7or8list[0], bg=self.__them.main_bg,
                   width=400, height=20, bd=0, highlightthickness=0)
        c.pack(side='top')
        b7or8list[0].update()
        width = b7or8list[0].winfo_width()
        b7or8list[0].geometry(
            f'+{self.__win.winfo_x() - width // 2}'
            f'+{self.__t_frames[4].winfo_y() + self.__win.winfo_y() - b7or8list[0].winfo_height() // 2}'
        )
        b7or8list.append(butts)
        fra[0].update()
        ban_x1, ban_y1 = fra[0].winfo_x(), fra[0].winfo_y()
        b.update()
        ban_y2 = b.winfo_y()
        b7or8list.append(TkORRwinController(b7or8list[0], (ban_x1, width - ban_x1), (ban_y1, ban_y2)))
        if order == 7:
            self.__b7list = b7or8list
        else:
            self.__b8list = b7or8list
        b7or8list[0].mainloop()

    def __set_b7or8(self, order, type_):
        if order == 7:
            self.__lh_form = type_
        else:
            self.__vh_form = type_
        form = ('dft', 'hs', 'rs')
        h_form = self.__lh_form if order == 7 else self.__vh_form
        b7or8list = self.__b7list if order == 7 else self.__b8list
        for idx in range(3):
            if form[idx] == h_form:
                b7or8list[-2][idx].configure(fg=self.__them.active_fg_butt,
                                             activeforeground=self.__them.fg_butt, )
            else:
                b7or8list[-2][idx].configure(fg=self.__them.fg_butt,
                                             activeforeground=self.__them.active_fg_butt, )

    def __finish_b7or8(self, order):
        if order == 7:
            self.__lhf = f'.{self.__b7list[1].get()}f'
            self.__lsf = f'.{self.__b7list[2].get()}f'
            self.__lf = f'.{self.__b7list[3].get()}f'
            self.__b7list[0].destroy()
            del self.__b7list[-1]
            self.__b7list = None
        else:
            self.__vhf = f'.{self.__b8list[1].get()}f'
            self.__vsf = f'.{self.__b8list[2].get()}f'
            self.__vf = f'.{self.__b8list[3].get()}f'
            self.__b8list[0].destroy()
            del self.__b8list[-1]
            self.__b8list = None
        self.__t_buttons[order].config(state='normal')

    def __b2_app(self):
        self.__b2list = []
        self.__t_buttons[2].config(state='disabled')
        self.__b2list.append(Toplevel())
        self.__b2list[0].overrideredirect(True)
        self.__b2list[0].configure(bg=self.__them.main_bg)
        Label(self.__b2list[0], text='\n    RECOMMENDED APPEARANCES    \n',
              font=('Times New Roman', 16),
              bd=0, bg=self.__them.main_bg, fg=self.__them.main_fg).pack(side='top')
        fra = Frame(self.__b2list[0], bg=self.__them.main_bg)
        fra.pack(side='top')
        but_id = ('dark theme', 'light theme')
        butts = []
        for idx in range(2):
            butts.append(Button(fra, text=but_id[idx], bd=0,
                                bg=self.__them.main_bg,
                                font=('Microsoft YaHei', 13), width=10,
                                activebackground=self.__them.main_bg,
                                fg=self.__them.fg_butt,
                                activeforeground=self.__them.active_fg_butt,
                                ))
            butts[idx].pack(side='left')
        if self.__them.set_them_id == 1:
            butts[0].configure(fg=self.__them.active_fg_butt,
                               activeforeground=self.__them.fg_butt, )
        else:
            butts[1].configure(fg=self.__them.active_fg_butt,
                               activeforeground=self.__them.fg_butt, )
        butts[0].configure(command=lambda: self.__finish_b2(1))
        butts[1].configure(command=lambda: self.__finish_b2(2))
        c = Canvas(self.__b2list[0], bg=self.__them.main_bg,
                   width=400, height=20, bd=0, highlightthickness=0)
        c.pack(side='top')
        self.__b2list[0].update()
        width = self.__b2list[0].winfo_width()
        self.__b2list[0].geometry(
            f'+{self.__win.winfo_x() + width // 2}'
            f'+{self.__t_frames[1].winfo_y() + self.__win.winfo_y() - self.__b2list[0].winfo_height() // 2}'
        )
        self.__b2list.append(TkORRwinController(self.__b2list[0]))

    def __finish_b2(self, serial_n):
        self.__them.set_them1() if serial_n == 1 else self.__them.set_them2()
        self.__win.configure(bg=self.__them.main_bg)
        self.__tc_displayer_col.configure(bg=self.__them.main_bg)
        self.__display_color_in_canvas()
        for cori in self.__tc_corners:
            cori.configure(bg=self.__them.main_bg)
            self.__cut_corners(30)
        for but_i in self.__t_buttons:
            but_i.configure(bg=self.__them.main_bg, fg=self.__them.main_fg,
                            activebackground=self.__them.main_bg,
                            activeforeground=self.__them.active_fg_butt)
        for fil_i in self.__t_fillers:
            fil_i.configure(bg=self.__them.main_bg)
        for fra_i in self.__t_frames:
            fra_i.configure(bg=self.__them.main_bg)
        self.__t_entry.configure(bg=self.__them.bg_entry,
                                 fg=self.__them.fg_entry,
                                 selectbackground=self.__them.main_fg,
                                 selectforeground=self.__them.main_bg,
                                 insertbackground=self.__them.fg_entry
                                 )
        for tex_i in self.__t_texts:
            tex_i.configure(bg=self.__them.bg_text, fg=self.__them.fg_text,
                            selectbackground=self.__them.main_fg,
                            selectforeground=self.__them.main_bg,
                            insertbackground=self.__them.fg_text, )
        self.__t_fillers[-1].create_rectangle(0, 0, 218, 90,
                                              fill=self.__them.main_bg, outline=self.__them.main_bg)
        self.__t_fillers[-1].create_image(110, 60, image=self.__fd) \
            if self.__them.set_them_id == 1 \
            else self.__t_fillers[-1].create_image(110, 60, image=self.__fl)
        self.__b2list[0].destroy()
        del self.__b2list[-1]
        self.__b2list = None
        self.__t_buttons[2].config(state='normal')


if __name__ == '__main__':
    main = Main()
