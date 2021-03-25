import numpy as np
import os

from image import Image
def brightness(image, factor): # (factor > 1 -> brightness goes up) (factor < 0 -> brightness goes down)
    x_pixels, y_pixels, num_channels = image.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = image.array[x, y, c] * factor

    # or vectorization can be used like: new_im.array = image.array * factor

    return new_im

def contrast(image, factor, mid = 0.5): # change contrast by factor value, and can take positive numbers
    x_pixels, y_pixels, num_channels = image.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image.array[x, y, c] - mid) * factor + mid
    
    return new_im
    # or vectorization can be used like: new_im.array = (image.array-mid) * factor + mid

def blur(image, factor): # factor between 0 and 25 preferable
    x_pixels, y_pixels, num_channels = image.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    rg = factor // 2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                sum = 0
                for x_i in range(max(0, x - rg), min(x_pixels - 1, x + rg) + 1):
                    for y_i in range(max(0, y - rg), min(y_pixels - 1, y + rg) + 1):
                        sum += image.array[x_i, y_i, c]
                new_im.array[x, y, c] = sum / (factor ** 2)
    return new_im

def highlight(image, highlight):
    x_pixels, y_pixels, num_channels = image.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    highlight_size = highlight.shape[0]
    rg = highlight_size // 2

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                sum = 0
                for x_i in range(max(0, x - rg), min(x_pixels - 1, x + rg) + 1):
                    for y_i in range(max(0, y - rg), min(y_pixels - 1, y + rg) + 1):
                        x_k = x_i + rg - x
                        y_k = y_i + rg - y
                        highlight_val = highlight[x_k, y_k]
                        sum += image.array[x_i, y_i, c] * highlight_val
                new_im.array[x, y, c] = sum

    return new_im

def merge(image1, image2): # images should have same resolution
    x_pixels, y_pixels, num_channels = image1.array.shape
    new_im = Image(x_pixels=x_pixels, y_pixels=y_pixels, num_channels=num_channels)

    for x in range(x_pixels):
        for y in range(y_pixels):
            for c in range(num_channels):
                new_im.array[x, y, c] = (image1.array[x, y, c] ** 2 + image2.array[x, y, c] ** 2) ** 0.5
    
    return new_im

