
from virgil_sdk.jwt.providers import CallbackJwtProvider

# Get generated token from server-side
def get_token_from_server():
    print(token_context)
    jwt_from_server = aunthficated_query_to_server(token_context)
    return jwt_from_server

# setup access token
access_token_provider = CallbackJwtProvider(get_token_from_server)
print(access_token_provider)
print(get_token_from_server)

import datetime

from virgil_crypto import VirgilCrypto
from virgil_crypto.access_token_signer import AccessTokenSigner
from virgil_sdk.jwt import JwtGenerator
from virgil_sdk.utils import Utils


api_key_base64 = "MC4CAQAwBQYDK2VwBCIEIF+gQkN4StqMMFJGWE1tKXcitkLqHqmrBz+OaQZKGZFR" 

private_key_data = Utils.b64_decode(api_key_base64)
print(private_key_data)

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

identity = "Alice"
alice_jwt = jwt_generator.generate_token(identity)

print("---")
print(alice_jwt)
print("----alice_jwt")
print(alice_jwt.to_string())

from virgil_sdk.storage import PrivateKeyStorage, KeyStorage, PrivateKeyExporter

key_pair = crypto.generate_keys()

exporter = PrivateKeyExporter(crypto)
private_key_storage = PrivateKeyStorage(exporter)

private_key = key_pair.private_key
print("private key storage load Alice")
print(private_key_storage.load("Alice"))
private_key_storage.delete("Alice")
private_key_storage.store(private_key, "Alice")

from virgil_crypto.card_crypto import CardCrypto
from virgil_sdk import CardManager, VirgilCardVerifier
from virgil_sdk.verification import VerifierCredentials, WhiteList

public_key_str = key_pair.public_key
card_crypto = CardCrypto()
your_backend_verifier_credentials = VerifierCredentials(signer="YOUR_BACKEND", public_key_base64=public_key_str)

your_backend_white_list = WhiteList()
your_backend_white_list.verifiers_credentials = your_backend_verifier_credentials

verifier = VirgilCardVerifier(card_crypto, white_lists=[your_backend_white_list])

print('---- verifier ----')
print(verifier)

card_manager = CardManager(
        card_crypto,
        access_token_provider,
        verifier
        )

from virgil_sdk.cards.raw_card_content import RawCardContent

rawCardObject = RawCardContent(
        "Alice",
        key_pair.public_key,
        0,
        "1,0",
        None
        )
print(key_pair.public_key)

card = card_manager.publish_card(
        identity = "Alice",
        private_key = key_pair.private_key,
        public_key = key_pair.public_key
        )

