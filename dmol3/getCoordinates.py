import os
import re

def write(numOfAtom, file_name, coord_ls, xyz_name):
	file_name = file_name[:-7] # 去掉.outmol文件后缀名
	with open(xyz_name, 'a') as xyz:
		xyz.write("%d\n%s\n" % (numOfAtom, file_name))
		for line in coord_ls:
			xyz.write("%s\n" % line)
		xyz.write('\n')

def main():
	xyz_name = 'coordinates_dmol3.xyz'

	# 删除冗余的xyz文件
	if os.path.exists(xyz_name):
		os.remove(xyz_name)

	# 遍历目录下的outmol文件并取出坐标
	for file in os.listdir():
		if file[-6:] != 'outmol':
			continue
		# 打开file获取numOfAtom, coordinates列表
		with open(file, 'r', encoding='utf-8') as f:
			line_ls = f.readlines()
			numOfAtom = 0
			coord_index = 0
			coordinates = []
			# 找到Final Coordinates出现的行数: coord_index
			for i, line in enumerate(line_ls):
				if 'Final Coordinates' in line:
					coord_index = i
					interval = 3 # 有Coordinates关键字的行和坐标数据间的行差
					coord_index += interval
					break
		    # 取出所有的坐标到coordinates
			for line in line_ls[coord_index :]:
				line = line.lstrip()
				match = re.match('^[0-9]+.+([A-Z]+.+)', line)
				if match is not None:
					coordinates.append(match.group(1))
				else:
					break
			numOfAtom = len(coordinates)
		#将从file得到的信息写入xyz_name
		write(numOfAtom, file, coordinates, xyz_name)

	return xyz_name


if __name__ == '__main__':
	try:
		file = main()
		print("%s has been exported" % file)
	except:
		print("Warning! Something went wrong")
