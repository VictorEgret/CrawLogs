import os
import sys
import gzip
from uuid import *

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
		return f"{self.time} {self.ip} {self.file}"

class Player:
	uuid: UUID
	name: str
	logins: list[Login]

	def __init__(self, uuid: UUID, name: str) -> None:
		self.uuid = uuid
		self.name = name
		self.logins = []

	def __repr__(self) -> str:
		repr = f"{self.uuid} {self.name} {self.logins[0]}\n"
		tmp = len(str(self.uuid)) + len(self.name) + 2
		for login in self.logins[1:]:
			repr += tmp * " " + str(login)
		return repr

def get_type(file: str) -> str:
	for _type in ZIP_TYPES:
		if file.endswith(_type):
			return _type
	return None

def extract_log_data(filename: str, data: str, extracted: dict[UUID, Player]) -> None:
	data = data.split("\n")
	it = iter(data)
	try:
		while True:
			line = next(it)
			if "User Authenticator" in line and "UUID" in line:
				line = line.split()
				try:
					time = line[0][1:-1]
					id = UUID(line[-1])
					name = line[-3]
					line = next(it)
					line = next(it)
					line = line.split()
					ip = line[3][:-1].split("/")[1]
					if not id in extracted:
						extracted[id] = Player(id, name)
					extracted[id].logins.append(Login(time, filename, ip))
				except StopIteration:
					pass

	except:
		pass

def extract_data(path: str) -> dict[UUID, Player]:
	data = {}
	for file in os.listdir(path):
		zip_type = get_type(file)
		if not zip_type:
			continue
		try:
			with gzip.open(path + file, 'rt', encoding="utf-8") as f_in:
				extract_log_data(path + file, f_in.read(), data)
		except:
			print(f"Error while extracting {path + file}", file=sys.stderr)
	try:
		with open(path + "latest.log", 'rt', encoding="utf-8") as f_in:
			extract_log_data(path + "latest.log", f_in.read(), data)
	except: pass
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
	for player in data.values():
		print(player)

if __name__ == "__main__":
	try:
		main()
	except BaseException as e:
		print(e, file=sys.stderr)
		exit(1)
