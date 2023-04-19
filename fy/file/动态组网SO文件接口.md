# 动态组网SO文件接口

## 1、动态组网infraEventMatchFunc

### 接口

| 接口数据           | 接口名称    | 接口格式                    |
| ------------------ | ----------- | --------------------------- |
| 所有单台阵事件台阵坐标       | arrLatLon   | double数组，8*1 |
| 声源相对阵列方位角 | theta_tilde | double数组，4*1 |
| 台阵接收到次声事件时间     | t_unix   | double数组，4*1 |
| 处理使用声速     | c0   | double，默认为300 |
| 事件匹配度[输出]     | S     | double       |


[所有单台阵事件台阵坐标]：(接受数据，从数据中获取台阵编号) 从单阵事件表中根据detect_time取出每一个台阵的最新一条记录。  
然后根据台阵编号查询：台阵基础表（dp_site_base_info）从而获取到对应的经纬度。目前有4个台阵。
比如：
  台阵 经度 纬度
  1  1.0  11.0
  2  2.0   22.0
  3  3.0   33.0
  4  4.0   44.0
则：arrLatLon=[1.0, 11.0, 2.0,22.0, 3.0, 33.0,4.0,44.0]

[声源相对阵列方位角]: 单阵事件表中代表性方位角:av_azimuth;

[台阵接收到次声事件时间]: 相关性最大时间:detect_time; 格式为13位置的时间戳，按照double传递  
[处理使用声速]:写死 默认值为:300  
[事件匹配度]: 输出为double类型的数据，规则为：
            s<0.15: 进行多阵处理，同事把此函数相关的数据写入多阵表(multi_array_event): 字段如:
                     多阵事件编号->系统uuid生成。
                     sevent_id->就是从单阵事件表中抽取4个台阵的4条最新记录。




函数声明:`double infraEventMatchFunc(const double arrLatLon[8], const double theta_tilde[4],const double t_unix[4], double c0)`

