from flask import request,jsonify
from flask_jwt_extended import (
    create_access_token,create_refresh_token,
    jwt_required,get_jwt_identity
)

from sqlalchemy import or_

import random,uuid,os,psycopg2

from apps.helpers.send_mail import send_email
from apps import db
from apps.helpers.s3 import upload_image_to_s3
from apps.database.models import User,Group,Exepense,UserLogin

from decouple import config

from datetime import datetime


def testing_api():
    user = db.session.query(User).first()
    data = {
        'id':user.id,
        'name':user.name,
        'username':user.user_name,
        'profile_image':user.profile_image
    }
    response = jsonify({
                'status': 'SUCCESS',
                'code': 200,
                'message': 'Testing Api with data',
                'data':data
            }), 200
    return response


def create_user():
    try:
        
        params = request.form
        
        try:
            user = db.session.query(User).filter(User.email == params.get('email')).first()

            auth_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            
            user_data = {
                'id':user.id,
                'name':user.name,
                'user_name':user.user_name,
                'profile_image':user.profile_image,
                'email':user.email,
                'dob':user.dob,
                'current_currency':user.current_currency,
                'device_id':user.device_ids,
                'created_at':str(user.created_at),
            }
            
            response = jsonify({
                'status': 'SUCCESS',
                'code': 302,
                'message': 'User Already Exist',
                'data':{
                    'token':auth_token,
                    'refresh_token':refresh_token,
                    'user':user_data
                    }
            }), 302
        except:
            image = upload_image(request.files['image'])
            device_id = []
            device_id.append(params.get('device_id'))
            user = User(
                name = params.get('name'),
                profile_image = image,
                email=params.get('email'),
                device_ids=device_id
            )
            
            db.session.add(user)
            db.session.commit()
            
            device_details = UserLogin(
                user_id = user.id,
                device_id = params.get('device_id'),
                device_name = params.get('device_name'),
                logged_in_status = True,
                login_at = datetime.now()
            )
                
            db.session.add(device_details)
            db.session.commit()
            
            auth_token = create_access_token(identity=user.id, fresh=True)
            
            refresh_token = create_refresh_token(user.id)
            
            user_data = {
                'id':user.id,
                'name':user.name,
                'user_name':user.user_name,
                'profile_image':user.profile_image,
                'email':user.email,
                'dob':user.dob,
                'current_currency':user.current_currency,
                'device_id':user.device_ids,
                'created_at':str(user.created_at)
            }
            
            response = jsonify({
                'status': 'SUCCESS',
                'code': 200,
                'message': 'User Created SuccessFully ...',
                'data':{
                    'token':auth_token,
                    'refresh_token':refresh_token,
                    'user':user_data,
                    }
            }), 200
        
        
    except Exception as e:
        print(f"\n\n\n Error {e} \n\n\n")
        response = jsonify({
            'status': 'ERROR',
            'code': 910,
            'message': f'Error {e} while creating user.'
        }), 500
    finally:
        db.session.close()
    return response


def reorder_username(username):
    # Split the username into parts
    reorder_usernames = []
    
    if '_' in username:
        parts = username.split("_")
        if len(parts) >= 2:
            reordered_username = f"{parts[1]}_{parts[0]}"
            reorder_usernames.append(reordered_username)
    if '@' in username:
        parts = username.split("@")
        if len(parts) >= 2:
            reordered_username = f"{parts[1]}@{parts[0]}"
            reorder_usernames.append(reordered_username)
    if '-' in username:
        parts = username.split("-")
        if len(parts) >= 2:
            reordered_username = f"{parts[1]}-{parts[0]}"
            reorder_usernames.append(reordered_username)
    return reorder_usernames


def check_username(username):
    
    exists = db.session.query(User.user_name).filter(User.user_name == username).first()

    if exists:
        return False
    else:
        return True
    
