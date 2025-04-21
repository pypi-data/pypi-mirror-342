from django.db import migrations, models
from django.db.models.functions import Lower


# Copyright (c) 2023 Carlton Gibson
# This migration is taken from the fantastic project `django-unique-user-email` created by Carlton Gibson.
# https://github.com/carltongibson/django-unique-user-email/


class CustomAddConstraint(migrations.AddConstraint):
    """
    Override app_label to target auth.User
    """

    def state_forwards(self, app_label, state):
        state.add_constraint("auth", self.model_name_lower, self.constraint)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model("auth", self.model_name)
        if self.allow_migrate_model(schema_editor.connection.alias, model):
            schema_editor.add_constraint(model, self.constraint)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        model = to_state.apps.get_model("auth", self.model_name)
        if self.allow_migrate_model(schema_editor.connection.alias, model):
            schema_editor.remove_constraint(model, self.constraint)


class Migration(migrations.Migration):
    dependencies = [
        ("django_solomon", "0002_magiclink_ip_address"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        CustomAddConstraint(
            model_name="user",
            constraint=models.UniqueConstraint(
                Lower("email"),
                name="unique_user_email"
            ),
        ),
    ]
