from datetime import datetime

from .models import Profile

def year(request):
    current_year = datetime.now().year
    return {'current_year': current_year}


def user_role(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            role = profile.role
        except Profile.DoesNotExist:
            role = None
    else:
        role = None
    return {'user_role': role}
