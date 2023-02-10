import os
import re
import sys
import gzip
from uuid import *
from typing import Optional

ZIP_TYPES = {".gz"}

class Login:
	time: str
	file: str
	ip: str

	def __init__(self, time: str, file: str, ip: str) -> None:
		self.time = time
		self.file = file
		self.ip = ip

	def __repr__(self) -> str:
		repr = f"{self.time} "
		repr += f"{self.ip}{' ' * (21 - len(self.ip))} {self.file}"
		return repr

class Player:
	uuid: UUID
	name: str
	logins: list[Login]

	def __init__(self, name: str = None, id: UUID = None) -> None:
		self.name = name
		self.uuid = id
		self.logins = []

	def __repr__(self) -> str:
		repr = f"{self.uuid} {self.name + ' ' * (16 - len(self.name))} {self.logins[0]}\n"
		tmp = len(str(self.uuid)) + len(self.name) + 16 - len(self.name) + 2
		for login in self.logins[1:]:
			repr += tmp * " " + str(login) + '\n'
		return repr

def get_type(file: str) -> str:
	for _type in ZIP_TYPES:
		if file.endswith(_type):
			return _type
	return None

def get_player_by_name(name: str, data: list[Player]) -> Optional[Player]:
	for player in data:
		if player.name == name:
			return player
	return None

def extract_log_data(filename: str, data: str, extracted: list[Player]) -> None:
	data = data.split("\n")
	line = ""
	try:
		for i in range(len(data)):
			line = data[i]
			time = line[1:9]
			has_ip = re.search(r"\w+\[\/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})", line)
			if has_ip:
				line = has_ip.group(0)
				name = line[:line.index('[')]
				ip = line[line.index('/') + 1:]
				player = get_player_by_name(name, extracted)
				if not player:
					player = Player(name=name)
					extracted.append(player)
				player.logins.append(Login(time, filename, ip))
				continue

			# TODO good uuid pattern
			has_uuid = re.match(r"(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})\.", line)
			print(line)
			if "User Authenticator" in line and has_uuid:
				line = line.split()
				id = line[-1]
				name = line[-3]
				player = get_player_by_name(name, extracted)
				if not player:
					player = Player(name, id)
					extracted.append(player)
				player.uuid = id
	except (StopIteration, IndexError):
		pass
	except ValueError:
		print(f"Invalid UUID format: \"{line[-1]}\"", file=sys.stderr)

def progress_bar(current, total, size):
	if not current == 0:
		print("\033[2K", end='')
	done = int(current / total * size)
	if current == total:
		print(f"\r|{'█' * size}| (100.00 %) ")
	else:
		print(f"\r|{'█' * done + ' ' * (size - done)}| ({current * 100 / total:.2f} %) ", end='')

def extract_data(path: str) -> list[Player]:
	data = []
	files = os.listdir(path)
	if os.path.exists(path + "latest.log"):
		files.append("latest.log")
	i = 1
	total = len(files)
	for file in files:
		progress_bar(i, total, 30)
		zip_type = get_type(file)
		if zip_type == None:
			try:
				with open(path + file, 'rt', encoding="utf-8") as f_in:
					extract_log_data(path + file, f_in.read(), data)
			except OSError:
				print(f"Error while extracting {path + file}", file=sys.stderr)
		else:
			try:
				with gzip.open(path + file, 'rt', encoding="utf-8") as f_in:
					extract_log_data(path + file, f_in.read(), data)
			except (OSError):
				print(f"Error while extracting {path + file}", file=sys.stderr)
		i += 1
	return data

def main() -> None:
	print("Logs data browser by Victor Egret for Minecraft 1.19.3")
	if len(sys.argv) == 1:
		path = input("Enter the logs folder path: ")
	else:
		path = sys.argv[1].replace("\\", "/")
	if not path[-1] == '/':
		path += '/'
	if not os.path.exists(path):
		raise FileNotFoundError(f"Cannot find {path}")
	if not os.path.isdir(path):
		raise NotADirectoryError(f"{path} is not a directory")
	
	data = extract_data(path)
	for player in data:
		print(player)

if __name__ == "__main__":
	try:
		main()
	except BaseException as e:
		print(e, file=sys.stderr)
		exit(1)
