from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order, CustomizationDetails, PaymentProof, Product, WebsiteSettings, Banner


class CustomOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'mobile_number', 'email', 'delivery_address']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'mobile_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'XXXXXXXXXX (10 digits)',
                'maxlength': '10',
                'size': '10',
                'inputmode': 'numeric',
                'pattern': '[0-9]{10}',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com (optional)'
            }),
            'delivery_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter complete delivery address with pincode'
            }),
        }
    
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number', '').strip()
        
        # Remove any spaces or special characters, keep only digits
        mobile_digits = ''.join(filter(str.isdigit, mobile_number))
        
        # Check if it's exactly 10 digits
        if len(mobile_digits) != 10:
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        
        return mobile_digits


class CustomizationForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1'
        })
    )
    
    class Meta:
        model = CustomizationDetails
        fields = ['custom_text', 'custom_image', 'notes']
        widgets = {
            'custom_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter custom text (e.g., name, quote)'
            }),
            'custom_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special instructions or notes'
            }),
        }


class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = PaymentProof
        fields = ['screenshot', 'upi_transaction_id']
        widgets = {
            'screenshot': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'required': True
            }),
            'upi_transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UPI Transaction ID (optional)'
            }),
        }


class OrderTrackingForm(forms.Form):
    tracking_info = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your mobile number or email',
            'autocomplete': 'off'
        }),
        help_text='Enter the mobile number or email used when placing the order'
    )


# Admin Forms
class AdminLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Username',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Password',
            'autocomplete': 'current-password'
        })
    )


class ProductForm(forms.ModelForm):
    # Add image fields for multiple images
    image_1 = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Primary product image (required)'
    )
    image_2 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Additional image (optional)'
    )
    image_3 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Additional image (optional)'
    )
    image_4 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        help_text='Additional image (optional)'
    )
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'base_price', 'customization_type', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Product description'
            }),
            'base_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'customization_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class WebsiteSettingsForm(forms.ModelForm):
    class Meta:
        model = WebsiteSettings
        fields = [
            'site_name', 'tagline', 'website_url', 'contact_phone', 'contact_email', 
            'upi_id', 'payment_qr_code', 'whatsapp_number', 'address', 'instagram_url', 
            'facebook_url', 'telegram_bot_token', 'telegram_chat_id', 'enable_telegram_notifications',
            'processing_time_days', 'delivery_time_days'
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yoursite.com'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'upi_id': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_qr_code': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control'}),
            'telegram_bot_token': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890:ABCdefGHIjklMNOpqrsTUVwxyz'}),
            'telegram_chat_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123456789'}),
            'enable_telegram_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'processing_time_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'delivery_time_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'subtitle', 'banner_type', 'image', 'link_url', 'link_text', 'is_active', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'banner_type': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'link_url': forms.URLInput(attrs={'class': 'form-control'}),
            'link_text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }