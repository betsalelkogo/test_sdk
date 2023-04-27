#from asyncio.windows_events import NULL
from itertools import chain


from multiprocessing.connection import Client
import pdb
import sys
import re
from pprint import pprint
from fireblocks_sdk import FireblocksSDK, TransferPeerPath, DestinationTransferPeerPath, \
    TRANSACTION_STATUS_CONFIRMED, TRANSACTION_STATUS_CANCELLED, TRANSACTION_STATUS_REJECTED, \
    TRANSACTION_STATUS_FAILED, VAULT_ACCOUNT, TRANSACTION_MINT, \
    TRANSACTION_BURN, ONE_TIME_ADDRESS, EXTERNAL_WALLET, PagedVaultAccountsRequestFilters

def connection(user):
    apiKey = user
    fireblocks = FireblocksSDK(apiSecret, apiKey)
    return fireblocks

#users:
admin = 'xyz'  
viewer = 'xyz'
admin_noco = 'xyz'
non_sign_Admin = 'xyz'
signer= 'xyz'
apiSecret = open('fireblocks_secret.key', 'r').read()

#____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# #Template:
# def FunctionName(fireblocks):
#     variable = fireblocks.function_name(parameter_from_doc='parameter_value')

#     pprint(variable)
# FunctionName(connection(user))

#Example:

# def rami_get_users_please(fireblocks):
#    users = fireblocks.get_users()
#    pprint(users)
# rami_get_users_please(connection(non_sign_Admin))
#______________________________________________________________________________________________________________________


def list_exc(fireblocks):
    exchangeAccounts = fireblocks.get_exchange_accounts()
    pprint(exchangeAccounts)

# list_exc(connection(admin))



def test200(fireblocks):
    vault_accounts = fireblocks.get_vault_accounts_with_page_info(
        PagedVaultAccountsRequestFilters(limit=10, order_by='ASC'))
    nextPage = vault_accounts.get('nextUrl')
    pervPage = vault_accounts.get('previousUrl')
    pprint(vault_accounts)
    pprint(fireblocks.get_vault_accounts_with_page_info(
        PagedVaultAccountsRequestFilters(limit=10, order_by='ASC', after=nextPage)))
#test200((connection(viewer)))



def EXC(fireblocks):
    vaultAsset = fireblocks.get_unspent_inputs(0,"BTC_TEST")
    pprint(vaultAsset)

#EXC(connection(admin))




def ct(fireblocks, asset, src, amount,  dest):
    tx_result = fireblocks.create_transaction(
        asset_id=asset,
        amount=amount,
        source=TransferPeerPath(VAULT_ACCOUNT, src),
        destination=DestinationTransferPeerPath(ONE_TIME_ADDRESS, one_time_address={"address": dest})
    )
    print(tx_result)

# for x in chain(range(0,5)):
#     ct(connection(admin), "SOL_TEST", 0, 0.499975, "BCqWgTGroeHC3YBBvTzBB9u6uH847B1A5MCPEsNf631E")







#Transactions:
#--------------------------------------------------------------------#

def ct1(fireblocks, asset, src, amount,  dest):
    tx_result = fireblocks.create_transaction(
        asset_id=asset,
        amount=amount,
        source=TransferPeerPath(VAULT_ACCOUNT, src),
        #destination=DestinationTransferPeerPath(VAULT_ACCOUNT, 0)
        #priority_fee=70,
        #max_fee="71",
        #fee=0.02,
        destination=DestinationTransferPeerPath(ONE_TIME_ADDRESS, one_time_address={"address": dest})
    )
    print(tx_result)
#ct1(connection(admin),  "SOL_TEST", 0, 0.499975, "BCqWgTGroeHC3YBBvTzBB9u6uH847B1A5MCPEsNf631E")
#ct1(connection(admin), "ETH_TEST3", 0, 0.0001, "0xc4e887BE206Bfc376837Cd1754AfA55617159A48")


def CanclT(fireblocks,txId):
    result = fireblocks.cancel_transaction_by_id(txId)
    
    print(result)

#CanclT(connection(admin),"c42cd4a5-4259-4fed-ad44-c30eb38b0bb2")




def txWhat(fireblocks,txId):
    tx = fireblocks.get_transaction_by_id(txId)

    
    print(tx)

#txWhat(connection(viewer),"accbc0f8-480b-4f1f-bdd7-a72540d6a9c5")



def txWhat_non(fireblocks):
    transactions = fireblocks.get_transactions()
    print(transactions)


#txWhat_non(connection(admin))




def ct_utxo(fireblocks, asset, src, amount, dest):
    tx_result = fireblocks.create_transaction(
        asset_id=asset,
        amount=amount,
        fee=3,
        source=TransferPeerPath(VAULT_ACCOUNT, src),
        destination=DestinationTransferPeerPath(ONE_TIME_ADDRESS, one_time_address={"address": dest}),
        extra_parameters={"inputsSelection":{"inputsToSpend": [{'index': '0','txHash': '8ebd42b53302826aa624b0c6270c6737c73f62ae3fc3257c7353f4c4d2e85ab6','index': '0','txHash': 'b5a81bca8812b540bb079d57849f94ac21fbabab68fb3a52e3a8d0f02c5bee21'}]}}
    

    )
    print(tx_result)

#ct_utxo(connection(admin), "BTC_TEST", 3, 0.00007, "n4ESysTttGuj6uFdQGBxPXBFJaQwdWd5Yr")


#--------------------------------------------------------------------#

