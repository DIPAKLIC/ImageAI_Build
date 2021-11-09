from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget
from UI import KV
from plyer import filechooser
import argparse
import torch
import torchvision.models
import torchvision.transforms as transforms
import os
from PIL import Image
import threading

device = 'cpu'
files = []
cur_dir = os.getcwd()
widgets = []
address = []
val = []


class App(MDApp):

    def build(self):
        self.root = Builder.load_string(KV)

    def upload(self, widget):
        if len(widgets) > 1:
            widgets[1].text = ""
        raw_path = filechooser.open_file(title="Select Images",
                                         filters=[("Images", "*.png", "*.jpg", "*.jpeg", "*.bmp", "*.dip")],
                                         multiple=True)
        count = 0
        for _ in raw_path:
            image = ImageLeftWidget(source=raw_path[count])
            item = OneLineAvatarListItem(text=raw_path[count])
            item.add_widget(image)
            widget.add_widget(item)
            files.append(raw_path[count])
            count += 1

    def clear(self, widget):
        widget.clear_widgets()
        files.clear()
        val.clear()
        address.clear()

    def predict_inp(self, button, label):
        widgets.clear()
        widgets.append(button)
        widgets.append(label)
        if len(files) > 0:
            t1 = threading.Thread(target=self.predict)
            button.disabled = True
            button.text = 'Processing'
            widgets[1].theme_text_color = 'Secondary'
            widgets[
                1].text = "Please wait for the program to predict, It might take a while depending on this device's " \
                          "performance "
            t1.start()
        else:

            label.theme_text_color = 'Error'
            label.text = "Please select atleast one image"

    def reset(self):
        widgets[0].disabled = False
        widgets[0].text = 'Process'
        widgets[1].text = ''
        self.switch_screen('preview_screen', 'left')

    def switch_screen(self, screen, dir):
        self.root.transition.direction = dir
        self.root.current = screen

    def prepare_image(self, image):
        if image.mode != 'RGB':
            image = image.convert("RGB")
        transform = transforms.Compose([
            transforms.Resize([224, 224]),
            transforms.ToTensor(),
        ])
        image = transform(image)
        image = image.unsqueeze(0)
        return image.to(device)

    def predict_main(self, image, model, item):
        image = self.prepare_image(image)
        with torch.no_grad():
            preds = model(image)
        local_value = '%.2f' % preds.item()
        address.append(item)
        val.append(local_value)

    def predict(self):
        print("Please wait for the program to predict, It might take a while depending on the device's performance")
        for item in files:
            os.chdir(cur_dir)
            model_dir = os.path.join(cur_dir, 'model/model-resnet50.pth')
            parser = argparse.ArgumentParser()
            parser.add_argument('--image_path', type=str, default=item)
            config = parser.parse_args()
            image = Image.open(config.image_path)
            model = torchvision.models.resnet50()
            model.fc = torch.nn.Linear(in_features=2048, out_features=1)
            model.load_state_dict(torch.load(model_dir, map_location=device))
            model.eval().to(device)
            self.predict_main(image, model, item)
        max_val = max(val)
        index = val.index(max_val)
        location = address[index]
        print('The best image is ' + '"' + location + '"' + ' with a predicted rating of ' + max_val)
        self.root.get_screen("preview_screen").ids["result_image"].source = location
        self.root.get_screen("preview_screen").ids["result_text"].text = "The predicted rating of the image is: "+ max_val
        self.reset()


class MainScreen(Screen):
    pass


class PreviewScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MainScreen(name='main_screen'))
App().run()
