from django.db import migrations

def create_default_roles(apps, schema_editor):
    Role = apps.get_model("users", "Role")
    default_roles = ["Admin", "Nurse", "Supplier", "Inventory Manager"]
    for role in default_roles:
        Role.objects.get_or_create(name=role)

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_roles),
    ]
