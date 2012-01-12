from gilbi.mistrael.models.user import User
from gilbi.mistrael.models.seller import Seller
from gilbi.mistrael.models.manager import Manager

def create_session(request, id):
    if 'user_id' not in request.session:
        request.session['user_id'] = id

def validate_session(request):
    if 'user_id' in request.session and User.objects.filter(id=request.session['user_id']).exists() == True:
        return True
    else:
        request.session.flush()
        return False

def validate_seller_session(request):
    if Seller.objects.filter(id=request.session['user_id']).exists() == True:
        return True
    else:
        return False

def validate_manager_session(request):
    if Manager.objects.filter(id=request.session['user_id']).exists() == True:
        return True
    else:
        return False
        
def destroy_session(request):
    request.session.flush()