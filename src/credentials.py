import pkce


def create_client_id():
    client_id = input("Please copy and paste your client id")
    return client_id


def create_client_secret():
    client_secret = input("Please copy and paste your client secret")
    return client_secret


def create_code_verifier():
    code_verifier = pkce.generate_code_verifier(length=128)
    return code_verifier
