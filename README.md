# 2FA

## Assignment

Your company is behind an online forum about cooking. The users need to register into it providing their email, password, some basic profile info, and then perform a safe login. In order to increase the safety of the login process, a user can enable the 2FA at the registration step to receive at the provided email a random OTP needed to complete the flow. To reduce the complexity of the assignment (if you want) you can use as Email Sender component a fake implementation that simply logs on the stdout the OTP rather than send the email for real.

You’re responsible to design a backend service and to actually code it in Python. You must version this project with git and provide a public URL where we can check your solution. Please don’t put any reference to our company inside the repository.

Some constraints:

- Provide a README.md file with clear instructions about how we can test your service in a local development environment;
- The communication protocol will be HTTP. We expect one route to register users, a second route to allow them to log in and a third to use in case the 2FA is enabled. You’re free to design as you like, but you’re asked to provide documentation for all of the endpoints;
- This service will operate inside a micro-services architecture and must be shipped inside a docker image, in order to be deployable in the cloud;
- We expect you to write automated tests for your project.

## Solution

The proposed solution is very simple. Due to a lack of time, a simple structure has been kept by developing a microservice that exposes Rest API
(defined in the swagger.yaml) for creating and authenticate a user.
To keep things as simple as possible, thanks to `pandas` library, i adopted the use of a csv file as a database and develop APIs with `Flask` framework.

Since I don't use python for backend development in my job, and not knowing any python test frameworks, and due to a lack of time, I haven't written unit tests, however, future tests can be written using `Pytest` or `PyUnit`.

In the root of this project you can find a Postman collection with a few api ready to use, import that collection in Postman to test the microservice.

If a new user is registered with flag otp set to true, in order to authenticate, the new user will have to follow a further step in which he have to declare an otp "sent by email" (the otp will be print in the console) sending email & otp at the endpoint `/auth/otp`, in response he will get an auth token.

To speed up development, for now all the code is save in a single file.

## Build

All building activities are managed by a Makefile. To build the docker image of the project go to the root of the directory,
and run the command `make build`. This command will create a new image named `2fa:latest`

## Run the server

To run the server, run the command `make server-up`. This command will execute the server on localhost on the port defined in the .env (default port is 3000)

## Possible Improvements

- Thank to the repository layer used to manage user data, a possible improvement can be switch from csv file to a database like `PostgreSQL` or `MongoDB`;
- Write some unit test using `Pytest` or `PyUnit`;
- Write the swagger documentation inside the code, using decorators (see [NestJS Swagger Decorator](https://docs.nestjs.com/openapi/types-and-parameters#types-and-parameters)) instead of handwriting in a swagger file;
- Introduce internal API doc UI inside the project;
- Better sepration of Controller, Service and Repository layers inside the codebase;
- Usint DTOs with validators to validate incoming data from API and throw the right error in case of unsuccessful validation;
- Introduce stage level in Dockerfile or using distroless images.