@jwt_required()
def suggest_usernames():
    try:
        user_id = get_jwt_identity()
        username = request.args.get('user_name')
        
        suggestions = []

        # reordered_username = reorder_username(username)

        # for user_name in reordered_username:
        #     suggestions.append(user_name)

        # Check if the provided username can be reordered
        availability = check_username(username)
        
        if availability:
            response = jsonify({
                'status': 'SUCCESS',
                'code': 404,
                'message': 'available'
            }), 404
        else:
            user = db.session.query(User).filter(User.id == user_id).first()
            if user.name != None or user.name != '':
                name = user.name.split(' ')
            email = user.email.split('@')
            
            suggestions.append(f"{name[0].lower()}{name[1].lower()}")
            suggestions.append(f"{email[0]}")
            
            if len(name) >= 2:
                first_name, last_name = name[0], name[-1]
                suggestions.append(f"{last_name[0].lower()}{first_name.lower()}")
                suggestions.append(f"{first_name.lower()}{last_name[0].lower()}")

            for _ in range(4):
                randon_number = random.randint(111,999)
                numbered_username = f"{username}{randon_number}"
                suggestions.append(numbered_username)
            
            for user_name in suggestions:
                exists = db.session.query(User).filter(User.user_name == user_name).first()
                
                if exists:
                    suggestions.remove(exists.user_name)
            print(f"\n\n\n suggestions { suggestions } \n\n\n")
                    

            response = jsonify({
                'status': 'SUCCESS',
                'code': 200,
                'message': 'Not Available check suggested user_name list',
                'data': suggestions
            }), 200
            
    except Exception as e:
        print(f"\n\n\n Error {e} \n\n\n")
        response = jsonify({
            'status': 'ERROR',
            'code': 910,
            'message': f'Error {e} while creating user.'
        }), 500
    finally:
        db.session.close()
    return response
        
    

@jwt_required()
def update_user():
    try:
        user_id = get_jwt_identity()
        params = request.form
        
        user = db.session.query(User).filter(User.id == user_id).first()
        
        user.name = params.get('name')
        user.current_currency = params.get('current_currency','INR',type=str)
        user.user_name = params.get('user_name')
        
        if params.get('email'):
            user.email = params.get('email')
        
        if params.get('phone_number'):
            user.phone_number = params.get('phone_number')
            
        if params.get('dob'):
            if user.dob == '' or user.dob == None:
                user.dob = params.get('dob')
            
        
        if request.files:
            if request.files['profile_image'] != None:
                profile_image = upload_image(request.files['profile_image'])
                user.profile_image = profile_image
            
        db.session.commit()
        
        response = jsonify({
            'status': 'SUCCESS',
            'code': 200,
            'message': 'User Profile Updated',
        }), 200
    
        
    except Exception as e:
        if 'user_user_name_key' in str(e):
            message = "Username already Taken"
        elif 'user_phone_number_key' in str(e):
            message = "Phone number already exists. Please use a different phone number."
        elif 'user_email_key' in str(e):
            message = "Email already exists. Please use a different Email."
        else:
            message = e
        print(f"\n\n\n Error {message} \n\n\n")
        response = jsonify({
            'status': 'ERROR',
            'code': 500,
            'message': message
        }), 500
    finally:
        db.session.close()
    return response


@jwt_required()
def get_user_profile():
    try:
        user_id = get_jwt_identity()
        
        user = db.session.query(User).filter(User.id == user_id).first()
        
        user_data = {
            'id': user.id,
            'name':user.name,
            'user_name':user.user_name,
            'profile_image':user.profile_image,
            'email':user.email,
            'phone_number':user.phone_number,
            'dob':user.dob,
            'current_currency':user.current_currency,
            'created_at':str(user.created_at),
        }
        
        response = jsonify({
                'status': 'SUCCESS',
                'code': 200,
                'message': 'Get User Profile Data',
                'data': user_data
            }), 200
    except Exception as e:
        print(f"\n\n\n Error {str(e)} \n\n\n")
        response = jsonify({
            'status': 'ERROR',
            'code': 500,
            'message': str(e)
        }), 500
    finally:
        db.session.close()
    return response

