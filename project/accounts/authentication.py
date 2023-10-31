from django.contrib.auth.models import User

class EmailAuthBackend:

    def authentication(self,request,email=None,password=None):
        try:
            user=User.objects.get(email=email)
            if User.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
        

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None