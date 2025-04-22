# ckanext-selfinfo

This extension is built to represent a basic information about the running CKAN Application accessible only to admins.

CKAN should be configured to be able to connect to Redis as it heavily relies on it for storage.

On CKAN admin page `/ckan-admin/selfinfo`, admin can see such information as:
* System Information
    - System Platform
    - Distribution
    - Python version
* RAM
    - RAM Usage in %
    - RAM Usage GB
    - RAM Total
    - Monitor feature
        - Top 10 processes shown
* Disk Space
    - Path
    - Disk Usage in %
    - Disk Total
    - Disk Free
* CKAN Information
    - Basic Information
    - Actions
    - Auth
    - Helpers
    - Blueprints
* GIT Information (Optional, see Config Settings section)
    - Project
    - Head
    - Based on
    - Commit
    - Remotes
    - Errors info in case if cannot be shown
* PIP Freeze
    - List of modules that are installed.
* Python Information
    - Provides information about CKAN Core, CKAN Extensions, Python installed packages. It shows their current version and latest version.
* Errors (Optional, see Enable Error Saving section)
    - Shows latest exceptions.

## Requirements

Having CKAN Core version 2.10+

Installing the packages mentioned in `requirements.txt` file.


## Installation

To install ckanext-selfinfo:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com//ckanext-selfinfo.git
    cd ckanext-selfinfo
    pip install -e .

3. Add `selfinfo` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Developer installation

To install ckanext-selfinfo for development, activate your CKAN virtualenv and
do:

    git clone https://github.com//ckanext-selfinfo.git
    cd ckanext-selfinfo
    python setup.py develop


## Config Settings

`ckan.selfinfo.redis_prefix_key` - This configuration is needed, when you use Redis with multiple CKAN apps. In order to have a unique key per portal, this configuration can be used. Example `ckan_test` will be used as `ckan_test_errors_selinfo`.

`ckan.selfinfo.page_url` - (Recommended to use) Used to provide alternative URL to Selfinfo Admin Page. By default it is set to `/ckan-admin/selfinfo`.

`ckan.selfinfo.main_action_name` - (Recommended to use) Used to provide an alternative name for the main action of selfinfo. By default it is set to `get_selfinfo`.

`ckan.selfinfo.partitions` - Used for representing disk space. The value is comma separated paths. By default the value is `/`, which is usually the root.

Example: `/path/to/partition /path/to/partition2 /path/to/partition3`

`ckan.selfinfo.errors_limit` - Limit used to specify how much errors will be stored in Redis. By default this value is `40`.

`ckan.selfinfo.ckan_repos_path` - Path to the src folder where CKAN and CKAN Extensions stored at the environment. While provided, additional GIT Infromation will be granted. Make sure that there no other folders and files that are not related to CKAN are stored there. Example: `/usr/lib/ckan/default/src`

`ckan.selfinfo.ckan_repos` - List of CKAN Extension folders separated by space (ckanext-scheming ckanext-spatial ckanext-xloader). By default, if `ckan.selfinfo.ckan_repos_path` is provided, it will look into the directory and gather the extensions from there.

#### NOTE!
For Linux, keep in mind that the added folder in `ckan.selfinfo.ckan_repos_path` should have the same owner as the one that runs the application (e.g. if the application runs from `ckan` User in the system, then ckanext-scheming folder owner should be `ckan`), otherwise there will be an error related to ownership of the repository.

Errors for GIT now being stored below the original Table on GIT Info tab.

`ckan.selfinfo.additional_profiles_using_redis_keys` - Retrieves selfinfo data on page from external sources that store selfinfo data using `write-selfinfo` cli command under unique Redis key. The stored data should be under same Redis connection as per the "default" profile.

Example: `unique_redis_key_1 unique_redis_key_2`

`ckan.selfinfo.categories_list` - (Optional) List of categories that should be shown on Selfinfo Page or Returned using API. Example of usage `ckan.selfinfo.categories_list = errors ram_usage disk_usage`.
By default shows all configured categories.

Next section shows current categories list.

## Full list of current categories:

* python_modules
* platform_info
* ram_usage
* disk_usage
* git_info
* freeze
* errors
* actions
* auth_actions
* blueprints
* helpers
* status_show

## Enable Errors Saving
In CKAN INI file, need to add and modify few lines.

After `handler_console` section add:

    [handler_selfinfoErrorHanlder]
    class = ckanext.selfinfo.handlers.SelfinfoErrorHandler
    level = ERROR
    formatter = generic

In `handlers` modify the `keys`, example:

    [handlers]
    keys = console, selfinfoErrorHanlder

In `logger_ckan` modify `handlers`, example:

    [logger_ckan]
    level = INFO
    handlers = console, selfinfoErrorHanlder
    qualname = ckan
    propagate = 0


## CLI

`selfinfo write-selfinfo` - Stores selfinfo data under unique Redis key. This data can be retrieved by selfinfo page if `ckan.selfinfo.additional_profiles_using_redis_keys` is set with the stored keys.

Arguments:
* key - Unique Redis key. Example `CKAN_Additional_Selfinfo_Source`
* label - (Optional) Label to be displayed on selfinfo page. Example `"Additional Selfinfo Source"`. If not provided, `key` will be used as label instead.

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-selfinfo

If ckanext-selfinfo should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

MIT
