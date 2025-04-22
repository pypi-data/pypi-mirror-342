from PIL import ImageGrab

bbox=(2560, 366, 2560+1920, 366+1080)
        
screenshot = ImageGrab.grab(bbox=bbox, all_screens=True)

screenshot = screenshot.convert('RGB')
screenshot.save("screenshot.png")