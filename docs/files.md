# Files permission system

All the media access is throttled through a view, \
that utilizes `AdminFilePermissionResolver`. \
That class uses the provided admin site, model name and object pk \
to resolve if there is a valid permission for the object from \
the request's user.

each file (image/file) is either:
- connected to an object (on the model)
- connected to an object through an m2m relation

in each case always a path is produced for storing the file: \
    `<model_name>/<object.pk>/filename`

That path is dynamically provided through \
`get_file_path` method on the instance's model.

in case the `model_name` is the model's that the `Image/FileField` is connected \
then the file must be appended after the creation of the object to ensure \
the `object.pk` part of the path.

In case the `object.pk` is provided as `"none"`, \
then no object permissions are checked

ALL THE PATHS PRODOCUED THROUGH `get_file_path` \
SHOULD BE TESTED THOROUGHLY THROUGH THE `AdminFilePermissionResolver`
