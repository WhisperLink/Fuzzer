# -*- coding: utf-8 -*-
import subprocess
import random
import string
import time
import os

def generate_random_string(max_length):
    length = random.randint(1, max_length)
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_args_and_string(max_length):
    # "-" 뒤에 하나의 문자만 오도록 설정
    option = '-' + random.choice(string.ascii_letters)
    value = generate_random_string(max_length)
    return option, value

def get_byte_data(filename): # 퍼징할 대상 선택
    f = open(filename, 'rb').read()
    return bytearray(f)

def bit_flipping_Mutator(filename, flips_ratio, num):
    # 파일의 바이트 데이터를 가져와 랜덤 값 수정 후 새로운 바이너리 생성
    byte_data = get_byte_data(filename)
    flips_count = int(len(byte_data) * flips_ratio) + 1
    flips_indices = random.sample(range(len(byte_data)), flips_count) # 중복 없이 인덱스 선택

    for index in flips_indices:
        byte_data[index] = random.getrandbits(8)

    onlyName = filename.split('/')
    newName = onlyName[-1]
    input_path = os.path.join("./tmp", f"id:{num:06}_{newName}")

    with open(input_path, "wb") as file:
        file.write(byte_data)

    os.chmod(input_path, 0o755)

    return input_path, flips_indices

def Worker(filename, flips_pro, max_length, num):
    option, value = generate_random_args_and_string(max_length)
    input_path, flips_indices = bit_flipping_Mutator(filename, flips_pro, num)
    command = f'{input_path} {option} {value}'
    result = subprocess.run(command, input=value.encode(), shell=True, capture_output=True)

    try:
        out = result.stdout.decode('utf-8') + result.stderr.decode('utf-8')
    except UnicodeDecodeError:
        out = result.stdout.decode('iso-8859-1') + result.stderr.decode('iso-8859-1')

    if("Segmentation" in out):
        print("Crash:", out)
        print("Command:", command)
        bit_flipping_Logger(input_path, option, value, flips_indices) # ./tmp/id:1234556_DogLang
    else:
        os.system(f"rm {input_path}")

def bit_flipping_Logger(filename, option, value, flips_indices):
    onlyName = filename.split('/')
    newName = f"{onlyName[-1]}_op:flipping"
    subprocess.run("mv {} ./crash/{}".format(filename, newName), shell=True, text=True) # crash가 발생하면 crash폴더에 실행 파일저장
    subprocess.run("echo 'value: {}\n\nindex: {}' > ./Logs/args:{}_{}".format(value, flips_indices, option, newName), shell=True, text=True)


# Logs 폴더: crash터진 파일에 어떤 인자값을 전달했는지 기록하고, 해당 파일에 실행 후 전달한 값 저장
# tmp 폴더: 변조된 실행 파일
def brute_force_Logger(filename, option, value, num):
    onlyName = filename.split('/')
    newName = f"id:{num:06}_{onlyName[-1]}_op:brute"
    subprocess.run("echo '{}' > ./Logs/args:{}_{}".format(value, option, newName), shell=True, text=True) # Logs 폴더에는 id값과 인자값으로된 파일 생성하고, 해당 파일에 전달한 데이터 저장

# 기존 파일에 무작위 입력값으로 퍼징 진행
def brute_force_Mutator(filename, max_length, num):
        # 무작위 입력 값 생성
        option, value = generate_random_args_and_string(max_length)
        # 명령어 실행
        command = f'{filename} {option}'

        result = subprocess.run(command, input=value, shell=True, text=True, capture_output=True)
        out = result.stdout + result.stderr
        if("Segmentation" in out):
            print(f"Executing command: {command}")
            print("Crash:", out)
            brute_force_Logger(filename, option, value, num)

def menu():
    print("1. brute_force_fuzzing")
    print("2. bit_flipping_fuzzing")

def main():
    MAX_COMMAND_LENGTH = 100

    menu()
    select = input("select menu > ")
    fileName = input("Input filename > ")

    print("Fuzzing...")
    if(select == '1'):
        num = 1
        while(1):
            brute_force_Mutator(fileName, MAX_COMMAND_LENGTH, num)
            num = num + 1
    else:
        num = 1
        while(1):
            Worker(fileName, 0.0001, MAX_COMMAND_LENGTH, num)
            num = num + 1

if __name__ == "__main__":
    main()
