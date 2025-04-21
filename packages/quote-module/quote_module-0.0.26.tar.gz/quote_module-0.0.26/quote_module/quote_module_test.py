import datetime
import time
import quote_module.quote_module as qm
from collections import defaultdict
import argparse

dict_serial_number = defaultdict(int)


def callback_pcap_read(quote: qm.QuoteS):
    pass
    if quote.pause != 0:
        print(quote)
        print(f'{quote.code_str} {quote.timestamp_str} close: {quote.close_price}, bool close:{quote.bool_close}, volume: {quote.close_volume}, '
              f'volume acc: {quote.volume_acc}, ask price: {quote.ask_price}, ask volume: {quote.ask_volume}, bid price: {quote.bid_price}, bid volume: {quote.bid_volume}, '
              f'bool continue: {quote.bool_continue}, bool bid price: {quote.bool_bid_price}, bool ask price: {quote.bool_ask_price}, bool odd: {quote.bool_odd}, '
              f'num ask: {quote.number_best_ask}, num bid: {quote.number_best_bid}, tick type: {quote.tick_type}, bool simtrade: {quote.bool_simtrade}, Pause: {quote.pause}, '
              f'now second: {quote.double_now_seconds}, msg type: {quote.message_type}, serial: {quote.serial_number}\n\n')

    last_serial_number = dict_serial_number[quote.message_type]
    if quote.serial_number != last_serial_number + 1:
        print(f'Error: {quote.message_type} {quote.serial_number} {last_serial_number}')
    dict_serial_number[quote.message_type] = quote.serial_number


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process pcap files in live or offline mode.')
    parser.add_argument('-r', '--read', type=str, help='Offline mode: specify the pcap file to read from.')
    parser.add_argument('-live', '--live', type=str, choices=['ml1', 'ml2', 'ml3', 'ml4', 'kgi', 'capital'], help='Live mode: specify the source type.')
    args = parser.parse_args()

    # Check if neither -r nor -live is provided
    if not args.read and not args.live:
        parser.print_help()
        return

    # Determine mode and execute accordingly
    if args.read:
        # Offline mode
        qm.set_offline_pcap_callback(callback_pcap_read)
        qm.start_offline_pcap_read(args.read)

        while True:
            ret = qm.check_offline_pcap_read_ended()
            if ret != 0:
                break
            # print(f'{datetime.datetime.now()} {ret}')
            time.sleep(1)

    elif args.live:
        # Live mode
        if args.live == 'ml1':
            qm.INTERFACE_IP_TSE = '10.175.1.17'
            qm.INTERFACE_IP_OTC = '10.175.2.17' 
            qm.INTERFACE_IP_FUT = '10.71.17.74'

        elif args.live == 'ml2':
            qm.INTERFACE_IP_TSE = '10.175.1.18'
            qm.INTERFACE_IP_OTC = '10.175.2.18' 
            qm.INTERFACE_IP_FUT = '10.71.17.74'
        elif args.live == 'ml3':
            qm.INTERFACE_IP_TSE = '10.175.2.21'
            qm.INTERFACE_IP_OTC = '10.175.1.21' 
            qm.INTERFACE_IP_FUT = '10.71.17.74'
        elif args.live == 'ml4':
            qm.INTERFACE_IP_TSE = '10.175.1.22'
            qm.INTERFACE_IP_OTC = '10.175.2.22' 
            qm.INTERFACE_IP_FUT = '10.71.17.74'
        elif args.live == 'kgi':
            qm.INTERFACE_IP_TSE = '10.101.214.58'
            qm.INTERFACE_IP_OTC = '10.101.214.58' 
            qm.INTERFACE_IP_FUT = '10.101.214.58'
        elif args.live == 'capital':
            qm.INTERFACE_IP_TSE = '10.75.80.25'
            qm.INTERFACE_IP_OTC = '10.75.80.25' 
            qm.INTERFACE_IP_FUT = '10.75.80.25'

        qm.set_mc_live_pcap_callback(callback_pcap_read)
        qm.start_mc_live_pcap_read()


if __name__ == "__main__":
    main()
