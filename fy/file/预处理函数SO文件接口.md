# 预处理函数SO文件接口

## 1、预处理InfraPreproc

### 接口

| 接口数据 | 接口名称   | 接口格式              |
| -------- | ---------- | --------------------- |
| 输入数据 | wvfrm_raw  | double数组，长度75000 |
| 输出数据 | wvfrm_proc | double数组，长度75000 |

函数声明：
void InfraPreproc(double *wvfrm_raw*[75000], double *wvfrm_proc*[75000])
