import os, cv2

class Image():
    def __init__(self, in_dir_path, out_dir_path):
        print('Init image loader')
        self.in_dir_path = in_dir_path
        self.out_dir_path = out_dir_path
        self.load_images()

    def load_images(self):
        self.image_names = os.listdir(self.in_dir_path)
        self.image_names.sort()
    
    def get_image(self, idx):
        return cv2.imread('{0}/{1}'.format(self.in_dir_path, self.image_names[idx]))
    
    def get_file_length(self):
        return len(self.image_names)
