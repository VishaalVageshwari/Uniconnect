def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = user.profile
        profile.facebook = {'link': response.get('link'),
                            'friends': response.get('friends')
        }
        profile.save()