import argparse
import subprocess
import time

TIMER_INT = 0.1
TIME_LIMIT = 300000
SOLVER = 'chuffed'
OUT_DIR = './benchmarks-results'
    
def main(mzn_model: str, solver: str, time_limit: int, out_dir: str):
    X = [5, 10, 15, 20]
    K = [a - 1 for a in range(20, 101, 10)]
    counter = 0

    for k in K:
        # This variable is used to track time outs for the same pallet
        # Once a box size times out, all smaller sizes will time out as well
        # (the problem gets harder)
        timed_out = False

        for x in X[::-1]:
            counter += 1
            if timed_out:
                print(f'Test {counter} skipped - pallet timed out')
                continue
            y = x + 5
            print(f'Test {counter}: k = {k}, x = {x}, y = {y}') 

            file_name = f'bench{k}-{x}'

            command = f"""minizinc --solver {solver} {mzn_model}  \
--cmdline-data "x = {x}" --cmdline-data "y = {y}" --cmdline-data "k = {k}" \
--output-time --time-limit {time_limit} > \
{out_dir}/{file_name}.txt"""
            
            #print(command)

            start_time = time.time()
            process = subprocess.Popen(command, stderr=subprocess.DEVNULL, shell=True)

            while process.poll() is None:
                elapsed_time = time.time() - start_time
                print(f"[time] {elapsed_time:.2f} s", end='\r')
                time.sleep(TIMER_INT)
            process.wait()
            if elapsed_time > (time_limit / 1000):
                timed_out = True

            with open(f'{out_dir}/{file_name}.txt','r') as file:
                print(file.read() + '\n\n')
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run benchmarks for 2D Packing Minizinc model"
    )
    parser.add_argument(
        "model",
        metavar="<model>.mzn",
        type=str, 
        help="Path to the minizinc model to test (.mzn file)"
    )
    parser.add_argument(
        "-s", "--solver", 
        type=str, 
        default=SOLVER, 
        help=f"Model solver (default: {SOLVER})"
    )
    parser.add_argument(
        "-t", "--time-limit", 
        type=int, 
        default=TIME_LIMIT, 
        help=f"Single test Time limit in milliseconds (default: {TIME_LIMIT})"
    )
    parser.add_argument(
        "-d", "--out-dir", 
        type=str, 
        default=OUT_DIR, 
        help=f"Output directory for results (default: {OUT_DIR})"
    )
    args = parser.parse_args()
    main(args.model, args.solver, args.time_limit, args.out_dir)
