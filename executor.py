import sys
import subprocess

def execute_python_code(code):
    result = subprocess.run(['python3', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

if __name__ == '__main__':
    code = sys.argv[1]
    stdout, stderr = execute_python_code(code)
    print(stdout)
    if stderr:
        sys.stderr.write(stderr)                                                                                              
                                                                                                
                                                                                                
                                                                                                
                                                                                                
                                                                                                
                                                                                                
                                                                                                
                                                                                                
                                                                                                
