from air import BlockAir

blocks = [
BlockAir
]

items = [

]

def fromid(id):
    for block in blocks:
        if block.id == id:
            return block

    for item in items:
        if item.id == id:
            return item

    return None

def fromname(name):
    for block in blocks:
        if block.name == name:
            return block

    for item in items:
        if item.name == name:
            return item

    return None
