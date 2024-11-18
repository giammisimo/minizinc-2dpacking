for x in range(5,25,5):
    y = x + 5
    for k in range(20 - 1, 110 - 1, 10):
        output = f'k = {k}; x = {x}; y = {y};\n'
        with open(f'bench{k}-{x}.dzn','w') as file:
            file.write(output)