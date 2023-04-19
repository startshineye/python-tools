from MysqlDBUtils import MysqlDB
import time
import ctypes

if __name__ == '__main__':
    c_float_array = ((ctypes.c_float * 5) * 15000)()
    while True:
        print('开始执行......')
        # 1、定期从原始数据表获取数据
        db = MysqlDB('103.36.193.81', 3306, 'root', 'rbjf_DEV123', 'ruoyi')
        results = db.select('SELECT infra_data FROM dp_origin_data where site_id=1 and (operate_status=0 or '
                            'operate_status is NULL) group by device_id')

        print(len(results))

        # 定义二维数组
        data = []
        # 遍历每行结果,添加到二维数组
        for row in results:
            # 将每一行数据按逗号切割
            arr = row[0].strip('[ ] \n').split(',')
            # 定义一维c_float数组
            c_arr = (ctypes.c_float * len(arr))()
            # 添加数据到c_float数组
            for i in range(len(arr)):
                c_arr[i] = ctypes.c_float(float(arr[i]))

                # 添加到data二维数组
            data.append(c_arr)

        print(data)
        print(type(data))

        if len(results) > 0:
            db.update('UPDATE dp_origin_data SET operate_status=%s WHERE site_id=1', 1)


        # 暂停10秒
        time.sleep(10)