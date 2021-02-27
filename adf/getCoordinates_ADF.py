import os
import re

def write(numOfAtom, file_name, coord_ls, xyz_name):
	file_name = file_name[:-8] # 去掉.logfile文件后缀名
	with open(xyz_name, 'a') as xyz:
		xyz.write("%d\n%s\n" % (numOfAtom, file_name))
		for line in coord_ls:
			xyz.write("%s\n" % line)
		xyz.write('\n')

def main():
	interval = 2 # Coordinates和坐标数据间的行差
	xyz_name = 'coordinates_ADF.xyz'

	# 删除冗余的xyz文件
	if os.path.exists(xyz_name):
		os.remove(xyz_name)

	# 遍历目录下的logfile文件并取出坐标
	for file in os.listdir():
		if file[-7:] != 'logfile':
			continue
		# 打开file获取numOfAtom, coordinates列表
		with open(file, 'r', encoding='utf-8') as f:
			line_ls = f.readlines()
			numOfAtom = 0
			coord_index_ls = []
			coordinates = []
			# 找到最后一个coordinates出现的行数: last_coord_index
			for i, line in enumerate(line_ls):
				if 'Coordinates' in line:
					coord_index_ls.append(i)
			last_coord_index = coord_index_ls[-1] + interval
		    # 取出所有的坐标到coordinates
			for line in line_ls[last_coord_index :]:
				line = line.lstrip()
				m = re.match('^[0-9]+\.(.+)', line)
				if m:
					coordinates.append(m.group(1))
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


