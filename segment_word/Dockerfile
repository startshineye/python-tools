FROM python:3.6
# 把store项目 添加到code文件夹 (code无需创建)
RUN mkdir /app/
WORKDIR /app/
COPY ./app .
COPY ./app/requirements.txt .
RUN pip3 config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple
RUN pip3 config set install.trusted-host pypi.mirrors.ustc.edu.cn
RUN pip3 install --no-cache-dir -r requirements.txt
# 端口5000 (可删除)
EXPOSE 5000
# 执行
CMD ["python3", "/app/SegmentAPI.py", "0.0.0.0"]