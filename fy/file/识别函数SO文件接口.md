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
| 采样率   | sampleRate           | uint，示例100 |
| 频谱滚降[输出] | spectral_roll_off | double   |

函数声明：

`double cal_spectral_roll_off(float* da, float* take, unsigned int N, unsigned int fs);`

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
| 窗长   | win           | uint，示例1024      |
| 步长   | step          | uint，示例512        |
| 频谱质心[输出] | spectral_centroid | double   |

函数声明：

`double cal_Spectral_centroid(float* xx, unsigned int N, unsigned int win, unsigned int step)`

### 8、函数cal_bispecd接口

| 接口数据 | 接口名称 | 接口格式              |
| -------- | -------- | --------------------- |
| 输入数据 | dataIn   | float                 |
| fft窗长 | nfft   | int             |
| 窗长 | wind   | uint             |
| 采样点数 | nsamp | uint |
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

### 9、上述8个函数输出为csv文件

样例如下：

| variance           | peakedness   | skewness     | zero_crossing_rate | spectral_centroid | spectral_roll_off | label |
| ------------------ | ------------ | ------------ | ------------------ | ----------------- | ----------------- | ----- |
| 6285750.1330416109 | 6.7565287961 | 0.6416172462 | 0.0120000000       | 0.0074015018      | 49.6277313232     | -1    |

先只填入这六种数据，最后一列默认为label和-1。

## 2、识别计算recog

### 1、函数model_load接口

| 接口数据           | 接口名称        | 接口格式        |
| ------------------ | --------------- | --------------- |
| 模型文件绝对地址   | model_file_name | string          |
| 模型文件指针[输出] | model           | 结构体svm_model |

```c++
struct svm_model
{
	struct svm_parameter param;	
	int nr_class;		
	int l;			
	struct svm_node **SV;		
	double **sv_coef;	
	double *rho;		
	double *probA;		
	double *probB;
	double *prob_density_marks;	
	int *sv_indices;       
	int *label;		
	int *nSV;		
	int free_sv;					
};
```

函数声明`struct svm_model *model_load(const char **model_file_name*)`

### 2、函数read_csv_problem接口

| 接口数据               | 接口名称 | 接口格式          |
| ---------------------- | -------- | ----------------- |
| 特征值数据地址         | dataIn   | 字符串数组        |
| 特征值数据结构体[输出] | prob     | 结构体svm_problem |

```c++
struct svm_problem
{
	int l;					
	double *y;
	struct svm_node **x;	
};

struct svm_node
{
	int index;		
	double value;  
};
```

函数声明`struct svm_problem read_csv_problem(const char* input_file_name)`

### 3、函数model_pred接口

| 接口数据         | 接口名称    | 接口格式          |
| ---------------- | ----------- | ----------------- |
| 模型文件指针[结构体]     | model      | float             |
| 特征值数据结构体 | prob        | 结构体svm_problem |
| 事件类型[输出]   | event_class | double数组        |

```c++
struct svm_problem
{
	int l;					
	double *y;
	struct svm_node **x;	 
};

struct svm_node
{
	int index;		
	double value;  
};
```

函数声明`double* model_pred(struct svm_model model, struct svm_problem prob)`
