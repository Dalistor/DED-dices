import hashlib

secret_key = 'A#2:(izWv%WuBi1u\+vwfL$t,'

def hash_id(id):
    hash_obj = hashlib.sha256((secret_key + str(id)).encode('utf-8'))
    hash_id = hash_obj.hexdigest()

    return f'{id}-{hash_id}'
    
def check_hash(hash):
    id, hash = hash.split('-')

    hash_obj = hashlib.sha256((secret_key + str(id)).encode('utf-8'))
    hash_id = hash_obj.hexdigest()

    if hash_id == hash:
        return True
    else:
        return False