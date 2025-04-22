# Insafe Connect to Database

### Build library command

`python setup.py sdist bdist_wheel`

### Upload library command

```shell
twine upload dist/*
```

### Install specific version

pip install insafeConnectToDatabase==0.2.2

### Environment setup

To activate cloud sql proxy, add SERVICE_ACCOUNT_KEY environment variable with base64 encoded credentials:

```shell
cat service-account-key.json | base64 | pbcopy
```

### Database Connection issue

while trying to connect to a database, we faced multiple issues as they're following

- connect to a staging database with proxy
    - we should use the library which is going to install the proxy script and read a service account from env
- have conflict with prot number 4532, which is shared between postgres we have in the cloud and the one we
  have in local docker
    - we have to change one of the port numbers

> **Note**: We have to make sure that we have latest cloud sql proxy in the project
> https://github.com/GoogleCloudPlatform/cloud-sql-proxy

- Make sure we have the following in the setup to add library assets

```python
    package_data = {
  'insafeConnectToDatabase': ['cloud-sql-proxy', 'cloud-sql-proxy-linux'],  # Include the script
}

```