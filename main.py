import requests
from loguru import logger

from config import (
    USE_PROXY,
    SLEEP_AFTER_REQUEST_SEC,
    RETRY_ATTEMPTS,
    SLEEP_AFTER_FAIL_REQUEST_SEC
)
from constants import (
    EVM_ADDRESSES_PATH,
    PROXIES_PATH,
    EXCEL_EXPORT_PATH,
    API_URL,
)
from utils import (
    read_from_txt,
    export_json,
    change_mobile_ip,
    print_greeting_msg,
    sleep
)


def main():
    print_greeting_msg()

    wallets = read_from_txt(EVM_ADDRESSES_PATH)
    proxies = read_from_txt(PROXIES_PATH)

    if USE_PROXY and len(wallets) != len(proxies):
        logger.error("Proxies count is not equal to wallets count. Terminating...")
        exit()

    logger.info(f'Total wallets to check: {len(wallets)}')

    result = {}
    for wallet in wallets:
        wallet_index = wallets.index(wallet)
        proxy_url = ''
        if USE_PROXY:
            proxy_url = f"http://{proxies[wallet_index]}"

        logger.info(f'Wallet: {wallet}')

        session = requests.Session()
        if USE_PROXY:
            session.proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
        else:
            change_mobile_ip()
        attempts = RETRY_ATTEMPTS
        while True:
            if attempts == 0:
                logger.error('All retry attempts exceeded. Gng to next wallet')
                break
            try:
                resp = session.get(f'{API_URL}{wallet}')
                resp_json = resp.json()
                total = resp_json[0]['points']

                logger.info(f'Total Scroll Marks: {total}')

                result[wallet] = total
                sleep(SLEEP_AFTER_REQUEST_SEC)

                break
            except Exception as e:
                logger.error(f'Failed to get Scroll Marks info.. Attempt: {attempts}')
                logger.error(f'Reason: {e}')
                sleep([SLEEP_AFTER_FAIL_REQUEST_SEC, SLEEP_AFTER_FAIL_REQUEST_SEC])
                attempts = attempts - 1

    logger.info('All wallets fetched. Running export to excel')
    export_json(result, EXCEL_EXPORT_PATH)

    logger.info('Shutting down...')
    exit()


if __name__ == "__main__":
    main()