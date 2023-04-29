import requests


API_KEY = "eo1nGwcz6HHZ_UR9M8YNXJhvW5eS428rJFg"
API_SECRET = "PMVmPf6r3PeQcnJ2QG1uaw"


error_reporting = 0
msg = ''
if 'btn' in request.POST:
    if requests.POST['domain']:
        api_key = API_KEY
        api_secret = API_SECRET

        domain = requests.POST['domain']
        domain = domain.replace('www.', '')
        domain = domain.replace('www', '')
        domain = domain.replace('/', '')
        domain = domain.replace(':', '')
        domain = domain.replace('https', '')
        domain = domain.replace('http', '')
        domain = domain.strip()
        domain = requests.utils.requote_uri(domain)

        domain_tld = domain.split('.')
        if not domain_tld[1]:
            domain_tld = domain_tld[0] + '.com'
        else:
            domain_tld = domain

        url = f'https://api.ote-godaddy.com/v1/domains/available?domain={domain_tld}'
        headers = {
            'Authorization': f'sso-key {api_key}:{api_secret}',
        }
        response = requests.get(url, headers=headers)
        check_domain = response.json()

        if check_domain['available'] == 1 or check_domain['available'] == True:
            msg = '<div class="alert alert-success">Congrats! Your domain <strong>{}</strong> is available.</div>'.format(domain_tld)
        elif check_domain['code']:
            msg = '<div class="alert alert-danger">{}</div>'.format(check_domain['fields'][0]['message'])
        elif check_domain['available'] == '' or check_domain['available'] == 0:
            msg = '<div class="alert alert-danger">Sorry! This domain <strong>{}</strong> is already registered.</div>'.format(domain_tld)

        suggest_url = f'https://api.ote-godaddy.com/v1/domains/suggest?query={domain_tld}&limit=5'
        response = requests.get(suggest_url, headers=headers)
        suggest_domain = response.json()
    else:
        msg = '<div class="alert alert-danger">Please enter any domain keyword</div>'
