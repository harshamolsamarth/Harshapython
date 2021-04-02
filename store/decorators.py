from django.shortcuts import redirect

def customer_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        #if request.session.get('user_obj') == 'logged_in':

        if request.session.get('user_obj') == True:
            return redirect('homepage')
        else:
            
            return redirect('signup')
    return wrapper_func

