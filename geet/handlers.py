from geet import core as geet
from geet import about
from getpass import getpass
import subprocess
import sys


def default_handler(args, gurl):
    len_args = len(args)
    if len_args != 1:
        print("  Incorrect request")
        return
    data = args[0]
    owner, repo = _parse_owner_repo(data)
    if owner is None:
        print("  Incorrect request")
        return
    geet_handler(owner, repo, gurl)


def geet_handler(owner, repo, gurl):
    # fetch
    is_success, assets = _fetch(owner, repo, gurl)
    if not is_success:
        return
    # geet asset to download
    name, url = _select_an_asset(assets)
    if name is None:
        return
    # confirm download
    if not _confirm_download():
        return
    # download
    is_success, tempfile, name = _download(name, url, gurl)
    if not is_success:
        return
    # backup first the current version if it exists
    is_success = _backup(owner, repo)
    if not is_success:
        return
    # unpack
    is_success = _unpack(name, tempfile, owner, repo)
    if not is_success:
        return
    # find an installation script
    module, path, root_dir = _find_installation_script(owner, repo)
    if module is None:
        return
    # confirm install
    if not _confirm_install(path):
        return
    # install
    _install(module, root_dir)


def rate_handler(args, gurl):
    """
    This command shows the rate limit.
    Geet uses Github API, so a rate limit exists.
    To increase your rate limit, authenticate yourself.
    To authenticate yourself, use the command "auth"
    in the loop mode.

    Usage:
        rate
    """
    status_code, status_text, data = geet.rate(gurl)
    if status_code is None:
        print("  Check your connection")
    elif status_code not in (200, 304):
        print("  {} {}".format(status_code, status_text))
    else:
        print("  Rate Limit: {}".format(data["limit"]))
        print("  Remaining : {}".format(data["remaining"]))


def auth_handler(args, gurl):
    """
    Authentication will rise up your connection rate limit

    Usage:
        auth
    """
    token = getpass(prompt="  Token: ")
    if token != "":
        gurl.token = token


def install_handler(args, gurl):
    """
    Execute the install script of an app

    Usage:
        install owner/repo
    """
    len_args = len(args)
    if len_args != 1:
        print("  Incorrect request")
        return
    data = args[0]
    owner, repo = _parse_owner_repo(data)
    if owner is None:
        print("  Incorrect request")
        return
    # find an installation script
    module, path, root_dir = _find_installation_script(owner, repo)
    if module is None:
        return
    # confirm install
    if not _confirm_install(path):
        return
    # install
    _install(module, root_dir)


def rollback_handler(args, gurl):
    """
    Rollback to previous version

    Usage:
        rollback owner/repo
    """
    len_args = len(args)
    if len_args != 1:
        print("  Incorrect request")
        return
    data = args[0]
    owner, repo = _parse_owner_repo(data)
    if owner is None:
        print("  Incorrect request")
        return
    is_success, error = geet.rollback(owner, repo)
    if is_success:
        print("  Successfully done")
    elif not is_success and error is not None:
        print("  Failed")
        print("  {}".format(str(error)))
    else:
        print("")


def list_handler(args, gurl):
    """
    List the apps downloaded with Geet

    Usage:
        list
    """
    len_args = len(args)
    if len_args != 0:
        print("  Incorrect request")
        return
    error, data = geet.get_list()
    if error is not None:
        print("  Failed to geet the list of apps")
        print("  {}".format(error))
        return
    if not data:
        print("  - Empty list -")
        return
    print("  - List of apps -\n")
    for owner, repos in data.items():
        for repo in repos:
            print("  {}/{}".format(owner, repo))


def del_handler(args, gurl):
    """
    Delete an app

    Usage:
        del owner/repo
    """
    len_args = len(args)
    if len_args != 1:
        print("  Incorrect request")
        return
    data = args[0]
    owner, repo = _parse_owner_repo(data)
    if owner is None:
        print("  Incorrect request")
        return
    ok = _ask_for_confirmation("Do you confirm this dangerous request ?")
    if not ok:
        print("  Cancelled")
        return
    is_success, error = geet.delete(owner, repo)
    if not is_success:
        print("  Failed")
        print("  {}".format(error))
    else:
        print("  Deleted")


def run_handler(args, gurl):
    """
    Run an app

    Usage:
        run owner/repo
    """
    len_args = len(args)
    if len_args != 1:
        print("  Incorrect request")
        return
    data = args[0]
    owner, repo = _parse_owner_repo(data)
    if owner is None:
        print("  Incorrect request")
        return
    print("  Running...")
    is_success, error = geet.run(owner, repo)
    if not is_success:
        print("  Failed")
        print("  {}".format(error))


def version_handler(args, gurl):
    """
    Show the version

    Usage:
        version
    """
    print("  {}".format(about.VERSION))


def path_handler(args, gurl):
    """ Show the absolute path of an app

    Usage:
        path owner/repo
    """
    len_args = len(args)
    if len_args != 1:
        print("  Incorrect request")
        return
    data = args[0]
    owner, repo = _parse_owner_repo(data)
    if owner is None:
        print("  Incorrect request")
        return
    is_success, path = geet.path(owner, repo)
    if not is_success:
        print("  This app doesn't exist")
        return
    print("  {}".format(path))