def inputsUtxo(fireblocks):
    vaultAsset = fireblocks.get_unspent_inputs("3", "BTC_TEST")
    pprint(vaultAsset)
#inputsUtxo(connection(admin))




def EST(fireblocks):
    fee_result = fireblocks.get_fee_for_asset("WND")
    pprint(fee_result)
#EST(connection(admin))



def EST_FEE(fireblocks,amount):
    estimated_fee = fireblocks.estimate_fee_for_transaction(
        asset_id="WND",
        amount=amount,
        source=TransferPeerPath(VAULT_ACCOUNT, 0),
        destination=DestinationTransferPeerPath(VAULT_ACCOUNT, 1)
       #extra_parameters={"inputsSelection":{"inputsToSpend": [{'index': '1','txHash': '4d43694a12159fddb612248008aeb876f51f42502254176c63b06cdff2a29430'}]}}


        )
    pprint(estimated_fee)
        
#EST_FEE(connection(admin),"1")
#EST_FEE(connection(admin),0.0015)


def EST_FEE_contract(fireblocks,amount):
    estimated_fee = fireblocks.estimate_fee_for_transaction(
        asset_id="DOGE_TEST",
        operation='CONTRACT_CALL',
        amount=amount,
        source=TransferPeerPath(VAULT_ACCOUNT, 0),
        destination=DestinationTransferPeerPath(VAULT_ACCOUNT, 1),
        extra_parameters={"contractCallData":''}
        )
    pprint(estimated_fee)
#EST_FEE_contract(connection(admin),"1")



def UNSPENT(fireblocks):
    vaultAsset = fireblocks.get_unspent_inputs(0,'BTC_TEST')
    pprint(vaultAsset)    
#UNSPENT(connection(admin))





def Supa(fireblocks):
    supportedAssets = fireblocks.get_supported_assets()
    pprint(supportedAssets)   

#Supa(connection(signer))


def addre(fireblocks):
   depositAddresses = fireblocks.get_deposit_addresses(0, "ETH_TEST")
   pprint(depositAddresses)

#addre(connection(non_sign_Admin))



def set_ref(fireblocks):
   vaultAsset = fireblocks.set_vault_account_customer_ref_id_for_address('4', 'BTC_TEST', 'tb1q4rt7kwgsrx5f3w5aqul8m29e6vdel3dg0q0s8h', 'test_test')
   #vaultAsset = fireblocks.set_vault_account_customer_ref_id('4','')
   pprint(vaultAsset)

#set_ref(connection(non_sign_Admin))



def get_vault(fireblocks):
   vault_account = fireblocks.get_vault_account(4)
   pprint(vault_account)

#get_vault(connection(non_sign_Admin))


def contract_wallets(fireblocks):
   contracts = fireblocks.get_contract_wallets()
   pprint(contracts)

#contract_wallets(connection(viewer))

def refresh_asset(fireblocks):
   vaultAsset = fireblocks.refresh_vault_asset_balance('0', 'BTC_TEST')
   pprint(vaultAsset)

#refresh_asset(connection(non_sign_Admin))


def assets_balance1(fireblocks):
   assets_balance = fireblocks.get_vault_balance_by_asset('BTC_TEST')
   pprint(assets_balance)

#a---=ssets_balance1(connection(signer))



def get_vault_account_asset1(fireblocks):
   vaultAsset = fireblocks.get_vault_account_asset('0','ETH_TEST')
   pprint(vaultAsset)

#get_vault_account_asset1(connection(signer))


def add_asset_wallet(fireblocks):
   internalWalletAsset = fireblocks.create_internal_wallet_asset(3, 'ETH_TEST','0x5a7c7F4604A871a3Ea7d663295079190650f75d9')
   pprint(internalWalletAsset)

#add_asset_wallet(connection(admin))




def freezetx(fireblocks):
   result = fireblocks.freeze_transaction('27dafe4a-59dd-4b91-8798-95d5c42b86a3')

   pprint(result)

#freezetx(connection(admin))

def get_vault_assets_balance1(fireblocks):
    assets_balance = fireblocks.get_vault_assets_balance('elidor')

    pprint(assets_balance)

#get_vault_assets_balance1(connection(admin))




def Contract123(fireblocks):
    contracts = fireblocks.create_contract_wallet('Yonatan')

    pprint(contracts)

#Contract123(connection(admin))


def internal_w(fireblocks):
    internalWallets = fireblocks.get_internal_wallets()

    pprint(internalWallets)

#internal_w(connection(admin))


def freeze(fireblocks,txidd):
    result = fireblocks.freeze_transaction_by_id(txidd)
    pprint(result)

#freeze(connection(admin),'24455df8-92b3-416c-bb27-6bb1190fafd2')


def unfreeze(fireblocks,txidd):
    result = fireblocks.unfreeze_transaction_by_id(txidd)
    pprint(result)
#unfreeze(connection(admin),'24455df8-92b3-416c-bb27-6bb1190fafd2')



def vault_assets_balance(fireblocks,):
    ssets_balance = fireblocks.get_vault_assets_balance( )
    pprint(ssets_balance)
#vault_assets_balance(connection(admin))

def list_transactions(fireblocks):
    transactions = fireblocks.get_transactions(source_id='0')
      
    pprint(transactions)
#list_transactions(connection(admin))


def get_ext_tx(fireblocks):
    tx = fireblocks.get_transaction_by_external_id('e0830fd7-ba3b-46b0-907c-8c5274f6404f')
     
    pprint(tx)
#get_ext_tx(connection(admin))