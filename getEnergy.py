import os
import sys
import re

def find_charges_spin(file, line_ls):
    # interval指的是行与行之间的差距
    interval_npa = 6
    interval_mulliken = 2
    interval_atom = 0

    npa_indexes = [] # 每个nbo分析包含了三个npa_index, 分别是total, alpha, beta
    mulliken_index = 0

    npa_charges = []
    alpha_spin = []
    beta_spin = []
    npa_spin = []

    atom_ls = []
    mulliken_charges = []
    mulliken_spin = []

    # 遍历文件找到原子的个数
    for line in line_ls:         
        if "NAtoms" in line:
            interval_atom = eval(line.split()[1])
            break

    # 开壳层体系存在total, alpha, beta电子的npa电荷, 将三个各自的行数取出
    for i, line in enumerate(line_ls):
        if "Summary of Natural Population Analysis:" in line:
            npa_indexes.append(i)

    # 取最后一个mulliken的行数
    for i, line in enumerate(line_ls):
        if "Mulliken charges and spin densities:" in line or "Mulliken charges:" in line:
            mulliken_index = i

    # 得到total_npa电荷的list
    if len(npa_indexes) == 0: # 关键字没有nbo或npa
        npa_charges = ['None'] * interval_atom
        npa_spin = ['None'] * interval_atom
    else:
        # 取total的npa电荷
        total_npa_index = npa_indexes[0] + interval_npa 
        for line in line_ls[total_npa_index : total_npa_index + interval_atom]:
            npa_charges.append(line.split()[2])
        # 计算npa_spin
        # 1. 取alpha的电子
        alpha_npa_index = npa_indexes[1] + interval_npa
        for line in line_ls[alpha_npa_index : alpha_npa_index + interval_atom]:
            alpha_spin.append(line.split()[-1])
        # 2. 取beta的电子
        beta_npa_index = npa_indexes[2] + interval_npa
        for line in line_ls[beta_npa_index : beta_npa_index + interval_atom]:
            beta_spin.append(line.split()[-1])
        # 3. 利用alpha电子和beta电子得到npa_spin
        alpha_spin = [float(n) for n in alpha_spin]
        beta_spin = [float(n) for n in beta_spin]
        npa_spin = [a - b for a, b in zip(alpha_spin, beta_spin)]

    # 得到mulliken电荷和自旋的list
    mulliken_index = mulliken_index + interval_mulliken
    for line in line_ls[mulliken_index : mulliken_index + interval_atom]:
        atom_ls.append(line.split()[1])
        mulliken_charges.append(line.split()[2])     
        try:
            mulliken_spin.append(line.split()[3])
        except:
            mulliken_spin.append('None') # 对于闭壳层体系, 没有mulliken_spin

    # 将file内的信息追加写入Charges.csv
    with open('Charges.csv', 'a') as f:
        f.write('%s\nAtom,No,Mulliken Charges,Mulliken Spin,NPA Charges,NPA Spin\n' % file)
        for i in range(interval_atom):
            f.write("%s,%d,%s,%s,%s,%s\n" % (atom_ls[i],
                                                i+1,
                                                mulliken_charges[i],
                                                mulliken_spin[i],
                                                npa_charges[i],
                                                npa_spin[i],
                                                ))

        f.write('\n')

def find_charge_multiplicity(line_ls, charge, multiplicity):
    for line in line_ls:
        if "Charge" in line and "Multiplicity" in line:
            charge = line.split()[2]
            multiplicity = line.split()[-1]
            break
    return charge, multiplicity

def main():
    while True:
        get_charges = input("Should charges and spin also be exported (y/n)? Input q to quit.\n")
        if get_charges == 'y':
            # 统计电荷前删除当前目录下的Charges.csv
            if os.path.exists('Charges.csv'):
                os.remove('Charges.csv')
            break
        elif get_charges == 'n':
            break
        elif get_charges == 'q':
            sys.exit()
        else:
            print("Please input y/n or q.")

    with open('Energy.csv', 'w') as result:
        # 写入表头
        result.write("File Name,isNormalTermination,Freq Functional,Imaginary Freq,\
    Thermal Correction To G,Charge ◇ Multiplicity,SCF Functional,Electronic Energy\n")
        # 遍历当前目录下所有的log文件, 提取有效信息, 写入Energy.csv文件
        for file in os.listdir():
            if file[-3:] != 'log':
                continue   
            isNormal = 'Abnormal'
            freq_ls = []
            imaginary = "No Freq"
            thermalCorrectionToGibbs = 'No Freq'
            method_freq = 'No Freq'    
            charge = 'None'
            multiplicity = 'None'
            scf = 'None'
            method_scf = 'None'   
            # 将log文件内的信息取出
            with open(file, 'r') as f:
                line_ls = f.readlines()

                #检查正常结束
                if "Normal termination of Gaussian" in line_ls[-1]:
                    isNormal = 'Normal'

                #导出电荷和自旋
                if get_charges == 'y' and isNormal == 'Normal':
                    find_charges_spin(file, line_ls)

                #得到charge和multiplicity
                charge, multiplicity = find_charge_multiplicity(line_ls, charge, multiplicity)
                # 如果log文件是从chk文件读取的坐标等信息, log文件内不会有charge, multiplicity?
                if charge != 'None':
                    charge_multiplicity = "(%s ◇ %s)" % (charge, multiplicity)
                else:         
                    charge_multiplicity = "Not found"  #没找到就填Not found
                            
                #得到频率、scf等信息
                pattern_freq = re.compile("^\s#.+\s(.+)/.+Freq$")
                for line in line_ls:
                    #得到频率计算的方法                  
                    if re.findall(pattern_freq, line):
                        method_freq = re.findall(pattern_freq, line)[0]
                    #得到自由能矫正
                    if "Thermal correction to Gibbs Free Energy" in line:
                        thermalCorrectionToGibbs = eval(line.split()[-1])
                    #得到SCF值和SCF计算的方法
                    if "SCF Done" in line:
                        scf = eval(line.split()[4])
                        method_scf = line.split()[2][2:-1]

                #如果做了freq计算就判断虚频的个数和最小的频率
                if method_freq != 'No Freq':
                    #将所有频率取出
                    for line in line_ls:
                        if "Frequencies --" in line:
                            entry_ls = re.findall("(-?[0-9]+\.[0-9]+)", line)
                            entry_ls = [float(item) for item in entry_ls]
                            freq_ls += entry_ls     
                    freq_ls = sorted(freq_ls)
                    minimum_freq = freq_ls[0]                
                    negative_count = 0
                    if minimum_freq < 0:    
                        for freq in freq_ls:
                            if freq < 0:
                                negative_count += 1
                    imaginary = '%d (min = %.2f)' % (negative_count, minimum_freq)

            # 将提取的有效信息写入Energy.csv
            result.write("{},{},{},{},{},{},{},{}\n".format(file, isNormal, method_freq, imaginary,
                                                         thermalCorrectionToGibbs, charge_multiplicity,
                                                         method_scf, scf))

if __name__ == '__main__':
    main()
    print("Normal Termination")

