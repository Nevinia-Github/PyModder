def check_os_contains(arr):
    for osKey, osValue in arr:
        if osKey == "name" and osValue == 'windows':
            return True
    return False


def check_os(arr):
    require = True

    for job in arr:
        action = True  # allow / disallow
        contain = True

        for key, value in job.items():

            if key == "action":
                if value == "allow":
                    action = True
                else:
                    action = False

            elif key == "os":
                contain = check_os_contains(value.items())

            elif key == "features":
                return False

        if not action and contain:  # disallow os
            require = False
        elif action and contain:  # allow os
            require = True
        elif action and not contain:  #
            require = False

    return require