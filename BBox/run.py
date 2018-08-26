import os, cv2, argparse
import image_loader
import prev_box, prev_line, box
from color import get_color_bgr
import xml_generator

def mouse_handler(event, x, y, flags, param):
    global PREV_BOX, PREV_LINE, PREV_BOX_DRAW, PREV_LINE_DRAW, boxer, liner, img_w, img_h, box_info, obj_name
    if event == cv2.EVENT_LBUTTONDOWN:
        PREV_BOX = True
        PREV_LINE = False
        PREV_LINE_DRAW = False
        x, y = check_coordinates(x, y)
        boxer.set_left_point(x, y)

    elif PREV_BOX == True and event == cv2.EVENT_MOUSEMOVE:
        PREV_BOX_DRAW = True
        x, y = check_coordinates(x, y)
        boxer.set_right_point(x, y)

    elif PREV_LINE == True and event == cv2.EVENT_MOUSEMOVE:
        PREV_LINE_DRAW = True
        x, y = check_coordinates(x, y)
        liner.set_left_point(x, y)
        liner.set_right_point(img_w-1, img_h-1)

    elif event == cv2.EVENT_LBUTTONUP:
        PREV_BOX = False
        PREV_BOX_DRAW = False
        PREV_LINE = True
        PREV_LINE_DRAW = True
        liner.set_left_point(x, y)
        box_info.add_box(obj_name, boxer.get_box())

def check_coordinates(x, y):
    global img_w, img_h

    if x < 0:
        x = 0
    elif x >= img_w:
        x = img_w - 1

    if y < 0:
        y = 0
    elif y >= img_h:
        y = img_h - 1

    return x, y

def init(args):
    global img_dir_path, box_dir_path, mode, loader, ws_name, boxer, liner, box_info, obj_names, color_names, data_generator
    print('init')

    datasets_path = './datasets/'
    ws_name = 'fire'
    img_dir_path = datasets_path + 'images/' + ws_name
    box_dir_path = datasets_path + 'boxes/' + ws_name

    if args['video'] == 'True':
        mode = 'video'
    elif args['image'] == 'True':
        mode = 'image'
        loader = image_loader.Image(img_dir_path, box_dir_path)

    if os.path.exists(box_dir_path) == False:
        os.mkdir(box_dir_path)
    
    boxer = prev_box.Prev_Box(0, 0, 0, 0)
    liner = prev_line.Prev_Line(0, 0, 0, 0)
    obj_names = ['fire', 'person']
    color_names = {'fire':'cyan', 'person':'magenta'}
    box_info = box.Box(obj_names)
    data_generator = xml_generator.XML_Generator()

def write_boxes(img_name, img_path, dst_dir_path, img_w, img_h, img_c, data_type):
    global obj_names, box_info

    box_list = box_info.get_all_boxes()
    data_generator.write(img_name, img_path, dst_dir_path, img_w, img_h, 3, box_list, obj_names, data_type)

def run():
    global mode, loader, ws_name, PREV_BOX, PREV_LINE, img_w, img_h, boxer, PREV_BOX_DRAW, PREV_LINE_DRAW, box_info, obj_name, obj_names, image_name, data_generator, box_dir_path
    print('Run')
    
    cv2.namedWindow(ws_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(ws_name, mouse_handler)
    img_idx = 0
    obj_idx = 0

    img_len = loader.get_file_length()
    ESC = 27
    NEXT = 83
    PREV = 81
    SPACE_BAR = 32
    BACK_SPACE = 8
    ENTER = 13
    PREV_BOX = False
    PREV_LINE = True
    PREV_BOX_DRAW = False
    PREV_LINE_DRAW = False

    obj_name = obj_names[0]
    print('Current object name: {}'.format(obj_name))
    while True:
        image = loader.get_image(img_idx)
        image_name = loader.get_image_name(img_idx)
        img_h, img_w = image.shape[:2]
        clone = image.copy()
        
        if PREV_BOX_DRAW == True:
            bx = boxer.get_box()
            cv2.rectangle(clone, (bx[0], bx[1]), (bx[2], bx[3]), (255, 0, 0), 1)

        elif PREV_LINE_DRAW == True:
            v_line = liner.get_vertical_line()
            h_line = liner.get_horizontal_line()

            cv2.line(clone, (v_line[0], v_line[1]), (v_line[2], v_line[3]), (0, 0, 255), 1)
            cv2.line(clone, (h_line[0], h_line[1]), (h_line[2], h_line[3]), (0, 0, 255), 1)
        
        box_list = box_info.get_all_boxes()

        for obj in obj_names:
            for b in box_list[obj]:                
                cv2.rectangle(clone, (b[0], b[1]), (b[2], b[3]), get_color_bgr(color_names[obj]), 1)

        cv2.imshow(ws_name, clone)
        key = cv2.waitKey(1) & 0xff
        
        if key == ESC:  
            break

        elif key == NEXT:
            if img_idx + 1 < img_len:
                img_idx += 1
        
        elif key == PREV:
            if img_idx - 1 >= 0:
                img_idx -= 1

        elif key == SPACE_BAR:
            obj_idx = (obj_idx+1)%len(obj_names)
            obj_name = obj_names[obj_idx]
            print('Current object name: {}'.format(obj_name))
        
        elif key == BACK_SPACE:
            print(obj_name)
            box_info.remove_box(obj_name)

        elif key == ord('n'):
            print(image_name)
        
        elif key == ENTER:
            write_boxes(image_name, '/temp/path/'+image_name, box_dir_path, img_w, img_h, 3, 'train')

    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', required=False, default=False, help='input type')
    parser.add_argument('-i', '--image', required=False, default=False, help='input type')
    args = vars(parser.parse_args())
    init(args)
    run()