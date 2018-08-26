class Box():
    def __init__(self, obj_names):
        self.box_list={}
        for obj_name in obj_names:
            self.box_list[obj_name] = []

    def get_all_boxes(self):
        return self.box_list

    def get_boxes(self, obj_name):
        return self.box_list[obj_name]

    def add_box(self, obj_name, box):
        self.box_list[obj_name].append(box)

    def remove_box(self, obj_name):
        box_len = len(self.box_list[obj_name])
        if box_len > 0:
            self.box_list[obj_name].pop(len(self.box_list[obj_name])-1)
        else:
            print('{0} box is empty'.format(obj_name))
