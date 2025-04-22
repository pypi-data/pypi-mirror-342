import logging

from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from taggit.models import ContentType, Tag, TaggedItem
from wagtail.models import Page

from wagtail_tagmanager.utils import get_page_tagging_model


class ManagedTag(Tag):
    class Meta:
        proxy = True
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    @cached_property
    def page_tag_model(self):
        return get_page_tagging_model()

    def _get_valid_tagged_items(self):
        valid_content_types = {
            ct.id: ct
            for ct in ContentType.objects.all()
            if ct.model_class() is not None
        }

        return TaggedItem.objects.filter(
            tag=self, content_type_id__in=valid_content_types.keys()
        ).select_related("content_type")

    def object_count_number(self):
        return getattr(self, "object_count_number", 0)

    def get_tagged_objects(self):
        """
        Return a list of all objects (across models) that are tagged with this tag.
        Only includes objects with valid model classes and existing instances.
        """
        page_ids = self.page_tag_model.objects.filter(tag=self).values_list(
            "content_object_id", flat=True
        )
        pages = Page.objects.filter(id__in=page_ids).specific()

        others = []
        for item in self._get_valid_tagged_items():
            try:
                obj = item.content_object
                if obj:
                    others.append(obj)
            except Exception:
                logging.exception("Object is deleted/missing")

        return list(pages) + others

    object_count_number.short_description = "Objects Used On"

    def __str__(self):
        return self.name
