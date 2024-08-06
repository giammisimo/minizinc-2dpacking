import os
import subprocess

number_of_benchmarks = 2

def can_continue(counter: int) -> bool:
    if counter >= number_of_benchmarks:
        return False
    return True

def read_mzn_file(mzn_file_path):
    # Dentro sono fatti così
    # l = [0,0]; u = [19,19];
    # box_size = [5,10];

    l = None
    u = None
    box_size = None

    with open(mzn_file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'l = ' in line:
                l = [int(x) for x in line.split('[')[1].split(']')[0].split(',')]
            elif 'u = ' in line:
                u = [int(x) for x in line.split('[')[1].split(']')[0].split(',')]
            elif 'box_size = ' in line:
                box_size = [int(x) for x in line.split('[')[1].split(']')[0].split(',')]

    return l, u, box_size


def main():
    benchmark_folder = './benchmarks'
    results_folder = './benchmarks-results'

    # Lista dei file nella directory
    files = os.listdir(benchmark_folder)

    # Ordinare i file
    ordered_benchmarks_files = sorted(files)
    
    counter = 0

    for file_name in ordered_benchmarks_files:  
        if not file_name.endswith('.mzn'):
            continue

        counter += 1

        if not can_continue(counter):
            break
        
        mzn_file_path = os.path.join(benchmark_folder, file_name)

        l, u, box_size = read_mzn_file(mzn_file_path)

        print(f'Running {mzn_file_path} with l={l}, u={u}, box_size={box_size}')

        # Creo il file temp tem.mzn, 

        # %This file is used as a known example for testing
        # %boxes = 4 , n = 7
        # u = 19;
        # x = 5; dove x è il primo elemento di box_size

        with open('temp.mzn', 'w') as f:
            f.write(f'%This file is used as a known example for testing\n')
            f.write(f'%boxes = 4 , n = 7\n')
            f.write(f'k = {u[0]};\n')
            f.write(f'x = {box_size[0]};\n')
        

        # Eseguo il comando bash

        file_name_without_extension = file_name.split('.')[0]
        os.system(f"minizinc --solver Gecode ./2dpacking_intervals.mzn temp.mzn | tee ./benchmarks-results/{file_name_without_extension}.txt")

        


if __name__ == "__main__":
    main()
