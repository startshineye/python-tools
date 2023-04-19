# 识别函数SO文件接口

## 1、特征值计算sigprocess

### 1、函数cal_Dispersion接口

| 接口数据 | 接口名称   | 接口格式 |
| -------- | ---------- | -------- |
| 输入数据 | dataIn     | float    |
| 数据长度 | dataLen    | uint     |
| 离散度[输出]   | dispersion | double   |

函数声明：

`double cal_Dispersion(float a[], unsigned int N)`

### 2、函数cal_Skewness接口

| 接口数据 | 接口名称 | 接口格式 |
| -------- | -------- | -------- |
| 输入数据 | dataIn   | float    |
| 数据长度 | dataLen  | uint     |
| 偏斜度[输出]   | skewness | double   |

函数声明：

`double cal_Skewness(float a[], unsigned int N)`

### 3、函数cal_Peakedness接口

| 接口数据 | 接口名称   | 接口格式 |
| -------- | ---------- | -------- |
| 输入数据 | dataIn     | float    |
| 数据长度 | dataLen    | uint     |
| 峭度[输出]     | peakedness | double   |

函数声明：

`double cal_Peakedness(float a[], unsigned int N)`

### 4、函数cal_Zero_crossingrate接口

| 接口数据 | 接口名称          | 接口格式 |
| -------- | ----------------- | -------- |
| 输入数据 | dataIn            | float    |
| 数据长度 | dataLen           | uint     |
| 过零率[输出]   | zero_crossingrate | double   |

函数声明：

`double cal_Zero_crossingrate(float a[], unsigned int N)`

### 5、函数cal_spectral_roll_off接口

| 接口数据 | 接口名称          | 接口格式 |
| -------- | ----------------- | -------- |
| 输入数据 | dataIn            | float    |
| 处理数据 | take            | float    |
| 数据长度 | dataLen           | uint     |
| 采样率   | sampleRate           | uint     |
| 频谱滚降[输出] | spectral_roll_off | double   |

函数声明：

`double cal_spectral_roll_off(float* da, float* take, unsigned int dataLen, unsigned int fs);`

### 6、函数cal_spectral_flux接口

| 接口数据 | 接口名称     | 接口格式              |
| -------- | ------------ | --------------------- |
| 输入数据 | dataIn       | float                 |
| 数据长度 | dataLen      | uint                  |
| 步长   | step           | uint                  |
| 窗长   | win           | uint                  |
| 频谱通量[输出] | spectral_flux | 结构体ARRAY，格式后附 |

函数声明：

`ARRAY cal_spectral_flux(float* a, unsigned int N, unsigned int step, unsigned int win);`

```c
typedef struct {
    float* addr;
    unsigned int size;
} ARRAY;
```



### 7、函数cal_Spectral_centroid接口

| 接口数据 | 接口名称          | 接口格式 |
| -------- | ----------------- | -------- |
| 输入数据 | dataIn            | float    |
| 数据长度 | dataLen           | uint     |
| 窗长   | win           | uint                  |
| 步长   | step          | uint                  |
| 频谱质心[输出] | spectral_centroid | double   |

函数声明：

`double cal_Spectral_centroid(float* xx, unsigned int N, unsigned int win, unsigned int step)`

### 8、函数cal_bispecd接口

| 接口数据 | 接口名称 | 接口格式              |
| -------- | -------- | --------------------- |
| 输入数据 | dataIn   | float                 |
| fft窗长 | nfft   | int             |
| 窗长 | wind   | uint             |
| 重叠长度 | overlap   | uint             |
| 参数1 | nrecs   | uint             |
| 参数2 | ly  | uint                  |
| 双谱[输出] | bispecd  | 结构体ARRAY，格式后附 |

函数声明：

`ARRAY cal_bispecd(float* y, int nfft, unsigned int wind,unsigned int nsamp, unsigned int overlap, unsigned int nrecs, unsigned int ly);`

```c
typedef struct {
    float* addr;
    unsigned int size;
} ARRAY;
```

八个函数说明：
第1个到第4个函数的输出结果为时域特征；
第5个到第7个函数的输出结果为频域特征；
第8个函数的输出结果为时频域特征；



