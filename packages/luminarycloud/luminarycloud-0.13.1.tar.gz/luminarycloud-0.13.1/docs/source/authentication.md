# Authentication

## Table of Contents

- [API Key Authentication](#api-key-authentication)
  - [Creating an API Key](#creating-an-api-key)
  - [Using an API Key](#using-an-api-key)
  - [Revoking an API Key](#revoking-an-api-key)
  - [Deleting an API Key](#deleting-an-api-key)
- [Interactive Authentication with the SDK](#interactive-authentication-with-the-sdk)
- [FAQ](#faq)

## API Key Authentication

### Creating an API Key

Using an API key, you can authenticate with the Python SDK without needing to
interactively log in. To do this, you'll need to obtain an API key from the
[Luminary Cloud Web Application](https://app.luminarycloud.com/) ↗️.

![API key screen](assets/api-key-01-screen.png)

Once logged in, navigate to **My Account**->**Profile** and you'll see a **API Keys** section under the **Profile Information** section. Click "Create API key" to create an API key.

![Create API key](assets/api-key-02-create.png)

A dialog box will appear asking you to enter a name for the API key and to select a duration for the API key. The default duration is three months, but you can select a longer duration from the dropdown menu if necessary. We recommend setting a duration and rotating the API key regularly.

You will be shown the API key; copy and save somewhere secure since you won’t be able to see it again within the Luminary Cloud web application.

One option is to store in a file on your local machine, for example:

Filename: `.env` (for use with python-dotenv)

Contents:

```
LC_API_KEY={MY_API_KEY}
```

### Using an API Key

You can specify an API key in the SDK by creating a new Client with the api_key parameter.

```
import luminarycloud as lc
api_key='{MY_LC_API_KEY}',
my_client=lc.Client(api_key=api_key)
lc.set_default_client(my_client)
```

You can also set the environment variable LC_API_KEY  before importing the luminarycloud SDK.

For example you can load the API key using python-dotenv using a `.env` file:

```
from dotenv import load_dotenv
load_dotenv()

# Initialize SDK after setting LC_API_KEY environment variable
import luminarycloud as lc
```

### Revoking an API Key

If you need to revoke an API key, you can do so by navigating to the API key section under My Account - > API Keys. If an API key is active you should see three dots at the right of the API key row; click this and select “Revoke”.

![Revoke API key](assets/api-key-03-revoke.png)

You’ll see a confirmation dialog box and if confirmed then you will see the API key as inactive (x instead of checkmark).

![Confirm revoke API key](assets/api-key-04-revoke-confirm.png)

### Deleting an API Key

If you need to delete an API key, you can do so by navigating to the API key section under My Account - > API Keys. If an API key is inactive (revoked) you should see three dots at the right of the API key row; click this and select “Delete”.

![Delete API key](assets/api-key-05-delete.png)

You’ll see a confirmation dialog box and if confirmed then you will no longer see the API key in the list.

![Confirm delete API key](assets/api-key-06-delete-confirm.png)

## Interactive Authentication with the SDK

When you first make an API call using the Python SDK, you'll see a message like
this:

```

Interactive login required. Your browser has been opened to visit the following
URL: ...

```

You'll need to open the printed link in your web browser and complete the login
flow using the same login credentials you normally use with the web app.

After logging in, an authentication token will be stored on your computer and
you'll be able to make API calls without having to login again. The token
expires after 30 days and then you'll need to repeat the authentication step.

## FAQ

**What permissions will I have when using the SDK?**

- When you make API calls using the Python SDK, the same permissions apply as
when using the Luminary web app.

**How frequently will I have to login using a web browser?**

- When you use an API key, you don't need to login using a web browser. Otherwise, you will need to login using a web browser every 30 days.

**I lost/forgot my API key. What can I do?**

- You can [create a new API key](#creating-an-api-key) using the web application.

**What is the difference between a revoked and deleted API key?**

- Neither revoked nor deleted API keys can be used to authenticate. A revoked API key is effectively the same as an expired API key and is still visible in the list of API keys, but has an x instead of a checkmark under the "Active" column. A deleted API key no longer appears in the list of API keys.

**Where is the authentication token stored?**

- The authentication token is stored in the `$HOME/.luminarycloud` directory on your computer. The file is named `config` and has a JSON format.
