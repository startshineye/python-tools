docker build -t jieba_image:v11.0 .
docker run -itd --name  jieba --restart=always -p 5000:5001 jieba_image:v11.0