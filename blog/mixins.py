from django.db import models
from django.utils.text import slugify



class UniqueSlugMixin(models.Model):
    slug_from_field = None
    
    
    class Meta:
        abstract = True
        
        
    def _generate_unique_slug(self):
        base_value = getattr(self, self.slug_from_field)
        slug = slugify(base_value)
        unique_slug = slug
        ModelClass = self.__class__
        num = 1
        
        
        while ModelClass.objects.filter(slug = unique_slug).exclude(pk = self.pk).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
            
        return unique_slug
    
    
    def save(self, *args, **kwargs):
        if not self.slug and self.slug_from_field:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)