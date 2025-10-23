from .models import CustomUser

def check_group(group_name,user_id) -> bool:
    try:
        #select * from CustomUser where id = x
        user = CustomUser.objects.get(id=user_id)
        return user.groups.filter(name=group_name).exists()
    except CustomUser.DoesNotExist:
        return False

def isAdmin(user_id) -> bool:
    return check_group('ADMIN',user_id)