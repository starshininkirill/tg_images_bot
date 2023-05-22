from telebot import TeleBot
from PIL import Image, ImageChops

token = '6229389421:AAEgn0UhQ5ehVrYmoeuWvffBrPNnfCYRpzk'

bot = TeleBot(token)


def download_photo(message, type):
    if type == 'document':
        file_id = message.document.thumb.file_id
    elif type == 'photo':
        file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    photo_extension = file_info.file_path.split('.')[-1]
    photo_full_name = f'{message.chat.id}.{photo_extension}'
    src = f'images/upload/{photo_full_name}'
    try:
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        return photo_full_name
    except Exception:
        return False


def reformat_image(image_name, user_id, rum_number):
    main_image = Image.open(f'images/upload/{image_name}')
    background_image = Image.open(f'images/sourse/ram_{rum_number}.png').resize(main_image.size)

    mask_im = Image.open(f'images/sourse/ram_{rum_number}.png').resize(main_image.size)
    mask_im = ImageChops.invert(mask_im)

    mask_im.save(f'images/reformat/masks/mask_{user_id}.png')

    background_image.paste(main_image, (0, 0), mask_im)
    result_photo_name = f'images/reformat/results/photo_{user_id}.png'
    background_image.save(result_photo_name)
    return result_photo_name