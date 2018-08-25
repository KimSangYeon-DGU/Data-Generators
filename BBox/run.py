import os, cv2, argparse
import image_loader

def init(args):
    global img_dir_path, box_dir_path, mode, loader
    print('init')

    datasets_path = './datasets/'

    img_dir_path = datasets_path + 'images/'
    box_dir_path = datasets_path + 'boxes/'
    if args['video'] == 'True':
        mode = 'video'
    elif args['image'] == 'True':
        mode = 'image'
        loader = image_loader.Image(img_dir_path, box_dir_path)

def run():
    global mode, loader
    print('Run')
    cur_img_idx = 0
    image = loader.get_image(cur_img_idx)
    cv2.imwrite('test.png', image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', required=False, default=False, help='input type')
    parser.add_argument('-i', '--image', required=False, default=False, help='input type')
    args = vars(parser.parse_args())
    init(args)
    run()