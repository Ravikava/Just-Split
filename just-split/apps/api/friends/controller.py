from flask import request,jsonify
from flask_jwt_extended import (
    create_access_token,create_refresh_token,
    jwt_required,get_jwt_identity
)

from apps import db
from apps.database.models import User,FriendRequest
from apps.helpers.utils import get_or_create
from datetime import datetime

@jwt_required()
def other_user_profile(id):
    try:
        user_id = get_jwt_identity()
        
        user = db.session.query(User).filter(User.id == user_id).first()
        
        searched_user = db.session.query(User).filter(User.id == id).first()
        
        check_request =  db.session.query(FriendRequest).filter(
            FriendRequest.receiver_id == user_id,
            FriendRequest.sender_id == id,
            FriendRequest.request_status == 'pending'
        ).first()
        
        my_request =  db.session.query(FriendRequest).filter(
            FriendRequest.receiver_id == id,
            FriendRequest.sender_id == user_id,
            FriendRequest.request_status == 'pending'
        ).first()
        
        if searched_user:
            if user.friends != None and id in user.friends:
                if searched_user.phone_number:
                    masked_number = "X" * (len(searched_user.phone_number) - 3) + searched_user.phone_number[-3:]

                user_data = {
                    'id': searched_user.id,
                    'name':searched_user.name,
                    'user_name':searched_user.user_name,
                    'profile_image':searched_user.profile_image,
                    'email':searched_user.email,
                    'phone_number':masked_number if searched_user.phone_number else None,
                    'is_friend':True
                }
            else:
                user_data = {
                    'id': searched_user.id,
                    'name':searched_user.name,
                    'user_name':searched_user.user_name,
                    'profile_image':searched_user.profile_image,
                    'is_friend':False,
                    'is_requested': True if check_request != None else False,
                    'my_request': True if my_request != None else False,
                }
            response = jsonify({
                'status': 'SUCCESS',
                'code': 200,
                'message': 'Get Other User Profile Data',
                'data': user_data
            }), 200
        else:
            response = jsonify({
                'status': 'NOT FOUND',
                'code': 404,
                'message': 'User Not Found',
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
def send_friend_request(receiver_id):
    try:
        user_id = get_jwt_identity()
        
        request,created = get_or_create(
            db.session,
            FriendRequest,
            sender_id = user_id,
            receiver_id = receiver_id,
            request_status = 'pending'
        )
        if not created:
            request.request_status = 'pending'
            request.created_at = datetime.now()
            db.session.commit()
        
        
        response = jsonify({
            'status': 'SUCCESS',
            'code': 200,
            'message': 'Friend Request Sent SuccessFully.. !',
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
def cancel_request(receiver_id):
    try:
        user_id = get_jwt_identity()
        
        request = db.session.query(FriendRequest).filter(
            FriendRequest.sender_id == user_id,
            FriendRequest.receiver_id == receiver_id,
            FriendRequest.request_status == 'pending'
        ).first()
        
        request.request_status = 'rejected'
        request.updated_at = datetime.now()
        
        db.session.commit()
        
        
        response = jsonify({
            'status': 'SUCCESS',
            'code': 200,
            'message': 'Request Canceled',
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
def get_pending_requests():
    try:
        user_id = get_jwt_identity()
        
        pending_requests = db.session.query(FriendRequest).filter(
            FriendRequest.receiver_id == user_id,
            FriendRequest.request_status == 'pending'
            ).all()
        
        
        user_data = [
            {
                'sender_id':user.sender_id,
                'sender_name': user.sender.name,
                'sender_username': user.sender.user_name,
                'sender_profile_image': user.sender.profile_image,
                'requested_at': str(user.created_at)
            } for user in pending_requests
        ]
        
        response = jsonify({
            'status': 'SUCCESS',
            'code': 200,
            'message': 'Get Pending Requests List',
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
def handle_friend_request():
    try:
        sender_id = request.args.get('sender_id',None)
        status = request.args.get('status',None)
        user_id = get_jwt_identity()
        
        user = db.session.query(User).filter(User.id == user_id).first()
        
        if sender_id and status:
            request_user = db.session.query(FriendRequest).filter(FriendRequest.sender_id == sender_id).first()
            
            if status == 'accepted':
                request_user.request_status = 'accepted'
                request_user.friendship_status = True
                request_user.updated_at = datetime.now()
                
                if user.friends != None:
                    exist_friends = []
                    for i in user.friends:
                        exist_friends.append(i)
                    exist_friends.append(int(sender_id))
                    user.friends = exist_friends
                else:
                    user.friends = [sender_id]
                
            if status == 'rejected':
                request_user.request_status = 'rejected'
                request_user.friendship_status = False
                request_user.updated_at = datetime.now()
            
            db.session.commit()
            
            
            response = jsonify({
                'status': 'SUCCESS',
                'code': 200,
                'message': f'Friend Request {status.upper()} .'
            }), 200
            
        else:
            response = jsonify({
                'status': 'SUCCESS',
                'code': 200,
                'message': 'Provide "sender_id" and "status" as query parameter'
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
def get_friends_list():
    try:
        user_id = get_jwt_identity()
        
        friends = db.session.query(User.friends).filter(User.id == user_id).first()

        if friends.friends:
            friends_data = db.session.query(
                User.id,
                User.name,
                User.profile_image
            ).filter(User.id.in_(friends.friends)).all()
        
            friends_list = [
                {
                    'id':user.id,
                    'name':user.name,
                    'profile_image':user.profile_image
                } for user in friends_data
            ]
        else:
            friends_list = []
        
        response = jsonify({
            'status': 'SUCCESS',
            'code': 200,
            'message': 'Get List of Friends',
            'data':friends_list
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
def remove_friend(friend_id):
    try:
        
        user_id = get_jwt_identity()
        
        user = db.session.query(User).filter(User.id == user_id).first()
        
        user_list = []
        for i in user.friends:
            user_list.append(i)
        if friend_id in user_list:
            user_list.remove(friend_id)
            user.friends = user_list
        
        friend_request_status = db.session.query(FriendRequest).filter(
            FriendRequest.receiver_id == user_id,
            FriendRequest.sender_id == friend_id,
            FriendRequest.request_status == 'accepted',
            FriendRequest.friendship_status == True
        ).first()
        
        friend_request_status.request_status = 'rejected'
        friend_request_status.friendship_status = False
        
        db.session.commit()
        
        response = jsonify({
            'status': 'SUCCESS',
            'code': 200,
            'message': 'Friend Removed SuccessFully..!'
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