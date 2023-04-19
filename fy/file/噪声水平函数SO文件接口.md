# 噪声水平函数SO文件接口

## 1、噪声水平noiseLevel

### 接口

| 接口数据           | 接口名称    | 接口格式                    |
| ------------------ | ----------- | --------------------------- |
| 输入数据[输入]       | datax   | float数组，大小为15000*1 |
| 噪声水平[输出] | noiseLevel | double |


输出函数声明：
`double noiseLevel(const double datax[15000])`