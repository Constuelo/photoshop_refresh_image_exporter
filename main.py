from psd_tools import PSDImage
import os


"""
    Exports images from a photoshop file
"""
path = input('path:')  # directory path of the PSD
root_dir = path

psd = input('psd name:')
path_join = os.path.join(path, psd)
name_pattern = input('example == 2018-12-10_AW18_Ph3_R4_Homepage_ \n'
                     'naming convention: ')

psd_load = PSDImage.load(path_join)

""" make an images directory if it does not exist """
os.makedirs(root_dir + '\\images', exist_ok=True)

desktopArtboard, tabletArtboard, mobileArtboard = None, None, None

desktop = '1600'
tablet = '1200'
mobile = '768'

counter = []
remove_psd_list = []

""" gets specific desktop and mobile artboard """
for i in psd_load.layers:
    if 'DESKTOP'.lower() in i.name.lower():
        desktopArtboard = i
    if '1200'.lower() in i.name.lower():
        tabletArtboard = i
    if 'MOBILE'.lower() in i.name.lower():
        mobileArtboard = i


def recurse(p, size):
    """
        Loop recursively through the visible photoshop layers \
        For group containing the word 'image' \
        Writes out images inside an 'images' directory \
        For best quality use Pixel Layers or Smart Objects \
        note: Shape layers (vector) do not work correctly. \
    """
    try:
        for layer in p.layers:
            if layer.visible:
                try:
                    """
                        New In Blocks
                    """
                    if 'block'.lower() in layer.name.lower():
                        for group in layer.layers:
                            try:
                                for a in group.layers:
                                    if a.kind == 'smartobject':
                                        counter.append(group)  # Add 1 to counter
                                        layer = a.linked_data
                                        remove_psd_list.append(layer.filename)  # Add temp psd to list
                                        image = newPSD(layer)
                                        save_image(image, size)
                                        remove_file(layer.filename)

                            except AttributeError:
                                pass
                except:
                    pass

                try:
                    """
                        All other images
                    """
                    if 'image'.lower() in layer.name.lower():
                        if 'block'.lower() not in p.name:
                            try:
                                if layer.kind == 'group':
                                    counter.append(layer)
                                    image = layer.as_PIL()
                                    save_image(image, size)

                            except AttributeError:
                                pass
                except:
                    pass

                recurse(layer, size=size)

    except AttributeError:
        pass


def save_image(image, size):
    if len(counter) <= 9:  # 01.jpg
        image.save(f'{root_dir}\\images\\{name_pattern}{size}_0{str(len(counter))}.jpg')
    if len(counter) > 9:  # 10.jpg
        image.save(f'{root_dir}\\images\\{name_pattern}{size}_{str(len(counter))}.jpg')


def newPSD(layer):
    file_psd = root_dir + '\\' + layer.filename
    layer.save(file_psd)
    psd_load = PSDImage.load(file_psd)
    image = psd_load.as_PIL()
    return image


def remove_file(file):
    os.remove(root_dir + '\\' + file)


recurse(desktopArtboard, size=desktop)
counter = []
recurse(mobileArtboard, size=mobile)
counter = []
recurse(tabletArtboard, size=tablet)
