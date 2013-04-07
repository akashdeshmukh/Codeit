from codeit.models import User
a = User.objects.all()
for i in a:
    i.total_points = 0
    i.is_active = False
    i.save()
