from kivy.uix.textinput import TextInput

class SayHello(TextInput):
    def build(self):
        self.window = GridLayout(cols=1, padding=10, spacing=10)
        
        return self.window
    
if __name__ == '__main__':
    SayHello().run()