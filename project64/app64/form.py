from django import forms


class LoginForm(forms.Form):
    UserName = forms.CharField(min_length=3, max_length=16,
                               error_messages={'required': u'用户名不能为空!'})
    PassWord = forms.CharField(min_length=6, max_length=16)