@jwt_required()
def search_user():
    try:
        search_query = request.args.get('query', '', type=str)
        
        searched_users = db.session.query(User).filter(
            or_(
                User.name.ilike("%{}%".format(search_query)),
                User.user_name.ilike("%{}%".format(search_query)),
                User.email.ilike("{}%".format(search_query)),
                User.phone_number.ilike("{}%".format(search_query)),
            )
            ).all()
        
        if searched_users != []:
            
            user_data = [
                {
                    'id': user.id,
                    'name':user.name,
                    'user_name':user.user_name,
                    'profile_image':user.profile_image,
                } for user in searched_users
            ]
            
            response = jsonify({
                'status': 'SUCCESS',
                'code': 200,
                'message': 'Get User Profile Data',
                'data': user_data
            }), 200
        else:
            response = jsonify({
                    'status': 'Not Found',
                    'code': 404,
                    'message': 'Searched User Not Found',
            }), 404
        
        
    except Exception as e:
        print(f"\n\n\n Error {str(e)} \n\n\n")
        response = jsonify({
            'status': 'ERROR',
            'code': 500,
            'message': str(e)
        }), 500
    finally:
        db.session.close()
    return response
    

@jwt_required()
def current_email_verification():
    try:
        user_id = get_jwt_identity()
        
        curr_email = db.session.query(User.email).filter(User.id == user_id).first()
        
        otp_num = random.randint(10000, 99999)
        
        recipient = curr_email.email
        subject = "Email OTP Verification"
        message_body = f"""
Hello Just Split User,

You've requested to Email OTP Verification code. Please find your 5-digit OTP below:

OTP Code: [ {otp_num} ]

Please use this OTP to complete your email verification process within the app.

If you didn't request this OTP, you can ignore this message. For any questions or assistance, please contact our support team.

Best regards,
The Just Split Team
        """
        response = jsonify({
                'status': 'SUCCESS',
                'code': 200,
                'message': 'OTP Sent SuccessFully !',
                'data':{
                    'otp':otp_num
                }
            }), 200
            
        sent_mail = send_email(recipient,subject,message_body)
    
    except Exception as e:
        print(f"\n\n\n Error {str(e)} \n\n\n")
        response = jsonify({
            'status': 'ERROR',
            'code': 500,
            'message': str(e)
        }), 500
    finally:
        db.session.close()
    return response


@jwt_required()
def new_email_verification():
    try:
        user_id = get_jwt_identity()
        params = request.json
        
        email = params.get('email')
        
        exists = db.session.query(User).filter(User.id == user_id).first()
        existing_emails = db.session.query(User.email).all()
        for i in existing_emails:
            if i.email == email:
                already_taken = True
                break
            else:
                already_taken = False
        if exists.email == email:
            response = jsonify({
                'status': 'SUCCESS',
                'code': 200,
                'message': "Old Email and New Email are Not be Same. Please Try a Different Email"
            }), 200
        elif already_taken:
            response = jsonify({
                'status': 'SUCCESS',
                'code': 200,
                'message': "Email Already Taken. Please Try a Different Email"
            }), 200
        else:
            otp_num = random.randint(10000, 99999)
        
            recipient = email
            subject = "Email OTP Verification"
            message_body = f"""
Hello Just Split User,

You've requested to Email OTP Verification code. Please find your 5-digit OTP below:

OTP Code: [ {otp_num} ]

Please use this OTP to complete your email verification process within the app.

If you didn't request this OTP, you can ignore this message. For any questions or assistance, please contact our support team.

Best regards,
The Just Split Team
            """
            response = jsonify({
                    'status': 'SUCCESS',
                    'code': 404,
                    'message': 'OTP Sent SuccessFully !',
                    'data':{
                        'otp':otp_num
                    }
                }), 404
            
            sent_mail = send_email(recipient,subject,message_body)
            
            
        
    except Exception as e:
        if 'user_email_key' in str(e):
            message = "Email Already Taken"
        else:
            message = e
        print(f"\n\n\n Error {message} \n\n\n")
        response = jsonify({
            'status': 'ERROR',
            'code': 500,
            'message': message
        }), 500
    finally:
        db.session.close()
    return response
    

