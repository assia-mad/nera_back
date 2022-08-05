from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.address = data.get('address')
        user.tel= data.get('tel')
        user.gender= data.get('gender')
        user.age = data.get('age')
        user.save()
        return user