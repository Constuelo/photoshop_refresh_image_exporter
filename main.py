from psd_tools import PSDImage
import os
from tqdm import tqdm
"""
    Exports images from a photoshop file
"""
BLUE, END = '\33[94m', '\033[0m'

intro_text = 'PSD images must be in a folder called strictly Image or image\n' \
         'New in images must be in a folder containing the work block\n'
print(intro_text)

path = input('file path:')
root_dir = path

psd = input('psd name:')
path_join = os.path.join(path, psd)
name_pattern = input('example == 2019-01-21_SS19_Ph1_R3_Homepage_UK\n'
                     'naming convention:')

print(f'\nLoading {{}}{psd}{{}}'.format(BLUE, END))
psd_load = PSDImage.load(path_join)
print(f'Finished loading {{}}{psd}{{}}\n'.format(BLUE, END))

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
                                        image = new_psd(layer)
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
                    if 'image'.lower() == layer.name.lower():
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
    """ Save image if counter length is less than 9 """
    if len(counter) <= 9:
        image.save(f'{root_dir}\\images\\{name_pattern}{size}_0{str(len(counter))}.jpg')

    """ Save image if counter length is greater than 9 """
    if len(counter) > 9:
        image.save(f'{root_dir}\\images\\{name_pattern}{size}_{str(len(counter))}.jpg')


def new_psd(layer):
    file_psd = root_dir + '\\' + layer.filename
    layer.save(file_psd)
    load = PSDImage.load(file_psd)
    image = load.as_PIL()
    return image


def remove_file(file):
    os.remove(root_dir + '\\' + file)


def clear_list(f):
    return f.clear()


recurse(desktopArtboard, size=desktop)
print('Finished desktop images.')
clear_list(counter)
recurse(mobileArtboard, size=mobile)
print('Finished mobile images.')
clear_list(counter)
recurse(tabletArtboard, size=tablet)
print('Finished tablet images.')
