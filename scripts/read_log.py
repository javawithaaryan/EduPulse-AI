try:
    with open('vision_debug.log', 'r') as f:
        print(f.read())
except Exception as e:
    print(e)
