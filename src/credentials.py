import pkce

# client_id = "48a43f17b4564edfad5c0ab4311df8f8"  # Unique identifier of the application
# client_secret = "88e773d34a074a6aacb009ef29d625cf"  # key used to pass in secure calls to SpotifyApi. Can be
# regenerated.
client_id = input("Please copy and paste your client id")
client_secret = input("Please copy and paste your client secret")
code_verifier = pkce.generate_code_verifier(length=128)
code_challenge = pkce.get_code_challenge(code_verifier)

