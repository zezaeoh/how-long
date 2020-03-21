from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)

        social_app_name = sociallogin.account.provider.upper()

        if social_app_name == "FACEBOOK":
            User.objects.get_or_create_facebook_user(user_pk=user.pk, extra_data=extra_data)

        elif social_app_name == "NAVER":
            User.objects.get_or_create_naver_user(user_pk=user.pk, extra_data=extra_data)
