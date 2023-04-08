from django.contrib.auth.models import User
users=["Maria", "Ana", "Rui", "Rita", "Joao", "Ines"]
def create_users():
    for name in users:
        mail = name.lower() + "@iscte.pt"
        password = "pass"
        User.objects.create_user(name, mail, password)

create_users()