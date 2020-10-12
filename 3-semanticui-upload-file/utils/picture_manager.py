# -*- coding:utf-8 -*-

def get_picture_list():
    import os
    picture_list = list() 
    path = os.getcwd()
    picture_name_list = os.listdir(path+"/static/pictures/") 
    for picture_name in picture_name_list :
        picture_list.append(dict(picture_name=picture_name))
    return picture_list
