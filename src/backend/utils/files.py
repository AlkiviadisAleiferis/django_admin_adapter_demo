def get_file_upload_path(instance, filename):
    """
    Generic function for dynamic upload path.

    Automatically calls the Model's ``get_upload_path``
    that provides the proper path, needed to resolve
    the permissions of the file.
    """
    return instance.get_upload_path(filename)