def email_verification():
    try:
        device_id = request.args.get('device_id',None,type=str)
        device_name = request.args.get('device_name',None,type=str)
        otp_num = random.randint(10000, 99999)
        params = request.json
        
        recipient = params.get('recipient')
        subject = params.get('subject')
        message_body = f"""
Hello there, Amazing Soul! ✨

Buckle up, because your JustSplit adventure is about to begin! 🚀 We're absolutely thrilled to welcome you to our family. 🌈🎉

*Drum roll, please! 🥁* Here's your magical key to unlock the wonders of JustSplit:



🔮 *Your Unique Verification Code:* {otp_num} 🔮



But wait, there's more! 💌

We've got a little sprinkle of fairy dust to make your day even brighter: a pinch of excitement, a dash of smiles, and a whole lot of love! 💖

So, here's what to do next:
1. Open up your JustSplit app.
2. Find the enchanted "Verification" section.
3. Gently type in your magical code and let the magic unfold!

And remember, if you didn't wave your wand to create this verification, no worries at all. Just ignore this email and carry on with your magical day! 🌟✨

Oh, and if you ever need a little help, a friendly wizard from our support team is just a message away at support@justsplit.app. They're ready to make your experience as enchanting as can be!

Adventure awaits, dear friend! 🌠
Your Friends at JustSplit.
        """
        try:
            user = db.session.query(User).filter(User.email == recipient).first()
            
            if user:
                if device_id:
                    if user.device_ids != None:
                        exist_device = []
                        for device in user.device_ids:
                            exist_device.append(device)
                        if not device_id in exist_device:
                            exist_device.append(device_id)
                            user.device_ids = exist_device
                    else:
                        user.device_ids = [device_id]
                db.session.commit()
                auth_token = create_access_token(identity=user.id, fresh=True)
                
                refresh_token = create_refresh_token(user.id)
                
                device_details = UserLogin(
                    user_id = user.id,
                    device_id = device_id,
                    device_name = device_name,
                    logged_in_status = True,
                    login_at = datetime.now()
                )
                
                db.session.add(device_details)
                db.session.commit()
            
                user_data = {
                    'id':user.id,
                    'name':user.name,
                    'user_name':user.user_name,
                    'profile_image':user.profile_image,
                    'email':user.email,
                    'dob':user.dob,
                    'current_currency':user.current_currency,
                    'device_id':user.device_ids,
                    'created_at':str(user.created_at),
                }
                message = 'User Already Exists'
                response = jsonify({
                    'status': 'SUCCESS',
                    'code': 200,
                    'message': message,
                    'data':{
                        'user' : user_data,
                        'token':auth_token,
                        'refresh_token':refresh_token,
                        'otp':otp_num
                    }
                }), 200
            else:
                response = jsonify({
                'status': 'Not Found',
                'code': 404,
                'message': 'User Not Found',
                'data':{
                    'otp':otp_num
                }
            }), 404
            
            sent_mail = send_email(recipient,subject,message_body)
            
        except Exception as e:
            print(f"\n\n\n Error {e} \n\n\n")
            response = jsonify({
                'status': 'ERROR',
                'code': 500,
                'message': f'Error {e}'
            }), 500
        
    except Exception as e:
        print(f"\n\n\n Error {e} \n\n\n")
        response = jsonify({
            'status': 'ERROR',
            'code': 500,
            'message': f'Error {e}'
        }), 500
    finally:
        db.session.close()
    return response

@jwt_required()
def log_out():
    try:
        user_id = get_jwt_identity()
        device_id = request.args.get('device_id')
        
        # add logout time and status in user_login table
        
        login_info = db.session.query(UserLogin).filter(
            UserLogin.user_id == user_id,
            UserLogin.device_id == device_id,
            UserLogin.logout_at == None,
            UserLogin.logged_in_status == True
            ).first()
        
        login_info.logout_at = datetime.now()
        login_info.logged_in_status = False
        
        db.session.commit()
        
        response = jsonify({
            'status': 'SUCCESS',
            'code': 200,
            'message': "Logged Out SuccessFully...",
        }), 200
        
    except Exception as e:
        print(f"\n\n\n Error {e} \n\n\n")
        response = jsonify({
            'status': 'ERROR',
            'code': 910,
            'message': f'Error {e}'
        }), 500
        
    finally:
        db.session.close()
        
    return response



def upload_image(image):
    # image = request.files['image']
    # Generate file
    file_id = uuid.uuid4().hex
    image_file_extension = os.path.splitext(image.filename)[
        1][1:]

    file_name = "Profile/{0}.{1}".format(
                file_id, image_file_extension)

    # Upload the file
    s3_file = upload_image_to_s3(
        file_name, image, image_file_extension)

    image_url = 'https://{0}.s3.amazonaws.com/{1}'.format(
        config('AWS_BUCKET_NAME'), s3_file)
    
    return image_url

