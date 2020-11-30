from django.shortcuts import render


def allowed_groups(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # raw_groups = request.user.groups.only('name')
            raw_groups = request.user.groups.all()
            user_groups = set([group.name for group in raw_groups])

            if user_groups.intersection(set(allowed_roles)):
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'users/401_unauthorized.html')

            # group = None
            # if request.user.groups.exist():
            #     group = request.user.groups.all()[0].name
            # if group in allowed_roles:
            #     return view_func(request, *args, **kwargs)
            # else:
            #     return render(request, 'users/401_unauthorized.html')

        return wrapper

    return decorator
