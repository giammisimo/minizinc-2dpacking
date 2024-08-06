for x in range(5,25,5):
    y = x + 5
    for k in range(20 - 1, 110 - 1, 10):
        output = f'l = [0,0]; \nu = [{k},{k}];\n'
        output += f'box_size = [{x},{y}];'
        with open(f'pallet_{k}-box_{x}.mzn','w') as file:
            file.write(output)