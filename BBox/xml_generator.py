import xml.etree.ElementTree as ET

class XML_Generator:
    def __init__(self):
        print('Init xml generator')

    def write(self, file_name, file_path, img_w, img_h, img_c, box_list, obj_names, data_type='train'):
        root = ET.Element('annotation')
        ET.SubElement(root, 'folder').text = str(data_type)
        ET.SubElement(root, 'filename').text = str(file_name)
        ET.SubElement(root, 'path').text = str(file_path)

        source = ET.SubElement(root, 'source')
        ET.SubElement(source, 'database').text = 'Unknown'

        size = ET.SubElement(root, 'size')
        ET.SubElement(size, 'width').text = str(img_w)
        ET.SubElement(size, 'height').text = str(img_h)
        ET.SubElement(size, 'depth').text = str(img_c)
        ET.SubElement(root, 'segmented').text = str(0)

        for obj_name in obj_names:
            for box in box_list[obj_name]:
                obj = ET.SubElement(root, 'object')
                ET.SubElement(obj, 'name').text = str(obj_name)
                ET.SubElement(obj, 'pose').text = 'Unspecified'
                ET.SubElement(obj, 'truncated').text = str(0)
                ET.SubElement(obj, 'difficult').text = str(0)

                bndbox = ET.SubElement(obj, 'bndbox')
                ET.SubElement(bndbox, 'xmin').text = str(box[0])
                ET.SubElement(bndbox, 'ymin').text = str(box[1])
                ET.SubElement(bndbox, 'xmax').text = str(box[2])
                ET.SubElement(bndbox, 'ymax').text = str(box[3])

        tree = ET.ElementTree(root)
        tree.write(file_name[:-4] + '.xml')
        print('Write')

    def update(self, file_name, _tag, context):
        tree = ET.ElementTree(file=file_name)
        for elem in tree.iter(tag=_tag):
            elem.text = str(context)

