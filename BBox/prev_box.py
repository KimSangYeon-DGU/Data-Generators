class Prev_Box():
    def __init__(self, x1, y1, x2, y2):
        print(' Init Prev box')
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def set_left_point(self, x, y):
        self.x1 = x
        self.y1 = y

    def set_right_point(self, x, y):
        self.x2 = x
        self.y2 = y

    def get_box(self):
        return tuple((self.x1, self.y1, self.x2, self.y2))