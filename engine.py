from backend import *

def main():

    ### create accunt and put your IFTTT webhooks API's here to recieve the notification on your phone
    IFTTT_URL = ''

    # _symbol = 'ETH'
    # _coef = 0.01
    # _time = 10

    ### initialize inputs
    _symbol = input('choose between "BTC" and "ETH": ').upper()
    STC_Price = Price(_symbol)
    
    if STC_Price.status:
    
        _coef = float(input('select the coef:'))
        _time = int(input('select the time sleep:'))

        STC_history = []
        
        STC_Post = Webhooks(IFTTT_URL, _symbol)
        NOTICE = DeviceNotice(_symbol)
        sound = Sound()

        ### create the first thereshold list
        ETHEREUM_PRICE_THRESHOLD = STC_Price.thereshold(_coef, STC_Price.get_price())

    ### log price and thereshold
        print()
        print(f'APP SET ON "{_symbol}" STOCKS')
        print(STC_Price.get_price(), '$')
        print(ETHEREUM_PRICE_THRESHOLD)
        print()

        while True:

            STC_Price = Price(_symbol)

            price = STC_Price.get_price()
            date = datetime.now()

            ### save a history of stock's price
            STC_history.append({'date': date, 'price': price})

            if price > ETHEREUM_PRICE_THRESHOLD[1]:

                ### notification on device
                NOTICE.send_notice(price)

                ### post price into webhooks and play sound
                send = STC_Post.send_notice(price=price)
                sound.notice_me()

                if send:
                    print('NOTIFICATIONS SEND AT {}'.format(date.strftime('%H:%M')))
                else:
                    print('NOTIFICATIONS NOT SEND!')
                
                print('PRICE: {}'.format(price))
                ETHEREUM_PRICE_THRESHOLD = STC_Price.thereshold(_coef, price)
                print('NEW THRESHOLD IS: {}\n'.format(ETHEREUM_PRICE_THRESHOLD))
        
            if price < ETHEREUM_PRICE_THRESHOLD[0]:
                
                NOTICE.send_notice(price)
                
                send = STC_Post.send_notice(price=price)
                sound.notice_me()
                if send:
                    print('NOTIFICATIONS SEND AT {}'.format(date.strftime('%H:%M')))
                else:
                    print('NOTIFICATIONS NOT SEND!')
                
                print('PRICE: {}'.format(price))
                ETHEREUM_PRICE_THRESHOLD = STC_Price.thereshold(_coef, price)
                print('NEW THRESHOLD IS: {}\n'.format(ETHEREUM_PRICE_THRESHOLD))
            
            ### limiting the history list
            if len(STC_history) == 10:
                ## print the history price
                ETH_history = []

            ### sleep the loop
            time.sleep(_time)

    else:
        print('CHOOSE CRYPTOCURRENCY SYMBOL CAREFULLY!')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'fixed this issue:\n{e}')