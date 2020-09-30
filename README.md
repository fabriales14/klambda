# Klambda

## 1. Description

Klambda is Command-line tool that connects to AWS services and perform a series of steps that 
manage the storage and authorization of users in order to create backend projects effectively,
having a library of Lambda functions that are reusable on different projects and teams.
All of this is setted up through a specification file, that its content will be processed, 
thus generating team projects, Lambda functions within their configuration. 

## 2. Steps to configure
In order to use the program, it's important to follo the next:

- Sign In on [Serverless](https://www.serverless.com/) and install it on your [computer](https://www.serverless.com/framework/docs/getting-started/).

- Sign In into [AWS Console](https://aws.amazon.com/).
**Notes:**
Make sure you are locally logged into your AWS account, if not, please follow the next steps:
## Setup your AWS Credentials
Go to IAM -> Select your user -> Security Credentials -> Create Access Key
Copy your api key
Copy your secret
```
sls config credentials --provider aws --key <YOUR KEY> --secret <YOUR SECRET>
```
To configure as your default profile use
```
sls config credentials --provider aws --key <YOUR KEY> --secret <YOUR SECRET> --profile default -o
```
Reference [here](https://serverless.com/framework/docs/providers/aws/cli-reference/config-credentials/).

- Make sure you have the last [Python](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/#files) installed on your machine, verify that these tools are executable from the terminal.

- Clone the repository from [here](https://gitlab.com/fabriales14/klambda).

- From the terminal navigate to the folder containing the project.

- Exexute the following command on the root folder of the project:
```
python setup.py install
```

## 3. How to use it
1. Create a folder where you want to storage a new project and navigate to it from the terminal.

2. Create the klambda.yml and user.yml files.

3. To execute the program and view the help menu, run the next command:
```
klambda -h
```

4. The common way to use the different features of the tool is this:
```
klambda [module||command] [command||parameters] [parameters]
```
Remember that the specification and user credentials files are necessary to execute the 
commands available in the tool.