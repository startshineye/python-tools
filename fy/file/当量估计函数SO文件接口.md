# 当量估计函数SO文件接口

## 1、当量估计EnergyCalFunc

### 接口

| 接口数据           | 接口名称    | 接口格式                    |
| ------------------ | ----------- | --------------------------- |
| 台阵状态       | nCHState   | int数组，大小为5*1 ；默认写0|
| 输入信号[输入] | pCH1D | float数组，大小为15000*1（每一个台阵,其中一个阵元150s的数据,也就是之前数据的每一列，我们用第一列即可） |
| 输入信号长度     | nsigLen   | int，为15000 |
| 采样率 | Fs | float，为100    |
| 传感器数量     | nDimMic        | int，为5       |
| 标记符号     | ArrFlag     | int，为5            |
| 分辨率     | Resolution     | float，为100                      |
| 声源与台阵距离     | DistS2A     | float 距离先写500；后面再调      |
| 风速     | windSpeed     | float  风速先写20；后面再调    |
| 天气     | weather     | int，为1                      |
| 地震类型     | earthquake     | int，为1                      |
| 控制参数     | structParameter     | 结构体Sys_Parameters，示例如下|
| 频率下限     | LowLimFreq     | float，为0.01                     |
| 频率上限     | HighLimFreq     | float，为20                     |
| 函数返回值: 当量[输出]     | energy     | float                     |


```c++
struct Sys_Parameters
{
	float windowLen[15];  //窗口长度
	float freqBins[15];   //频率序列
	float csThd[15];      //一致性门限
	float corrThd[15];    //相关门限
	float sigma_A[15];    //方位角方差门限
	float sigma_V[15];    //声速方差门限
	float sigma_F;        //频率方差门限
	float sigma_T;        //时间方差 百分比 通常为100%，即与步长一致 10秒
	float timeThd;        //时间域值门限 通常为200%    默认为20秒
	int   nFamilyMax;     //family 中最多的元素数
	int   nFamilyMin;     //family 中最少的元素数
	float ThresholdDistance;
	// 界面新增
	float VelocityMax;    //声速最大值阈值
	float VelocityMin;    //声速最小值阈值

	float freqHighLim[15];
	float freqLowLim[15];
	float overlapRate;

};
```
输出函数声明：
`float EnergyESTCallBack(int * nCHState, float*pCH1D, int nsigLen, float Fs, 
int nDimMic, int ArrFlag, float Resolution, float DistS2A,
float windSpeed, int weather, int earthquake,
Sys_Parameters structParameter, float LowLimFreq, float HighLimFreq)`