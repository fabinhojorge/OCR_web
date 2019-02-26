from django.db import models
from core import utils
import hashlib
from PIL import Image
import pytesseract


class ImageFileManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(models.Q(internal_reference__icontains=query) |
                                          models.Q(name__icontains=query) |
                                          models.Q(description__icontains=query)
                                          )


class ImageFile(models.Model):

    name = models.CharField("Name", max_length=100)
    internal_reference = models.CharField("Internal Reference", max_length=100, editable=False)
    description = models.TextField("Description", blank=True, null=True)
    image = models.ImageField(upload_to="OCR_image/input/", verbose_name="Input Image")
    create_at = models.DateTimeField("Create at", auto_now_add=True)
    updated_at = models.DateTimeField("Update at", auto_now=True)

    def __str__(self):
        return "{0:03d} - {1}".format(self.id, self.image)

    def execute_and_save_ocr(self):
        img = Image.open(self.image)
        print("The image {0} was opened.".format(self.image))
        txt = pytesseract.image_to_string(img)
        print('OCR: \n{0}\n'.format(txt))
        ocr_txt = OCRText()
        ocr_txt.image = self
        ocr_txt.text = txt
        ocr_txt.lang = "EN"
        ocr_txt.save()
        return ocr_txt

    """
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('course_details', args=[], kwargs={'slug': self.slug})

    """

    def save(self, *args, **kwargs):

        if not self.internal_reference:
            random_value = utils.random_value_generator(size=20)
            while ImageFile.objects.filter(internal_reference=random_value).exists():
                random_value = utils.random_value_generator(size=20)
            hash_value = hashlib.md5(bytes(str(self.id) + str(random_value), 'utf-8'))
            self.internal_reference = hash_value.hexdigest()
        super(ImageFile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "ImageFile"
        verbose_name_plural = "ImageFiles"
        ordering = ['id']

    objects = ImageFileManager()


class OCRText(models.Model):
    text = models.TextField("OCR text", blank=True)
    lang = models.TextField("Language", default="EN")
    image = models.ForeignKey('ImageFile', on_delete=models.CASCADE)
    create_at = models.DateTimeField("Create at", auto_now_add=True)
    updated_at = models.DateTimeField("Update at", auto_now=True)

    def __str__(self):
        return "{0:03d} - {1}".format(self.id, self.image.internal_reference)


    class Meta:
        verbose_name = "OCRText"
        verbose_name_plural = "OCRTexts"
        ordering = ['id']
