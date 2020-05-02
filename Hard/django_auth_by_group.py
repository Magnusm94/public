from django.shortcuts import render
from django.contrib.auth.models import Group


# Checks if a user have the required permissions to access a page based on arguments.
# Can redirect user to a more fitting page. (usable in the project this is for)
# I'm still very new to django, and there is probably better ways of doing it :)
class redirect:

    def __init__(self):
        self.groups = []
        self.permission = []

    def __call__(self, request, *args, **kwargs):
        if args:
            self.check(request, *args)

        if args and not len(self.groups):
            self.suggested_path(request)
            if self.permission:
                end = str(kwargs['file']).split('/')
                path = '%s/%s' % (self.permission[0], end[len(end) - 1])
                return render(request, path)

        if len(self.groups) or not args:
            if 'file' in kwargs.keys():
                return render(request, kwargs['file'])

    def check(self, request, *args):
        self.groups = []
        user = str(request.user.username)
        for arg in args:
            group = Group.objects.get(name=arg)
            users = str(group.user_set.all())
            if user in users:
                self.groups.append(arg)

    # other personalised function made to return a list of which groups the user belongs in.
    def suggested_path(self, request):
        for i in find_group(request):
            self.permission.append(i)