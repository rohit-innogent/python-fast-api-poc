# python-fast-api-poc

## Description
A CRUD based POC project using fast api which is one of the fastest framework for python.

# Steps for Deploying to AWS EC2
Log into your AWS account and create an EC2 instance using the latest stable Ubuntu Linux AM and SSH into the instance and run these commands to update the software repository and install our dependencies.
```bash
sudo apt-get update
sudo apt install -y python3-pip nginx
```

Add the FastAPI configuration to NGINX's folder. Create a file called fastapi_nginx .

```bash
sudo vim /etc/nginx/sites-enabled/fastapi_nginx
```

And put this config into the file (replace the IP address with your EC2 instance's public IP):
```bash
server {
    listen 80;   
    server_name <YOUR_EC2_IP>;    
    location / {        
        proxy_pass http://127.0.0.1:8000;    
    }
}
```

Start NGINX
```bash
sudo service nginx restart
```

Clone the FastAPI server app
```bash
https://github.com/rohit-innogent/python-fast-api-poc.git
```

Start FastAPI
```bash
cd python-fast-api-poc

pip install -r requirements.txt

python -m uvicorn main:app
```

Video link for reference [click to open link](https://www.youtube.com/watch?v=SgSnz7kW-Ko)
