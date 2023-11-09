memory_address="0x7ffc3c8160d8"

page_size = 4 * 1024 # 4KB

def convert_address_to_page(memory_address):
    page_number = memory_address / page_size
    offset = memory_address % page_size
    return page_number, offset

page_number, offset = convert_address_to_page(int(memory_address, 16)) 
print(hex(int(page_number)) + " " + hex(offset))
print(hex(int(memory_address, 16) & ~((1<<12) -1)))