if __name__ == '__main__':

    operations = ['(1)brightness', '(2)contrast', '(3)blur', '(4)highlight', '(5)merge']
    path = os.getcwd()
    input_path = path + '/input'

    while True:
        print('Choose which operation you want to perform with Photoshop:')
        for i in operations:
            print(i)

        edit_choice = input()
        init = os.listdir(input_path)[0]
        to_edit = Image(filename=init)
        to_edit_1 = Image(filename=init)
        to_edit_2 = Image(filename=init)

        if edit_choice == '1':
            print('Choose one of the following photos to edit:')
            cur = 0
            with os.scandir(input_path) as entrylist:
                for entry in entrylist:
                    if entry.is_file():
                        cur = cur + 1
                        print('(' + str(cur) + ')' + entry.name)
            photo_choice = int(input())
            chosen_photo = ''
            ok = 0
            cur = 0
            with os.scandir(input_path) as entrylist:
                for entry in entrylist:
                    if entry.is_file():
                        cur = cur + 1
                        if cur == photo_choice:
                            to_edit = Image(filename=entry.name)
                            chosen_photo = entry.name
                            ok = 1
                            break
            if ok == 0:
                break

            print('Enter factor to adjust brightness( > 1 for brighter, < 1 for darker)')
            new_factor = float(input())
            result = brightness(to_edit, new_factor)
            if(new_factor > 1.0):
                result.write_image('brightened_' + chosen_photo)
                print('Your edited photo is in output folder with name: brightned_' + chosen_photo)
            else:
                result.write_image('darkened_' + chosen_photo)
                print('Your edited photo is in output folder with name: darkened_' + chosen_photo)
        
        elif edit_choice == '2':
            print('Choose one of the following photos to edit:')
            cur = 0
            with os.scandir(input_path) as entrylist:
                for entry in entrylist:
                    if entry.is_file():
                        cur = cur + 1
                        print('(' + str(cur) + ')' + entry.name)
            photo_choice = int(input())
            chosen_photo = ''
            ok = 0
            cur = 0
            with os.scandir(input_path) as entrylist:
                for entry in entrylist:
                    if entry.is_file():
                        cur = cur + 1
                        if cur == photo_choice:
                            to_edit = Image(filename=entry.name)
                            chosen_photo = entry.name
                            ok = 1
                            break
            if ok == 0:
                break
            
            print('Enter factor to adjust contrast:')
            new_factor = float(input())
            result = contrast(to_edit, new_factor)
            result.write_image('contrast_' + chosen_photo)
            print('Your edited photo is in output folder with name: contrast_' + chosen_photo)
        
        elif edit_choice == '3':
            print('Choose one of the following photos to edit:')
            cur = 0
            with os.scandir(input_path) as entrylist:
                for entry in entrylist:
                    if entry.is_file():
                        cur = cur + 1
                        print('(' + str(cur) + ')' + entry.name)
            photo_choice = int(input())
            chosen_photo = ''
            ok = 0
            cur = 0
            with os.scandir(input_path) as entrylist:
                for entry in entrylist:
                    if entry.is_file():
                        cur = cur + 1
                        if cur == photo_choice:
                            to_edit = Image(filename=entry.name)
                            chosen_photo = entry.name
                            ok = 1
                            break
            if ok == 0:
                break
            
            print('Enter factor to blur(between 0 and 25 is preferable):')
            new_factor = int(input())
            result = blur(to_edit, new_factor)
            result.write_image('blured_' + chosen_photo)
            print('Your edited photo is in output folder with name: blurred_' + chosen_photo)
        
        elif edit_choice == '4':
            print('Choose one of the following photos to edit:')
            cur = 0
            with os.scandir(input_path) as entrylist:
                for entry in entrylist:
                    if entry.is_file():
                        cur = cur + 1
                        print('(' + str(cur) + ')' + entry.name)
            photo_choice = int(input())
            chosen_photo = ''
            ok = 0
            cur = 0
            with os.scandir(input_path) as entrylist:
                for entry in entrylist:
                    if entry.is_file():
                        cur = cur + 1
                        if cur == photo_choice:
                            to_edit = Image(filename=entry.name)
                            chosen_photo = entry.name
                            ok = 1
                            break
            if ok == 0:
                break
            
            for_x = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]) # x edge detection filter
            for_y = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]) # y edge detection filter
            res_x = highlight(to_edit, for_x)
            res_x.write_image('highlighted_x_' + chosen_photo)
            res_y = highlight(to_edit, for_y)
            res_y.write_image('highlighted_y_' + chosen_photo)
            result = merge(res_x, res_y)
            result.write_image('highlighted_' + chosen_photo)
            print('Your edited photo is in output folder with name: highlighted_' + chosen_photo)
        
        elif edit_choice == '5':
            print('Choose two of the following photos to merge(resolutions should match):')
            cur = 0
            with os.scandir(input_path) as entrylist:
                for entry in entrylist:
                    if entry.is_file():
                        cur = cur + 1
                        print('(' + str(cur) + ')' + entry.name)
            photo_choice_1, photo_choice_2 = [int(photo_choice_1) for photo_choice_1 in input("Enter two value: ").split()]
            chosen_photo_1 = ''
            chosen_photo_2 = ''
            ok_1 = 0
            cur = 0
            with os.scandir(input_path) as entrylist:
                for entry in entrylist:
                    if entry.is_file():
                        cur = cur + 1
                        if cur == photo_choice_1:
                            to_edit_1 = Image(filename=entry.name)
                            chosen_photo_1 = entry.name
                            ok_1 = 1
                            break
            ok_2 = 0
            cur = 0
            with os.scandir(input_path) as entrylist:
                for entry in entrylist:
                    if entry.is_file():
                        cur = cur + 1
                        if cur == photo_choice_2:
                            to_edit_2 = Image(filename=entry.name)
                            chosen_photo_2 = entry.name
                            ok_2 = 1
                            break
            if ok_1 == 0 or ok_2 == 0:
                break
            
            result = merge(to_edit_1, to_edit_2)
            result.write_image('merged_photo.png')
            print('Your merged photo is in output folder with name: merged_photo.png')