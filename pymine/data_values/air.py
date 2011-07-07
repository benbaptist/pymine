class BlockAir:
    id = 0x00 # 0
    name = "air"
    blocktype = 0x00
    state = 0x00
    size = [1, 1]
    fall = False
    luminance = 0
    resistance = [0, 0]
    minetool = 0x00
    stackable = 0

    def __init__(self):
        pass

    def action_use(self):
        pass

    def action_break(self):
        pass
