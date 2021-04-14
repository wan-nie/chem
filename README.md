# 计算化学软件输出文件的整理脚本

## gauss
*用于[Gaussian](https://gaussian.com/)的log文件能量统计和坐标生成的[python](https://www.python.org/)脚本*

* **getEnergy.py**
  * 运行后可以选择除能量外也统计电荷、自旋信息  
  * 脚本会在当前目录下得到Energy.csv文件，里面包含了能量相关信息  
  * 如果选择统计电荷和自旋，当前目录下也会得到Charges.csv文件  

- **getCoordinates.py**  
  - 运行后会得到coordinates.xyz文件  

## adf
*用于[ADF](https://www.scm.com/product/adf/)的logfile文件坐标生成的[python](https://www.python.org/)脚本*  

* **getCoordinates_ADF.py**
  * 运行后会得到coordinates_ADF.xyz文件 
  
## solvent_accessible_surface
*由[PASCUAL-AHUIR]( https://doi.org/10.1002/jcc.540151009)等人开发的[gepol93](http://server.ccl.net/cca/software/SOURCES/FORTRAN/molecular_surface/gepol93/index.shtml)*

## dmol3
*用于[DMol3](http://molscience.com/software/DMol3)的outmol文件能量统计和坐标生成的[python](https://www.python.org/)脚本*

## draw_energy_profile
*可以根据反应中各个物质的坐标（index，energy）绘制连续的曲线*
* 运行前将数据保存为data.csv
* 每一列为一个路线，主路线放到第一列。
* 辅助路线列只添加希望画出的能量值，如果有空缺则在该index添加'continue'
* 具体的例子参见`./draw_energy_profile/data.csv`和得到的`profile.png`
