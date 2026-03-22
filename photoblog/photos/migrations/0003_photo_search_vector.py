from django.contrib.postgres.search import SearchVectorField
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("photos", "0002_alter_photo_options_alter_photo_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="photo",
            name="search_vector",
            field=SearchVectorField(editable=False, null=True),
        ),
        migrations.RunSQL(
            sql="""
CREATE TRIGGER photos_update_search_trigger
BEFORE INSERT OR UPDATE OF title, description ON photos_photo
FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(
    search_vector, 'pg_catalog.simple', title, description);
UPDATE photos_photo SET title = title;""",
            reverse_sql=(
                "DROP TRIGGER IF EXISTS photos_update_search_trigger ON photos_photo;"
            ),
        ),
    ]
