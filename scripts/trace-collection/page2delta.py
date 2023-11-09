prev_page_addr = None

with open("page.txt", "r") as f_in, open("delta.txt", "w") as f_out:
    for line in f_in:
        elements = line.split()
        pc = int(elements[0], 16)
        page_addr = int(elements[1], 16)
        if prev_page_addr is not None:
            # To convert to page deltas subsequent addresses need to be divided by 4096.
            # Otherwise going from 1 page to the other will show up as +4096
            delta = (page_addr - prev_page_addr)//4096
            if delta == 0:
                continue
            f_out.write(f"{hex(pc)} {delta}\n")
        else:
            f_out.write(f"{hex(pc)} {0}\n")

        prev_page_addr = page_addr
