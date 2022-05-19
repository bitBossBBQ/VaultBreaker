#!/usr/bin/python3
import subprocess
import timeit
import string

vault_path="/home/kali/Desktop/vault/vault.o" #Specify the full path the the vault binary
bad_char="1"
number_of_tests=100#The more tests run, the more likely it is for the password to become solved. This also makes the attack take longer.
max_password_length=11

def password_found(command,args): #A simple string match check based on the command output
	the_check=False
	result=subprocess.run([command, args], capture_output=True, text=True)
	if "SUCCESS" in result.stdout:
		the_check=True
	return the_check

def benchmark(command_path, command_args, num_of_tests):
	command_path_setup="import subprocess"
	system_command_path=f"subprocess.run(['{command_path}', '{command_args}'], capture_output=True, text=True)"
	t = timeit.timeit(stmt=system_command_path, setup=command_path_setup, number=num_of_tests)
	return t

def find_best_word(known_bad_char, password, num_of_tests):
	best_time=benchmark(vault_path, password+known_bad_char, num_of_tests)-benchmark(vault_path, password, num_of_tests) #Starting with a known bad test time
	for test_char in string.ascii_lowercase:
		test_time=benchmark(vault_path, password+test_char, num_of_tests)-benchmark(vault_path, password, num_of_tests) #Cycle through the lowercase ascii chars
		if test_time>best_time:
			best_time=test_time
			best_char=test_char
	return password+best_char

the_password=""
incomplete=True
count=1
while incomplete:
	the_password=find_best_word(bad_char, the_password, number_of_tests)
	print(f"{the_password}")
	if password_found(vault_path,the_password) or count==max_password_length:
		incomplete=False
	count+=1
print(f"Is the password {the_password} correct? {password_found(vault_path,the_password)}")
