from psd_tools import PSDImage
import os
from pathlib import Path
"""
    Exports images from a photoshop file
"""
BLUE, END = '\33[94m', '\033[0m'

intro_text = 'PSD images must be in a folder called strictly Image or image \n' \
             'New in images must be in a folder containing the work block \n'
print(intro_text)

user_directory = input('file path:')

""" psd file name, does not need to include extension """
psd = input('PSD name:')

if psd:
    for file in os.listdir(user_directory):
        if psd in file:
            path_of_psd = Path(user_directory).joinpath(file)
            break

""" if input is none finds any psd file in directory """
if not psd:
    for file in os.listdir(user_directory):
        if '.psb' in file or '.psd' in file:
            path_of_psd = Path(user_directory).joinpath(file)
            break

if not path_of_psd:
    path_of_psd = Path(user_directory).joinpath(psd)

print('example == 2019-01-21_SS19_Ph1_R3_Homepage_UK \n')
name_pattern = input('naming convention:')

print(f'\nLoading {{}}{psd}{{}}'.format(BLUE, END))
psd_load = PSDImage.open(path_of_psd)
print(f'Finished loading {{}}{psd}{{}}\n'.format(BLUE, END))

""" make an images directory if it does not exist """
os.makedirs(Path(user_directory).joinpath('images'), exist_ok=True)

desktopArtboard, tabletArtboard, mobileArtboard = None, None, None

desktop = '1600'
tablet = '1200'
mobile = '768'

counter = []
remove_psd_list = []

""" gets specific desktop and mobile artboard """
for i in reversed(list(psd_load.descendants())):
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
        for layer in reversed(p):
            if layer.visible:
                try:
                    """
                        New In Blocks
                    """
                    if 'new in'.lower() in layer.name.lower():
                        try:
                            for a in reversed(list(layer.descendants())):
                                if a.kind == 'smartobject':
                                    counter.append(layer)  # Add 1 to counter
                                    layer = a.smart_object
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
                    if 'image'.lower() in layer.name.lower():
                        if 'new in'.lower() not in p.name.lower():
                            try:
                                if layer.kind == 'group':
                                    counter.append(layer)
                                    image = layer.compose()
                                    save_image(image, size)

                            except AttributeError:
                                pass
                except:
                    pass

                recurse(layer, size=size)

    except AttributeError:
        pass
    except TypeError:
        pass


def save_image(image, size):
    """ Save image if counter length is less than 9 """
    if len(counter) <= 9:
        image.convert('RGB').save(
            Path(user_directory).joinpath('images', f'{name_pattern}{size}_0{str(len(counter))}.jpg'), quality=85)

    """ Save image if counter length is greater than 9 """
    if len(counter) > 9:
        image.convert('RGB').save(
            Path(user_directory).joinpath('images', f'{name_pattern}{size}_{str(len(counter))}.jpg'), quality=85)


def new_psd(layer):
    file_psd = Path(user_directory).joinpath(layer.filename)
    layer.save(file_psd)
    load = PSDImage.open(file_psd)
    image = load.compose()
    return image


def remove_file(f):
    os.remove(Path(user_directory).joinpath(f))


def clear_list(f):
    return f.clear()


print('Starting desktop images...')
recurse(desktopArtboard, size=desktop)
clear_list(counter)
print('Starting mobile images...')
recurse(mobileArtboard, size=mobile)
clear_list(counter)
print('Starting tablet images...')
recurse(tabletArtboard, size=tablet)