from aip import AipImageCensor
from queue import Queue
import os
from threading import Thread


""" 你的 APPID AK SK """
APP_ID = '16417834'
API_KEY = 'Mrr6fjs7vg95aslKyMKpfa2k'
SECRET_KEY = 'EsMycqjPXC4mnauARQyGlESFSgxfOexa'

client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)


def check_file_content(file_path, q):
    """ 读取图片 """
    fp = open(file_path, 'rb')
    """ 调用色情识别接口 """
    result = client.imageCensorUserDefined(fp.read())
    if result['conclusion'] == '不合规':
        q.put(False)
    else:
        q.put(True)


def check_image(file_path):
    q = Queue()
    t = Thread(target=check_file_content, args=[file_path, q])
    t.start()
    return q.get()
