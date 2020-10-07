# Klambda

## 1. Description

Klambda is Command-line tool that connects to AWS services and perform a series of steps that manage the storage and authorization of users in order to create backend projects effectively and having a library of Lambda functions that are reusable on different projects and teams.All of this is setted up through a specification file, that its content will be processed, thus generating team projects, Lambda functions within their configuration. 

## 2. Steps to configure
In order to use the program, it's important to follo the next:

- Create an account on [Serverless](https://www.serverless.com/) and install it on your computer with some of the following commands:
    - Linux/Mac:
    ```
    curl -o- -L https://slss.io/install | bash 
    ```
    - Windows (using choco package manager):
    ```
    choco install serverless
    ```
    - With npm:
    ```
    npm install -g serverless
    ```

- Login into Serverless Framework locally with the next command:
```
serverless login
```
**This command will open your default browser, please indicate your credentials, it will redirect to the terminal and it will recognize your credentials.**

- Create an account on [AWS](https://aws.amazon.com/), then follow the instructions of the next [video](https://www.youtube.com/watch?v=KngM5bfpttA)


- Install Docker Desktop:
[mac](https://docs.docker.com/docker-for-mac/install/)
[windows](https://docs.docker.com/docker-for-windows/install/)

**Note: In case on of the commands present error, please execute it again under admin permissions.**

The way to execute the Docker image of the program is the following:
- Linux/Mac:
```
docker run --rm -it -v $(pwd):/project falvaradoe/klambda -h
```
- Windows:
```
docker run --rm -it -v %cd%:/project falvaradoe/klambda -h
```
- PowerShell:
```
docker run --rm -it -v ${PWD}:/project falvaradoe/klambda -h
```
Please use the format properly according to your Operating System.

## 3. How to use it
1. Create a folder where you want to storage a new project and navigate to it on the terminal.

2. Create the klambda.yml and user.yml files.

3. To execute the program and view the help menu, run the next command:
```
docker run --rm -it -v $(pwd):/project falvaradoe/klambda --h
```
This command will download the Docker image locally.
4. The common way to use the different features of the tool is this:
```
klambda [module||command] [command||parameters] [parameters]
```
**Remember that the specification and user credentials files are necessary to execute the  commands available in the tool.**