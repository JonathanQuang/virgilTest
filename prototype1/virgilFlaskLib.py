from virgil_sdk.jwt.providers import CallbackJwtProvider
import datetime
from virgil_crypto import VirgilCrypto
from virgil_crypto.access_token_signer import AccessTokenSigner
from virgil_sdk.jwt import JwtGenerator
from virgil_sdk.utils import Utils
from virgil_sdk.storage import PrivateKeyStorage, KeyStorage, PrivateKeyExporter
from virgil_crypto.card_crypto import CardCrypto
from virgil_sdk import CardManager, VirgilCardVerifier
from virgil_sdk.verification import VerifierCredentials, WhiteList

class VirgilFlaskLib:
    
    def __init__(self):
        self.crypto = VirgilCrypto()
        self.api_key_base64 = "MC4CAQAwBQYDK2VwBCIEIF+gQkN4StqMMFJGWE1tKXcitkLqHqmrBz+OaQZKGZFR"
        self.app_id = "6af75f0dd9be50ebb77facad0f71eaf3"
        self.app_key_id = "3def16346c7b43bbaed5b4b9acb9ac8affa4"
        self.api_key = self.crypto.import_private_key(Utils.b64_decode(self.api_key_base64))
        self.ttl = datetime.timedelta(hours=1).seconds
        self.access_token_signer = AccessTokenSigner()
        self.key_pair = self.crypto.generate_keys()

        self.server_crypto = VirgilCrypto()
        self.server_key_pair = self.server_crypto.generate_keys()

        self.server_private_key_data = self.server_crypto.export_private_key(self.server_key_pair.private_key, "test password")
        self.server_public_key_data = self.server_crypto.export_public_key(self.server_key_pair.public_key)
        self.server_private_key_str = Utils.b64encode(self.server_private_key_data)
        self.server_for_client_public = Utils.b64encode(self.server_public_key_data)


        self.server_exporter = PrivateKeyExporter(self.server_crypto)
        self.server_private_key_storage = PrivateKeyStorage(self.server_exporter)
        self.server_public_key_str = self.server_key_pair.public_key
        self.server_card_crypto = CardCrypto()
        self.server_your_backend_white_list = WhiteList()
        self.server_your_backend_white_list = VerifierCredentials(signer="Jonathan",public_key_base64 = self.server_public_key_str)
        self.verifier = VirgilCardVerifier(self.server_card_crypto, white_lists = [self.server_your_backend_white_list])
        self.access_token_provider = CallbackJwtProvider(self.get_token_from_server("Alice"))
        self.card_manager = CardManager(
            self.server_card_crypto,
            self.access_token_provider,
            self.verifier
        )

    def get_private_key(self):
        return self.key_pair.private_key

    def get_public_key(self):
        return self.key_pair.public_key    

    #jwt token generation
    def get_token_from_server(self, token_context):
        #jwt_from_server = authficated_query_to_server(token_context)
        #jwt_from_server = token_context
        jwt_from_server = self.generate_JWT_for_user("Alice")
        return jwt_from_server

    #JWT generator with necessary paramters
    def get_JWT_generator(self):
        return JwtGenerator(self.app_id, self.api_key, self.app_key_id, self.ttl, self.access_token_signer)

    def generate_JWT_for_user(self, identity):
        jwt_generator = self.get_JWT_generator()
        self.identity = identity
        return jwt_generator.generate_token(identity)

    #function is broken
    def publish_card(self):
        #self.card = self.card_manager.publish_card(identity = self.identity, private_key = self.server_key_pair.private_key, public_key = self.server_key_pair.public_key)
        self.card = self.card_manager.publish_card(identity = self.identity, private_key = self.server_key_pair.private_key, public_key = self.server_key_pair.public_key)

    def signAndEncrypt(self, message):
        message_to_encrypt = message
        data_to_encrypt = Utils.strtobytes(message)

        alice_private_key, alice_private_key_additional_data = self.server_private_key_storage.load("Alice")
        
