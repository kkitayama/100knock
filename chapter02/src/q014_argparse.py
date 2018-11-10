
import argparse

def main():
    with open(args.data_path, 'r') as f:
        for i, line in enumerate(f):
            if i == args.lines:
                break
            print(line, end='')
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog='q014_argparse', 
                        usage='Print the first N lines of a file.', 
                        description='description', 
                        epilog='end', 
                        add_help=True,
                        )
    
    parser.add_argument('data_path')
    parser.add_argument('-N', '--lines',
                                           type=int,
                                           default=5)
    
    args = parser.parse_args()
    
    main()