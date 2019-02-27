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

from virgil_sdk.jwt import JwtGenerator
from virgil_sdk.utils import Utils
from virgil_sdk.jwt.providers import CallbackJwtProvider

class VirgilServerClient:

    def __init__(self):
        print("generated")
    
    ####SERVER SIDE
    def authenticated_query_to_server(self,token_context, token_ttl=9999):
        self.crypto = VirgilCrypto()
         

        self.app_key_base64 = "MC4CAQAwBQYDK2VwBCIEIEtNPMUG9uR8YxukWw1gX3bkXjbsbOZoN54d2ZKSz09a"
#        self.app_key_base64 = "MC4CAQAwBQYDK2VwBCIEIJvD17QhpJ1qFfIq3q8eqrZ0oBIf9GQ0T+6obQCmspnQ"
        #self.app_key_base64 = "MC4CAQAwBQYDK2VwBCIEIF+gQkN4StqMMFJGWE1tKXcitkLqHqmrBz+OaQZKGZFR"
        #self.app_id = "6af75f0dd9be50ebb77facad0f71eaf3"
        self.app_id = "def16346c7b43bbaed5b4b9ac8affa4"
#        self.api_key_id = "3def16346c7b43bbaed5b4b9acb9ac8affa4"
        self.api_key_id = "309d53349835f34d5a03966d9de51877" 

        self.app_key = self.crypto.import_private_key(Utils.b64decode(self.app_key_base64))

        self.builder = JwtGenerator(
            self.app_id,
            self.app_key,
            self.api_key_id,
            token_ttl,
            AccessTokenSigner()
        )

        #self.identity = token_context.identity
        #return self.builder.generate_token(self.identity).to_string()
        #PLEASE MAKE TOKEN_CONTEXT AN ACTUAL JWT TOKEN
        #return self.builder.generate_token(token_context)
        try:
            self.identity = token_context.identity
            return self.builder.generate_token(self.identity).to_string()
        except:
            return self.builder.generate_token(token_context)
    

    ########CLIENT SIDE
    def get_token_from_server(self,token_context):
        print('get token from server')
        print(token_context)
        jwt_from_server = self.authenticated_query_to_server(token_context)
        return jwt_from_server

    def set_access_token_provider(self):
        self.access_token_provider = CallbackJwtProvider(self.get_token_from_server)

    def publish_card(self,user):
        self.client_crypto = VirgilCrypto()
        card_crypto = CardCrypto()
        validator = VirgilCardVerifier(card_crypto)
        token_provider = CallbackJwtProvider(self.get_token_from_server)
        print('token_provider')
        print(vars(token_provider))
        card_manager = CardManager(
            card_crypto,
            access_token_provider = token_provider,
            card_verifier = validator
        )

        key_pair = self.client_crypto.generate_keys()
        
        username = user
        public_key_data = self.client_crypto.export_public_key(key_pair.public_key)
        public_key_str = Utils.b64encode(public_key_data)

        class DummyClass:
            def __init__(self, raw_key):
                self.raw_key = raw_key

        dummy = DummyClass(key_pair.public_key.raw_key)    
    
        print(public_key_data)
        print(public_key_str)
        print(key_pair.public_key)

        card = card_manager.publish_card(
            identity = username,
            private_key = key_pair.private_key,
            public_key = key_pair.public_key
        )
        print(vars(card))
    
