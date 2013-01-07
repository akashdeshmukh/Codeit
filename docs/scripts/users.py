from codeit.models import User

for i in range(200):
    u = User()
    u.first_name = "-"
    u.last_name = "-"
    u.receipt_no = i
    u.total_points = 0
    u.year = "-"
    u.isactive = False
    u.save()
