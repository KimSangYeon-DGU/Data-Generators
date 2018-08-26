import os, cv2, argparse
import image_loader
import prev_box, prev_line

def mouse_handler(event, x, y, flags, param):
    global PREV_BOX, PREV_LINE, PREV_BOX_DRAW, PREV_LINE_DRAW, boxer, liner, img_w, img_h
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
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
        print(x, y)
        PREV_BOX = False
        PREV_BOX_DRAW = False
        PREV_LINE = True
        PREV_LINE_DRAW = True
        liner.set_left_point(x, y)

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
    global img_dir_path, box_dir_path, mode, loader, ws_name, boxer, liner
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

def run():
    global mode, loader, ws_name, PREV_BOX, PREV_LINE, img_w, img_h, boxer, PREV_BOX_DRAW, PREV_LINE_DRAW
    print('Run')
    
    cv2.namedWindow(ws_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(ws_name, mouse_handler)
    img_idx = 0
    
    img_len = loader.get_file_length()
    ESC = 27
    NEXT = 83
    PREV = 81
    SPACE_BAR = 32
    BACK_SPACE = 8

    PREV_BOX = False
    PREV_LINE = True
    PREV_BOX_DRAW = False
    PREV_LINE_DRAW = False

    while True:
        image = loader.get_image(img_idx)
        img_h, img_w = image.shape[:2]
        clone = image.copy()
        
        if PREV_BOX_DRAW == True:
            box = boxer.get_box()
            cv2.rectangle(clone, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 1)

        elif PREV_LINE_DRAW == True:
            v_line = liner.get_vertical_line()
            h_line = liner.get_horizontal_line()

            cv2.line(clone, (v_line[0], v_line[1]), (v_line[2], v_line[3]), (0, 0, 255), 1)
            cv2.line(clone, (h_line[0], h_line[1]), (h_line[2], h_line[3]), (0, 0, 255), 1)
            
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

    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', required=False, default=False, help='input type')
    parser.add_argument('-i', '--image', required=False, default=False, help='input type')
    args = vars(parser.parse_args())
    init(args)
    run()