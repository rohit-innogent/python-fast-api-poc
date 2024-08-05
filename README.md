# python-fast-api-poc

## Description
A CRUD based POC project using fast api which is one of the fastest framework for python.

# Steps for Deploying to AWS EC2
Log into your AWS account and create an EC2 instance using the latest stable Ubuntu Linux AM and SSH into the instance and run these commands to update the software repository and install our dependencies.
```bash
sudo apt-get update
sudo apt install -y python3-pip
```

Clone the repository
```bash
git clone https://github.com/rohit-innogent/python-fast-api-poc.git
```

Start application
```bash
cd python-fast-api-poc

git checkout fast-api-poc

python3.11 -m pip install -r requirements.txt

python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

After running go to AWS instance --> Security tab --> Edit inbound rules --> create rule --> Enable access from anywhere.
Go to the public ip provided by the instance add :8000 in the end as our api is running at that particular port.

That's it you can now access your Fastapi from anywhere.

### Video link to deploy application on AWS EC2
Youtube: [Video link](https://www.youtube.com/watch?v=_719QPPARUw)
GitHub repo link : [GitHub link](https://github.com/smurfcoders/fastapi-hosting)
