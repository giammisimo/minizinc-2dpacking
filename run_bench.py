import os
import sys
import platform

number_of_benchmarks = 36
MZN_FILE = sys.argv[1]

# MacOS or Linux
def check_operating_system():
    os_name = platform.system()
    if os_name == 'Darwin':
        return 'macos'
    elif os_name == 'Linux':
        return 'linux'
    else:
        return 'unsupported'
    
def read_mzn_file(mzn_file_path):
    # Works with benchmarks with the following pattern
    # k = [num1]; x = [num2];
    vars = {'k':None, 'x':None}
    with open(mzn_file_path) as f:
        s = f.read()
        exec(s, None, vars)
    return vars['k'], vars['x']

def can_continue(counter: int) -> bool:
    return counter < number_of_benchmarks


def main():
    benchmark_folder = './benchmarks'
    results_folder = './benchmarks-results'

    # Lista dei file nella directory
    files = os.listdir(benchmark_folder)

    # Ordinare i file
    ordered_benchmarks_files = sorted(files)
    
    counter = 0

    for file_name in ordered_benchmarks_files:  
        if not file_name.endswith(('.dzn','.mzn')):
            continue

        counter += 1

        if not can_continue(counter):
            break
        
        mzn_file_path = os.path.join(benchmark_folder, file_name)

        k, x = read_mzn_file(mzn_file_path)

        print(f'Running {mzn_file_path} with k = {k}, x = {x}, y = {x + 5}')      

        file_name_without_extension = file_name.split('.')[0]
        bench_path = f"{benchmark_folder}/{file_name}"
        
        if check_operating_system() == 'macos':
            os.system(f"minizinc --solver Gecode ./{MZN_FILE} {bench_path} --time-limit 300000 | tee ./benchmarks-results/{file_name_without_extension}.txt")
        elif check_operating_system() == 'linux':
            
            if MZN_IDE_DIR := os.getenv('MZN'):
                MINIZINC = os.path.join(MZN_IDE_DIR, 'bin', 'minizinc')
            else:
                MINIZINC = 'minizinc'

            os.system(f"{MINIZINC} --output-time --solver Gecode ./{MZN_FILE} {bench_path} --time-limit 300000 | tee ./benchmarks-results/{file_name_without_extension}.txt")
        else:
            print("Sistema operativo non supportato.")
            return
        


if __name__ == "__main__":
    main()
