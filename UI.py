KV = """
ScreenManager:
    id: screen_manager
    MainScreen:
    PreviewScreen:

<MainScreen>:
    name: 'main_screen'
    FloatLayout:
        spacing: 8
        ScrollView:
            size_hint: 1, 1
            pos_hint: {'x': 0, 'y': 0}
        MDToolbar:
            id: toolbar
            title: 'Image AI'
            left_action_items: [["menu", lambda x: menu.set_state('toggle')]]
            pos_hint: {'top': 1}
            elevation: 8
        MDLabel:
            text: 'Select images to upload'
            size_hint_y: None
            pos_hint: {'top': 0.9}
            font_style: 'H5'
            halign: 'center'
            font_name: 'Poppins-Medium'
            underline: True
        MDRectangleFlatButton:
            text: 'Select Images'
            pos_hint: {'top': 0.74, 'center_x': 0.255}
            font_name: 'Poppins-Medium'
            size_hint_x: 0.43
            on_release: app.upload(list)
        MDRectangleFlatButton:
            text: 'Clear Selection'
            pos_hint: {'top': 0.74, 'center_x': 0.745}
            font_name: 'Poppins-Medium'
            size_hint_x: 0.43
            on_release: app.clear(list)
        BoxLayout:
            orientation: 'vertical'
            pos_hint: {'center_y': 0.4}
            padding: 10, 10
            size_hint_y: 0.55
            ScrollView:
                MDList:
                    id: list
                    padding: 15
                    pos_hint: {'center_y': 0.6}

            MDRectangleFlatButton:
                id: process_button
                text: 'Process'
                size_hint_y: None
                size_hint_x: 0.6
                pos_hint: {'center_x': 0.5, 'center_y': 0.8}
                font_name: 'Poppins-Medium'
                on_release: app.predict_inp(process_button, error_label)
                disabled: False
            MDLabel:
                id: error_label
                size_hint_y: None
                text: ""
                halign: 'center'
                font_name: 'Poppins-Italic'
                theme_text_color: 'Error'
            

    MDNavigationDrawer:
        id: menu
        BoxLayout:
            orientation: 'vertical'
            padding: 10
            spacing: 30
            Image:
                source: 'logo.png'
                pos_hint: {'center_y': 0.1}
            
            MDLabel:
                text: 'Go farther with Image.'
                size_hint_y: None
                height: self.texture_size[1]
                font_name: 'FontsFree-Net-Magilio'
                font_size: '35'
                line_height: 1.4
                halign: 'center'
            ScrollView:

<PreviewScreen>:
    name: 'preview_screen'
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            id: toolbar
            title: 'Image AI'
            left_action_items: [["arrow-left", lambda x: app.switch_screen('main_screen', 'right')]]
            pos_hint: {'top': 1}
            elevation: 8
        MDLabel:
            size_hint_y: None
            padding : 10, 10
            text: "The best image is: "
            font_style: 'H5'
            halign: 'center'
            font_name: 'Poppins-Italic'
            theme_text_color: 'Primary'
            underline: True
        Image:
            id: result_image
            source: "C:/Users/TANMO/Desktop/IMG_20211102_165512.jpg"
        MDLabel:
            id: result_text
            size_hint_y: None
            padding : 10, 10
            text: "The predicted rating of the image is: 7.89"
            font_style: 'H6'
            halign: 'center'
            font_name: 'Poppins-Italic'
            theme_text_color: 'Secondary'  
        
        ScrollView:
"""