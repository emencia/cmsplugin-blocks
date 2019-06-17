def add_to_tuple(var, *args, **kw):
    """
    Append new items inside a tuple.

    This utility method should be used to modify settings tuples and lists.

    Features:

    * Avoid duplicates by checking whether the items are already there;
    * Add many items at once;
    * Allow to add the items before some other item, when order is important
      (by default it appends). If the before item does not exist, just insert
      the value at the end;

    Example:

        INSTALLED_APPS = add_to_tuple(INSTALLED_APPS, 'foo')

        INSTALLED_APPS = add_to_tuple(INSTALLED_APPS, 'foo', 'bar')

        INSTALLED_APPS = add_to_tuple(INSTALLED_APPS, 'first' before='second')

        INSTALLED_APPS = add_to_tuple(INSTALLED_APPS, 'second', after='first')
    """
    before = kw.get('before')
    after = kw.get('after')

    var = list(var)
    for arg in args:
        if arg not in var:
            if before and before in var:
                var.insert(var.index(before), arg)
            elif after and after in var:
                var.insert(var.index(after)+1, arg)
            else:
                var.append(arg)

    return tuple(var)
