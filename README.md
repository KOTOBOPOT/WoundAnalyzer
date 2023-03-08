# Wound Analyzer
This repository contains Telegram Bot which analyze wound image for different tissue types.

# WARNING
Several repository images(for example below in README.md) can shock. If you are impressionable person, authors don't recommend you to see this repository

## Neural Network
The topic of the study was the segmentation of medical images, namely the segmentation of wounds and other similar tissue lesions. The article "Fully automatic wound segmentation with deep convolutional neural network" was used as materials, available at the link below:<br /> https://www.nature.com/articles/s41598-020-78799-w
<br />

The dataset attached to the article (currently the repository of the project article on github is not available) contained 1009 images of foot tissue lesions and segmentation markup to them. Since the goal of the project is to create a model capable of segmenting tissues in the wound itself, it was decided to follow the example of the article by first training a model capable of segmenting the site of the skin lesion itself, and then use it to remove everything from the picture that is not a wound in order to improve the quality of the second model that produces segmentation the tissues are already inside the wound itself (in the article, the wound is first detected, after which the image is cropped by the bounding box and fed to the input of the second neural network performing segmentation)

<br />
UNet++ was chosen as the architecture of the first model because the article "UNet++: A Nested U-Net Architecture for Medical Image Segmentation" talks about the advantages of this modernization of the UNet architecture for segmentation of medical images. The article is available at the link: https://arxiv.org/pdf/1807.10165.pdf
<br />
<br />
The UNet++ model was trained on an available dataset with the following loss functions, after which one of the models was trained on a dataset that underwent augmentation, expanding it to 5500+ images. The results of the training are presented below:
<br />
<br />


![alt tag](https://github.com/KOTOBOPOT/WoundAnalyzer/blob/main/photos/graphics/UNET%2B%2Bdice.png)

![alt tag](https://github.com/KOTOBOPOT/WoundAnalyzer/blob/main/photos/graphics/UNET%2B%2Bbce.png)

![alt tag](https://github.com/KOTOBOPOT/WoundAnalyzer/blob/main/photos/graphics/UNET%2B%2Bbce%2Baug.png)

![alt tag](https://github.com/KOTOBOPOT/WoundAnalyzer/blob/main/photos/graphics/UNET%2B%2Blosses_IOU.png)

<br />
Augmentation gives a great advantage: IOU increases at any stage and the training itself becomes more stable
<br />

Due to the limited computing power, it was not possible to conduct a large number of experiments using the selected dataset. As a result, a model capable of segmenting images of wounds with an accuracy of 0.83 IOU was obtained. It is used to make examples.
<br />

It should be mentioned that the model does not cope well with the segmentation of wounds on parts of the body other than the feet, since the training took place on an open dataset of wounds and foot ulcers. To improve the quality of the model, you should get a marked dataset with wounds on other parts of the body and retrain the model.
<br />

In the future, it is planned to use the model created now for segmentation of tissues in the wound itself. The initial stage of the solution will be the segmentation of the wound itself in order to simplify the work for the neural network, which will be created and trained later. The initial segmentation of the lesion site itself with the help of a trained model is necessary, since some types of tissues that may be present in the wound are also found on unaffected skin that can get into the frame. Also, traces of blood on clothes or a cot, which also sometimes appear in the frame, can be mistakenly classified by the second neural network as tissue in the wound, so you should initially clear the images of such "noises" that will interfere with the work of the second neural network, the development of which we plan to begin in the near future.
<br />
### Segmentation example
![alt tag](https://github.com/KOTOBOPOT/WoundAnalyzer/blob/main/photos/example/foots_ex.png)

## Bot
Bot released by python module telebot

## Telegram Commands:
/pr - Get image and send result of processing<br />
/cancel - Cancel current command<br />
/help - Get info about bot<br />

## Using Example
![alt tag](https://github.com/KOTOBOPOT/WoundAnalyzer/blob/main/photos/bot%20using%20example/example.jpg)


## Install
To run this bot on your own you need:
1. Copy this repository where you want to run bot
2. Create file 'token.ini' contained bot token
3. Run 'WoundAnalyzerBot.py'

## Authors
Tsupin Dmitry dimatsypin@gmail.com (ML) 
<br />
Pronin Dmitry DDPronin003@yandex.ru (ML)
<br />
Borisov Viktor borisov_vk@mail.ru (ML)
<br />
Brezhnev Danila Stalkee97@gmail.com (Med)
<br />


