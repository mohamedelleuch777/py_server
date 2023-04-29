import whois


domain = "kartaj.ai"

result = whois.whois(domain)
if result.status is None or result.status == []:
    print(f"The domain {domain} is available!")
else:
    print(f"The domain {domain} is taken!")


print (result.status)