from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('safezone_app', '0003_alter_zonas_options'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
            CREATE TABLE IF NOT EXISTS zonas (
                id bigserial PRIMARY KEY,
                nombre_zona varchar(100) NOT NULL UNIQUE,
                zona_geografica varchar(13) NOT NULL,
                activo integer NULL,
                fecha_creacion timestamp with time zone NOT NULL
            );
            '''
        )
    ]
