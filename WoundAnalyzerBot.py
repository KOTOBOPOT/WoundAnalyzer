''' 
StyleTransferBot combines Telegram bot and Neural Network
'''
from bot import DialogBot
import photo_processing.files_proccessing as files_proccessing
import photo_processing.ImageProcessing as ImagesProcessing
import torch
from PIL import Image

import os
PATH_TO_MODEL = 'C:/Users/boris/OneDrive/Рабочий стол/1 учеба/ML/Deep Learning School 1-ый семестр/проект/wound analyses/model/UNet++_80Epoch_bceLoss_lr=0p0001_0p5+resSplit.pt'
class StyleTransferBot(DialogBot):
    USERS_WAY = files_proccessing.USERS_WAY
    RES_WAY= files_proccessing.RES_WAY

    def __init__(self, save_images = False):
        super().__init__(is_logging= True)
        self.__set_up_image_bot()
        self.SAVE_IMAGES = save_images
        self.Network = ImagesProcessing.ProcessImage(PATH_TO_MODEL)
        

    def __set_up_image_bot(self):
        bot = self.bot


        @bot.message_handler(commands=['pr'])
        def send_processing(message):
            user_id = str(self.get_user_id(message))
            bot.reply_to(message, "Send wound image to process....")
            bot.register_next_step_handler(message, get_image);
            



        def get_image(message):
            user_id = self.get_user_id(message)  
            if message.content_type == 'photo':
                raw = message.photo[-1].file_id  
                path = files_proccessing.create_user_folder(user_id) + "\\" + 'wound' + ".jpg"
                file_info = bot.get_file(raw)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(path, 'wb') as new_file:
                    new_file.write(downloaded_file)

                bot.send_message(message.from_user.id, f"Got image. Please wait...")  # message.photo)
                user_fileway = files_proccessing.get_user_fileway(user_id)
                self.Network.run(f'{user_fileway}\\wound.jpg', user_fileway)
                bot.send_photo(user_id, photo=open(files_proccessing.get_user_fileway(user_id) + '\\res.jpg', 'rb'))
                torch.cuda.empty_cache()
                res_image = Image.open(files_proccessing.USERS_WAY + f'{user_id}\\res.jpg')
                path = files_proccessing.create_res_folder()

                res_image.save(path + '\\res.jpg')
            elif message.text == '/cancel':
                bot.send_message(message.from_user.id, f"Canceling comand.")
                #self.update_parameter("waiting_parameter", "None", is_internal_config=True, user_id=user_id)
            else:
                bot.send_message(message.from_user.id,
                                 f"I cant read this Image or it's not image. Please send image(to cancel send /cancel )")
                bot.register_next_step_handler(message, get_image);    


        @bot.message_handler(content_types=['text'])
        def get_unknown_message(message):
            bot.reply_to(message, "Unknown message. See /help command")
if __name__ == '__main__':
    bot = StyleTransferBot()
    bot.start()
