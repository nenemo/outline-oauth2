from flask import Flask, render_template, request
from outline_vpn.outline_vpn import OutlineVPN
from os import environ

app = Flask(__name__)

app_api_url = environ.get('APP_API_URL')

app_api_key = environ.get('APP_API_KEY')

if not app_api_url or not app_api_key:
    print('Environment variable APP_API_URL or APP_API_KEY not set')
    exit(1)


def key_to_dict(key):
    return {
        'key_id': key.key_id,
        'name': key.name,
        'password': key.password,
        'port': key.port,
        'method': key.method,
        'access_url': key.access_url,
        'data_limit': key.data_limit
    }


@app.route('/')
def index():
    email = request.headers.get('X-Forwarded-Email')

    if not email:
        error = u'We couldn’t find the X-Forwarded-Email header and couldn’t determine your email 😔'
        return render_template('index.html', error=error)

    api_url = app_api_url
    api_key = app_api_key
    client = OutlineVPN(api_url, api_key)

    user_key = None
    for key in client.get_keys():
        if key.name == email:
            user_key = key_to_dict(key)
            break

    if not user_key:
        try:
            new_key = client.create_key()
            client.rename_key(new_key.key_id, email)
            user_key = key_to_dict(new_key)
            user_key["name"] = email
        except Exception as e:
            print(str(e))
            error = u'Unfortunately, we couldn’t create an account for you 😔'
            return render_template('index.html', error=error)

    return render_template('index.html', data=user_key)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