# =================================
#            PRIVATE
# =================================
def _parse_owner_repo(val):
    data_splitted = val.split("/")
    if len(data_splitted) != 2:
        return None, None
    if data_splitted[0] == "":
        data_splitted[0] = data_splitted[1]
    elif data_splitted[1] == "":
        data_splitted[1] = data_splitted[0]
    owner, repo = data_splitted
    return owner, repo


def _fetch(owner, repo, gurl):
    status_code, status_text, data = geet.fetch(owner, repo, gurl)
    if status_code not in (200, 304):
        print("  Failed")
        if status_code is None:
            print("  {}".format(status_text))
        else:
            print("  {} {}".format(status_code, status_text))
        return False, None
    print("")
    print("  https://github.com/{}/{}".format(owner, repo))
    assets = _useful_info(data)
    return True, assets


def _useful_info(data):
    assets = []
    data = geet.useful_info(data)
    space = "  "
    print("")
    print("{}- Latest Release -\n".format(space))
    print("{}Tag name     : {}".format(space, data["tag_name"]))
    print("{}Target comm. : {}".format(space, data["target_commitish"]))
    print("{}Created at   : {}".format(space, data["created_at"]))
    print("{}Published at : {}".format(space, data["published_at"]))
    print("{}Author login : {}".format(space, data["author_login"]))
    assets_count = len(data["assets"])
    if assets_count == 0:
        return assets
    print("\n  Asset{}:".format("s" if assets_count > 1 else ""))
    for i, asset in enumerate(data["assets"]):
        cache = (asset["name"], asset["url"])
        assets.append(cache)
        print("")
        print("{}-{}-".format(space*2, i))
        print("{}Name           : {}".format(space*2, asset["name"]))
        print("{}Size           : {} bytes".format(space*2, asset["size"]))
        print("{}Created at     : {}".format(space*2, asset["created_at"]))
        print("{}Updated at     : {}".format(space*2, asset["updated_at"]))
        print("{}Uploader login : {}".format(space*2, asset["uploader_login"]))
        print("{}Download count : {}".format(space*2, asset["download_count"]))
        print("{}Content type   : {}".format(space*2, asset["content_type"]))
    return assets


def _select_an_asset(assets):
    count = len(assets)
    if count == 0:
        print("")
        print("  There aren't asset to download")
        return None
    elif count == 1:
        return assets[0]
    print("")
    asset = (None, None)
    index = input("  Pick an asset index: ")
    if index == "":
        print("  You haven't submitted an index")
        return asset
    try:
        index = int(index)
        asset = assets[index]
    except Exception:
        print("  You submitted an incorrect index")
        print("  Cancelled")
    return asset


def _confirm_download():
    print("")
    ok = _ask_for_confirmation("Do you confirm the download ?")
    if ok:
        return True
    print("  Cancelled")
    return False


def _download(name, url, gurl):
    print("")
    print("  Downloading...")
    is_success, error, tempfile, name = geet.download(name, url, gurl)
    if is_success:
        print("  Asset successfully downloaded")
    else:
        print("  Failed to download the asset")
        print("  {}".format(str(error)))
        print("  Cancelled")
    return is_success, tempfile, name


def _unpack(name, tempfile, owner, repo):
    print("")
    print("  Unpacking...")
    is_success, error = geet.unpack(name, tempfile, owner, repo)
    if not is_success:
        print("  Failed to unpack the asset")
        print("  {}".format(str(error)))
        print("  Cancelled")
    else:
        print("  Asset successfully unpacked")
    return is_success


def _backup(owner, repo):
    is_success, error = geet.backup(owner, repo)
    if not is_success and error is not None:
        print("")
        print("  Failed to backup the current version")
        print("  {}".format(error))
        return False
    elif is_success:
        print("")
        print("  Successfully created a backup of the current version")
        return True
    return True


def _find_installation_script(owner, repo):
    print("")
    print("  Searching for an installation script...")
    response = geet.find_install_script(owner, repo)
    is_success = response["is_success"]
    error = response["error"]
    module = response["module"]
    path = response["path"]
    root_dir = response["root_dir"]
    if is_success:
        print("  Found a script")

    elif not is_success and error is not None:
        print("  Failed")
        print("  {}".format(error))
    else:
        print("  There is no install script")
    return module, path, root_dir


def _confirm_install(path):
    print("")
    print("  Install script")
    print("  {}".format(path))
    ok = _ask_for_confirmation("Do you confirm installation ?")
    if ok:
        return True
    print("  Cancelled")
    return False


def _install(module, root_dir):
    print("")
    print("  Installing...")
    p = subprocess.Popen([sys.executable, "-m", module],
                         cwd=root_dir)
    p.communicate()
    print("")
    print("  Done")


def _ask_for_confirmation(message):
    choice = input("  {} (y/N): ".format(message))
    if choice.lower() == "y":
        return True
    return False
