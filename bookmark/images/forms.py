from django import forms
from urllib import request
from django.core.files.base import ContentFile
from pytils.translit import slugify

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url': forms.HiddenInput, }
    # Пользователи не будут вручную заполнять адрес.
    # Вместо этого мы добавим JavaScript-инструмент для выбора картинки на любом
    # постороннем сайте, а наша форма будет получать URL изображения в качестве параметра.
    # Мы заменили виджет по умолчанию для поля url и  используем HiddenInput.
    # Этот виджет формируется как input элемент с атрибутом type="hidden".
    # Мы сделали это для того, чтобы пользователи не видели поле url.

    def clean_url(self):
        url = self.cleaned_data['url']
        # 1) получает значение поля url, обращаясь к атрибуту формы cleaned_data;
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        # 2) разделяет URL, чтобы получить расширение файла и проверить, является
        # ли оно корректным. Если это не так, форма генерирует исключение ValidationError.
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'The given URL does not match valid image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        # создает объект image, вызвав метод save() с аргументом commit=False;
        image_url = self.cleaned_data['url']
        # получает URL из атрибута cleaned_data формы;
        image_name = '{}.{}'.format(
            slugify(image.title), image_url.rsplit('.', 1)[1].lower())
            # генерирует название изображения, совмещая слаг и расширение картинки;
        # Скачиваем изображение по указаному адресу
        response = request.urlopen(image_url)
        # использует Python-пакет urllib, чтобы скачать файл картинки, и вызывает метод save() 
        # поля изображения, передавая в него объект скачанного файла, ContentFile.
        image.image.save(image_name, ContentFile(response.read()), save=False)
        if commit:
            image.save()
            # при переопределении метода важно оставить стандартное поведение,
            # поэтому сохраняем объект изображения в базу данных только в том случае, 
            # если commit равен True.
        return image
