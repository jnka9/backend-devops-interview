import django.contrib.postgres.indexes
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        TrigramExtension(),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(fields=["email"], name="user_email_idx"),
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(fields=["is_published", "-created_at"], name="post_pub_created_idx"),
        ),
        migrations.AddIndex(
            model_name="post",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.indexes.OpClass("title", name="gin_trgm_ops"),
                name="post_title_trgm_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="post",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.indexes.OpClass("body", name="gin_trgm_ops"),
                name="post_body_trgm_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="comment",
            index=models.Index(fields=["post", "created_at"], name="comment_post_created_idx"),
        ),
        migrations.RunSQL(
            sql=(
                "CREATE INDEX IF NOT EXISTS blog_post_tags_tag_post_idx "
                "ON blog_post_tags (tag_id, post_id)"
            ),
            reverse_sql="DROP INDEX IF EXISTS blog_post_tags_tag_post_idx",
        ),
    ]
