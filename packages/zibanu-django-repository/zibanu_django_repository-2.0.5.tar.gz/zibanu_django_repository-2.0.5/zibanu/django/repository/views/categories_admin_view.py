# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2025. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2025. Todos los derechos reservados.

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         18/02/25
# Project:      Zibanu Django
# Module Name:  admin_categories_view
# Description:
# ****************************************************************
import logging
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request
from zibanu.django.lib.utils import object_to_list
from zibanu.django.repository.models import Category


class CategoriesAdminView(admin.ModelAdmin):
    """ Category Model class."""
    list_display = ("name", "parent", "published", "level")
    fieldsets = (
        (None, {"fields": ("name", "parent")}),
        (_("Features"), {
            "fields": ["gen_thumb", "gen_ml", "extract_metadata", "extract_tables", "file_types", ("sort_by", "sort_type")],
            "classes": ["collapse"],
        }),
        (_("Status"), {"fields": ("published", )})
    )
    actions = ["publish_categories", "unpublish_categories"]
    list_filter = ["parent", "level"]
    sortable_by = ["name", "published", "level"]
    list_select_related = ["parent"]
    list_per_page = 20

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Override Method to set a queryset for "parent" foreign key.

        Parameters
        ----------
        db_field: Field
            Model field object to use as foreign key.
        request: HttpRequest
            HTTP Request object.
        kwargs: dict
            Keyword arguments passed to `ForeignKey`.

        Returns
        -------
        FormField
        """
        if db_field.name == "parent":
            kwargs["queryset"] = Category.objects.get_only_parents(published=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.action(description=_("Publish the selected categorie/s."))
    def publish_categories(self, request: Request, queryset: QuerySet) -> None:
        """
        Method to publish selected categories and its children.
        Parameters
        ----------
        request:
            HTTP request object

        queryset:
            Set of selected categories to do the action on.

        Returns
        -------
        None
        """
        queryset.update(published=True)
        for child in queryset:
            Category.objects.set_children_publish(child.id, True)

    @admin.action(description=_("Unpublish the selected categorie/s."))
    def unpublish_categories(self, request: Request, queryset: QuerySet) -> None:
        """
        Method to unpublish selected categories and its children.
        Parameters
        ----------
        request:
            HTTP request object
        queryset:
            Set of selected categories to do the action on.

        Returns
        -------
        None
        """
        with transaction.atomic():
            queryset.update(published=False)
            for child in queryset:
                Category.objects.set_children_publish(child.id, False)


    def save_model(self, request, obj, form, change):
        """ Override save model method. """

        try:
            super().save_model(request, obj, form, change)
        except ValidationError as exc:
            error_list = object_to_list(exc.messages)
            if len(error_list) > 0:
                for message_error in error_list:
                    messages.error(request, message_error)
                    logging.error(message_error)
        except Exception as exc:
            messages.error(request, str(exc))
            logging.error(str(exc))
