import os
from uuid import uuid4

def rename_serverimagefile_to_uuid(instance, filename):
    upload_to = f'servers/'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex

    filename = f'server_{instance}_{uuid}.{ext}'
    
    return os.path.join(upload_to, filename)

def rename_chatimagefile_to_uuid(instance, filename):
    upload_to = f'chats/{instance}/'
    ext = filename.split('.')[-1]
    uuid = uuid4().hex

    filename = f'{uuid}.{ext}'
    
    return os.path.join(upload_to, filename)