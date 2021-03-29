import os


class Parameters:
    file = 'File_name'
    basis = 'Basis'
    potential = 'Pseudopotential'
    functional = 'Functional'
    aux = 'Aux_density'
    grid = 'Integration_grid'
    energy = 'Energy'


def write(single_file_parasmeter_list, csv_name):
    with open(csv_name, 'a') as csv:
        writing_string = ','.join(single_file_parasmeter_list)
        writing_string += '\n'
        csv.write(writing_string)


def main():
    csv_name = 'Energy.csv'

    # 删除冗余的csv文件
    if os.path.exists(csv_name):
        os.remove(csv_name)

    # 建立csv文件的表头
    with open(csv_name, 'a') as csv:
        csv.write('%s,%s,%s,%s,%s,%s,%s\n' % (Parameters.file,Parameters.basis, Parameters.potential,
                                    Parameters.functional, Parameters.aux,
                                    Parameters.grid, Parameters.energy))

	# 遍历目录下的outmolfile文件取出能量等信息，取出后写入csv文件
    for file in os.listdir():
        if file[-6:] != 'outmol':
            continue
        with open(file, 'r') as f:
            line_ls = f.readlines()
            paras_index = 0
            energy_index = 0
            paras = []
            energy = 0
            # 遍历文件行找到paras所在位置和energy所在位置
            for i, line in enumerate(line_ls):
                if 'Electronic parameters' in line:
                    paras_index = i
                    interval = 3  # 选取的信息从Basis开始
                    paras_index += interval

                if 'Energy is' in line:
                    energy_index = i

            paras = [line.split()[1] for line in line_ls[paras_index : paras_index+5]]
            energy = line_ls[energy_index].split()[2]
            paras.append(energy)
            paras.insert(0, file)
        write(paras, csv_name)

if __name__ == '__main__':
    main()
