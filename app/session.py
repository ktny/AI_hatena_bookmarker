import config
from requests_oauthlib import OAuth1Session


def create_hatena_session():
    # 認証情報を使ってOAuth1Sessionオブジェクトを作成
    return OAuth1Session(
        config.HATENA_CONSUMER_KEY,
        client_secret=config.HATENA_CONSUMER_SECRET,
        resource_owner_key=config.HATENA_ACCESS_TOKEN,
        resource_owner_secret=config.HATENA_ACCESS_TOKEN_SECRET,
    )
