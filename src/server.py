from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
import hashlib
import random
from dataclasses import dataclass


@dataclass
class UserDto: 
  name: str
  surname: str
  email: str
  password: str
  otp: bool


@dataclass
class AuthLogin: 
  email: str
  password: str

salt = 32
usersCsvPath = './database/users.csv'
otpCsvPath = './database/otp.csv'

app = Flask(__name__)
api = Api(app)  

class UserRepository:
  def find(self, email=None, excludePassword=True):
    data = pd.read_csv(usersCsvPath)

    if excludePassword:
      data.drop('password', axis=1, inplace=True)

    if email is not None: 
      return data[data['email'] == email]
    else: 
      return data; 

  def insert(self, user: UserDto):
    data = pd.read_csv(usersCsvPath)
    newIndex = data['userId'].max()+1
    frame = pd.DataFrame(
      [{
        "userId": newIndex,
        "password": user.password, 
        "email": user.email,
        "name": user.name,
        "surname": user.surname, 
        "otp": user.otp
      }]
    )
    
    
    n = pd.concat([data,frame])
    n.to_csv(usersCsvPath, mode='w', index=False)

  def generateOtp(self, email: str):
    otp  = random.choice('0123456789')+random.choice('0123456789')+random.choice('0123456789')+random.choice('0123456789')

    # Fake Email Sent
    print("OTP: ", otp)
    
    data = pd.read_csv(otpCsvPath)
    user = data[data['email'] == email]
    
    if user.empty: 
      frame = pd.DataFrame([{
        "email": email,
        "otp": otp
      }])
      n = pd.concat([data,frame])
      n.to_csv(otpCsvPath, mode='w', index=False)
    else:
      data.loc[user.index, ['otp']] = [otp]
      data.to_csv(otpCsvPath, mode='w', index=False)


  def checkOtp(self, email: str, otp: str) -> bool:
    data = pd.read_csv(otpCsvPath)
    user = data[data['email'] == email]

    if str(user.iloc[0]['otp']) == otp: 
      # delete row
      data.drop(user.index, axis=0, inplace=True)
      data.to_csv(otpCsvPath, index=False)
      return True


    return False

class UserController(Resource): 
  @app.route('/user', methods=['GET'])
  def find(email=None):
    userRepository = UserRepository()

    return app.response_class(
      response=userRepository.find().to_json(None, indent=1, orient='records'),
      status=200, 
      mimetype='application/json'
    )

  @app.route('/user', methods=['POST'])
  def create():
    data = request.json
    passwordHash = hashlib.sha256(str(data['password']).encode()).hexdigest() 
    userDto = UserDto(name=data['name'], surname=data['surname'], email=data['email'], password=passwordHash, otp=data['otp'])
  
    userRepository = UserRepository()
    
    # Check if user already exist
    user = userRepository.find(email=userDto.email)
    if not user.empty:
      return app.response_class(
        response='User already exists',
        status=400, 
        mimetype='application/json'
      )  

    userRepository.insert(userDto)
    
    return app.response_class(
      response=userRepository.find(email=userDto.email).to_json(None, indent=1, orient='records'),
      status=200, 
      mimetype='application/json'
    )
    

class Auth(Resource): 
  @app.route('/auth/login', methods=['POST'])
  def login(): 
    data = request.json
    passwordHash = hashlib.sha256(str(data['password']).encode()).hexdigest()

    userRepository = UserRepository() 
    user = userRepository.find(email=data['email'],excludePassword=False)
    
    if user.empty or user.iloc[0]['password'] != passwordHash: 
      return app.response_class(
        response='Auth Faild',
        status=400, 
        mimetype='application/json'
      )
    
    if user.iloc[0]['otp']:
      userRepository.generateOtp(user.iloc[0]['email'])
      return {'action': 'otp'}
    else:
      return {'token':  'jwt_token'}

    
  @app.route('/auth/otp', methods=['POST'])
  def checkOtp():
    data = request.json
    userRepository = UserRepository()
    
    if not userRepository.checkOtp(data['email'], data['otp']): 
      return app.response_class(
        response='Auth Faild',
        status=400, 
        mimetype='application/json'
      )
    
    return {'token':  'jwt_token'}


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=3000)
  
