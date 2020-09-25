import pkce

client_id = "48a43f17b4564edfad5c0ab4311df8f8"  # Unique identifier of the application
client_secret = "88e773d34a074a6aacb009ef29d625cf"  # key used to pass in secure calls to SpotifyApi. Can be
# regenerated.

# def get_auth_code():
#     if __name__ == "__main__":
#         auth_code = input("please copy the code")


def get_code_verifier():
    code_verifier = pkce.generate_code_verifier(length=128)
    return code_verifier

def get_challenge_code():
    code_verifier = get_code_verifier()
    code_challenge = pkce.get_code_challenge(get_code_verifier())
    return code_challenge
