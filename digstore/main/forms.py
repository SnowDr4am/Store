from django.forms import ModelForm, TextInput, Textarea, FileInput, NumberInput, Select
from .models import Product
from django.core.exceptions import ValidationError
from PIL import Image
import mimetypes
import os

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image", "category", "combinations"]
        widgets = {
            "name": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите название товара",
                "style": "background-color: #2a2a2a; color: #e0e0e0; border: 1px solid #00ff99;"
            }),
            "description": Textarea(attrs={
                "class": "form-control",
                "placeholder": "Введите описание товара",
                "style": "background-color: #2a2a2a; color: #e0e0e0; border: 1px solid #00ff99;"
            }),
            "price": NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Введите цену",
                "step": "0.5",
                "min": "0",
                "style": "background-color: #2a2a2a; color: #e0e0e0; border: 1px solid #00ff99;"
            }),
            "image": FileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
                "style": "background-color: #2a2a2a; color: #e0e0e0; border: 1px solid #00ff99;"
            }),
            "category": Select(attrs={
                "class": "form-select",
                "style": "background-color: #2a2a2a; color: #e0e0e0; border: 1px solid #00ff99;"
            }),
            "combinations": Textarea(attrs={
                "class": "form-control",
                "placeholder": "Введите комбинации, разделяя запятыми (например: ABC123, XYZ789)",
                "rows": 4,
                "style": "background-color: #2a2a2a; color: #e0e0e0; border: 1px solid #00ff99;"
            }),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 2 * 1024 * 1024:
                raise ValidationError("Изображение слишком большое (максимум 2 МБ).")

            mime_type, _ = mimetypes.guess_type(image.name)
            allowed_mimes = ['image/jpeg', 'image/png']
            if mime_type not in allowed_mimes:
                raise ValidationError("Разрешены только изображения JPEG или PNG.")

            ext = os.path.splitext(image.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png']:
                raise ValidationError("Недопустимое расширение файла. Используйте .jpg или .png.")

            try:
                img = Image.open(image)
                if img.size != (160, 160):
                    img = img.resize((160, 160), Image.LANCZOS)
                    image.file = img
            except Exception as e:
                raise ValidationError("Не удалось обработать изображение.")

        return image