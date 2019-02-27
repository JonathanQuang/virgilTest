

#following virgil's tutorial on their website

from virgil_sdk.jwt.providers import CallbackJwtProvider

# Get generated token from server-side
def get_token_from_server():
    jwt_from_server = aunthficated_query_to_server(token_context)
    return jwt_from_server

# setup access token
access_token_provider = CallbackJwtProvider(get_token_from_server)

#-------------------------------------


import datetime

from virgil_crypto import VirgilCrypto
from virgil_crypto.access_token_signer import AccessTokenSigner
from virgil_sdk.jwt import JwtGenerator
from virgil_sdk.utils import Utils


#
#

# API_KEY (you got this Key at Virgil Dashboard)
api_key_base64 = "MIGhMF0GCSqGSIb3DQEFDTBQMC8GCSqGSIb3DQEFDDAiBBC7Sg/DbNzhJ/uakTvafUMoAgIUtzAKBggqhkiG9w0CCjAdBglghkgBZQMEASoEEDunQ1yhWZoKaLaDFgjpxRwEQAFdbC8e6103lJrUhY9ahyUA8+4rTJKZCmdTlCDPvoWH/5N5kxbOvTtbxtxevI421z3gRbjAtoWkfWraSLD6gj0="
api_key_base64 = "MC4CAQAwBQYDK2VwBCIEIF+gQkN4StqMMFJGWE1tKXcitkLqHqmrBz+OaQZKGZFR" 

private_key_data = Utils.b64_decode(api_key_base64)



# Crypto library imports a private key into a necessary format
crypto = VirgilCrypto()
api_key = crypto.import_private_key(private_key_data)

#  initialize accessTokenSigner that signs users JWTs
access_token_signer = AccessTokenSigner()

# use your App Credentials you got at Virgil Dashboard:
app_id = "6af75f0dd9be50ebb77facad0f71eaf3"
app_key_id = "3def16346c7b43bbaed5b4b9ac8affa4"
ttl = datetime.timedelta(hours=1).seconds

# setup JWT generator with necessary parameters:
jwt_generator = JwtGenerator(app_id, api_key, app_key_id, ttl, access_token_signer)

# generate JWT for a user
# remember that you must provide each user with his unique JWT
# each JWT contains unique user's identity (in this case - Alice)
# identity can be any value: name, email, some id etc.
identity = "Alice"
alice_jwt = jwt_generator.generate_token(identity)

# as result you get users JWT, it looks like this: "eyJraWQiOiI3MGI0NDdlMzIxZjNhMGZkIiwidHlwIjoiSldUIiwiYWxnIjoiVkVEUzUxMiIsImN0eSI6InZpcmdpbC1qd3Q7dj0xIn0.eyJleHAiOjE1MTg2OTg5MTcsImlzcyI6InZpcmdpbC1iZTAwZTEwZTRlMWY0YmY1OGY5YjRkYzg1ZDc5Yzc3YSIsInN1YiI6ImlkZW50aXR5LUFsaWNlIiwiaWF0IjoxNTE4NjEyNTE3fQ.MFEwDQYJYIZIAWUDBAIDBQAEQP4Yo3yjmt8WWJ5mqs3Yrqc_VzG6nBtrW2KIjP-kxiIJL_7Wv0pqty7PDbDoGhkX8CJa6UOdyn3rBWRvMK7p7Ak"
# you can provide users with JWT at registration or authorization steps
# Send a JWT to client-side
jwt_string = alice_jwt.to_string()


#---------------------------github tutorial below

from virgil_crypto import VirgilCrypto
from virgil_sdk.storage import PrivateKeyStorage, KeyStorage, PrivateKeyExporter

crypto = VirgilCrypto()


# generate a key pair
key_pair = crypto.generate_keys()


#setup privateKeyStorage
exporter = PrivateKeyExporter(crypto)
private_key_storage = PrivateKeyStorage(exporter)
print(private_key_storage)


# save Alice private key into key storage
private_key = key_pair.private_key
#private_key_storage.store(private_key, "Alice")


# create and publish user's card with identity Alice on the Card Service

#   api never explicity mentioned how to setup a card manager, so here's to my attempt, 
#   starting with setting up a VirgilCardVerifier

from virgil_crypto.card_crypto import CardCrypto
from virgil_sdk import CardManager, VirgilCardVerifier
from virgil_sdk.verification import VerifierCredentials, WhiteList


#       initialize Crypto library
public_key_str = key_pair.public_key
card_crypto = CardCrypto()
your_backend_verifier_credentials = VerifierCredentials(signer="YOUR_BACKEND", public_key_base64=public_key_str)

your_backend_white_list = WhiteList()
your_backend_white_list.verifiers_credentials = your_backend_verifier_credentials

verifier = VirgilCardVerifier(card_crypto, white_lists=[your_backend_white_list])


# initialize card_manager and specify access_token_provider, card_verifier
card_manager = CardManager(
    card_crypto,
    access_token_provider,
    verifier
)


print(card_manager)

#we're going to try and generate a raw card
from virgil_sdk.cards.raw_card_content import RawCardContent

rawCardObject = RawCardContent(
        "Alice",
        key_pair.public_key,
        0,
        "1.0",
        None
)

"""
card =  card_manager.publish_card(
        raw_card = rawCardObject
        )

card = card_manager.publish_card(
    identity="Alice",
    private_key=key_pair.private_key,
    public_key=key_pair.public_key
)
"""


#end first part of the github example code

from virgil_sdk.utils import Utils

# prepare a message
message_to_encrypt = "Hello, Bob!"
my_str_as_bytes = str.encode("Hello, Bob!")
#data_to_encrypt = Utils.strtobytes((message_to_encrypt,'utf-8'))
data_to_encrypt = my_str_as_bytes
alice_private_key, alice_private_key_additional_data = private_key_storage.load("Alice")

# using CardManager search for Bob's cards on Cards Service
cards = card_manager.search_card("Bob")
print(cards)
bob_relevant_public_keys = list(map(lambda x: x.public_key, cards))

# sign a message with a private key then encrypt using Bob's public keys
encrypted_data = crypto.sign_then_encrypt(data_to_encrypt, alice_private_key, bob_relevant_public_keys)
