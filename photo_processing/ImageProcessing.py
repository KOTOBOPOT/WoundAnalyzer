'''
ImagesProcessing - provides neural network thats combine style and content image. Neural network is got from pytorch.org
'''
from  PIL import Image
from torchvision.transforms.functional import to_pil_image, pil_to_tensor
from torchvision import transforms
import torch
import numpy as np
import cv2
from matplotlib import pyplot as plt
from torchvision.utils import save_image
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


#import model
from photo_processing.model import Nested_UNet

class ProcessImage:
    

    def __init__(self, PATH_TO_MODEL):
        self.model = Nested_UNet()
        self.model.load_state_dict(torch.load(PATH_TO_MODEL,map_location = device))
        self.model.to(device);
        self.model.eval();
    
    def run(self, img_fileway, way_to_save=''):
        loader = transforms.Compose([
            transforms.Resize((256,256)),  # scale imported image
            transforms.ToTensor()])  # transform it into a torch tensor
        orig = Image.open(img_fileway)
        orig_t = loader(orig).reshape(1,3,256,256).type(torch.FloatTensor)
        orig_np = orig_t.numpy()

        orig_t_copy = orig_t
        orig_t = orig_t.to(device)

        result = self.model.forward(orig_t)
        result = torch.relu(result)
        
        #Res is mask for original image to get only wound from image
        res = result.cpu().detach().numpy().reshape(256,256,1)
        res = np.clip(res,0,1)
        res[res>=0.5] = 1
        res[res<0.5] = 0
        
        masked_on = np.multiply(orig_np.reshape(3,256,256),np.concatenate((res.reshape(1,256,256),res.reshape(1,256,256),res.reshape(1,256,256)), axis = 0))
        
        wound_image = Image.fromarray(torch.from_numpy(masked_on*255).permute(1, 2,0).numpy().astype('uint8'), 'RGB')#torch.from_numpy(masked_on).permute(1, 2, 0)#Original image with wound mask
         
        wound_image.save(way_to_save + '\\res.jpg')
#        save_image(wound_image, way_to_save + '/res.jpg')
if __name__ == '__main__':
    pr_im = ProcessImage('C:/Users/boris/OneDrive/Рабочий стол/1 учеба/ML/Deep Learning School 1-ый семестр/проект/wound analyses/model/UNet++_80Epoch_bceLoss_lr=0p0001_0p5+resSplit.pt')
    wound_fileway = 'C:/Users/boris/OneDrive/Рабочий стол/1 учеба/ML/Deep Learning School 1-ый семестр/проект/wound analyses/tests/играемся/pics/Проба база.jpg'#"<fileway to .jpg image>"

    print('Starting calcs')
    
    pr_im.run(wound_fileway)
    torch.cuda.empty_cache()
    print('End of calcs')