from pillapp.models import User, Prescription, medicine

def test_user():
    User.objects.create(
        user_name = 'user0001',
        user_pw = 'password0001'
    )

def test_imgpath():
    base_dir = ''
    Prescription.objects.create(
        p_imgpath = '',
        user_id = User.objects.get(pk=1)
    )

