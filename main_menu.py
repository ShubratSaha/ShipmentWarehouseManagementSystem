import boto3
import os
import datetime
import time

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('Shipments')

ans = 'y'
while ans == 'y':
    os.system('clear')
    print(' ___________________________________________________________ ')
    print('|           Shipment Warehouse Management System            |')
    print('|-----------------------------------------------------------|')
    print('|  1. Shipment Received                                     |')
    print('|  2. Shipment Dispatch                                     |')
    print('|  3. List of All Shipments                                 |')
    print('|  4. List of Pending Shipments                             |')
    print('|  5. List of Dispatched Shipments                          |')
    print('|  6. Search Shipment                                       |')
    print('|  7. Exit                                                  |')
    print('|___________________________________________________________|')
    print('')
    ch = int(raw_input('   Enter your choice(1-7) : '))
    if ch == 1:
        os.system('clear')
        print(' ___________________________________________________________ ')
        print('|                     Shipment Received                     |')
        print('|___________________________________________________________|')
        print('')
        s_id = raw_input('   1. Enter the Shipment ID          : ')
        resp = table.get_item(Key={"Shipment_ID": s_id})
        if 'Item' not in resp.keys():
            s_desc = raw_input('   2. Enter the Shipment Description : ')
            s_sender_name = raw_input('   3. Enter the Sender Name          : ')
            s_sender_address = raw_input('   4. Enter the Sender Address       : ')
            s_receiver_name = raw_input('   5. Enter the Receiver Name        : ')
            s_receiver_address = raw_input('   6. Enter the Receiver Address     : ')
            s_value = int(raw_input('   7. Enter the Shipment Value       : '))
            s_rd = str(datetime.datetime.now())
            s_dd = " "
            with table.batch_writer() as batch:
                batch.put_item(Item={"Shipment_ID": s_id, "Description": s_desc,
                                     "Sender_Details": {"Name": s_sender_name, "Address": s_sender_address},
                                     "Receiver_Details": {"Name": s_receiver_name, "Address": s_receiver_address},
                                     "Shipment_Value": s_value, "Receive_Date": s_rd, "Dispatch_Date": s_dd})
            print('   New Shipment Received...')
        else:
            print('   Invalid Shipment ID... Already Exists...')
    elif ch == 2:
        os.system('clear')
        print(' ___________________________________________________________ ')
        print('|                     Shipment Dispatch                     |')
        print('|___________________________________________________________|')
        print('')
        sd_id = raw_input('   1. Enter the Shipment ID to be dispatched : ')
        resp = table.get_item(Key={"Shipment_ID": sd_id})
        if 'Item' in resp.keys():
            if resp['Item']['Dispatch_Date'] != " ":
                print('\n    Shipment Already Dispatched...')
            else:
                print('')
                print(' --------------------- Shipment Details ---------------------')
                print '   1. Shipment ID          : ', resp['Item']['Shipment_ID']
                print '   2. Shipment Description : ', resp['Item']['Description']
                print '   3. Sender Name          : ', resp['Item']['Sender_Details']['Name']
                print '   4. Sender Address       : ', resp['Item']['Sender_Details']['Address']
                print '   5. Receiver Name        : ', resp['Item']['Receiver_Details']['Name']
                print '   6. Receiver Address     : ', resp['Item']['Receiver_Details']['Address']
                print '   7. Shipment_Value       : ', resp['Item']['Shipment_Value']
                print '   8. Receive Date         : ', resp['Item']['Receive_Date']
                dis_ans = raw_input('\n   Are you sure you want to dispatch this shipment(y/n) : ')
                if dis_ans == 'y':
                    dis_date = str(datetime.datetime.now())
                    resp = table.update_item(
                        Key={"Shipment_ID": sd_id},
                        ExpressionAttributeNames={
                            "#dispatch": "Dispatch_Date",
                        },
                        ExpressionAttributeValues={
                            ":id": dis_date,
                        },
                        UpdateExpression="SET #dispatch = :id",
                    )
                    print('\n   Shipment Dispatched Successfully...')
                else:
                    print('\n   Shipment Not Dispatched...')
        else:
            print('   Invalid Shipment ID...')
    elif ch == 3:
        os.system('clear')
        print(' ___________________________________________________________ ')
        print('|                   List of All Shipments                   |')
        print('|___________________________________________________________|')
        print('')
        resp = table.scan()
        ctr = 0
        if 'Items' in resp.keys():
            for i in resp['Items']:
                print(' --------------------- Shipment Details ---------------------')
                print '   1. Shipment ID          : ', i['Shipment_ID']
                print '   2. Shipment Description : ', i['Description']
                print '   3. Sender Name          : ', i['Sender_Details']['Name']
                print '   4. Sender Address       : ', i['Sender_Details']['Address']
                print '   5. Receiver Name        : ', i['Receiver_Details']['Name']
                print '   6. Receiver Address     : ', i['Receiver_Details']['Address']
                print '   7. Shipment Value       : ', i['Shipment_Value']
                print '   8. Receive Date         : ', i['Receive_Date']
                print '   9. Dispatch Date        : ', i['Dispatch_Date']
                print('')
                ctr = 1
        if ctr == 0:
            print('   No Shipments to show...')
    elif ch == 4:
        os.system('clear')
        print(' ___________________________________________________________ ')
        print('|                 List of Pending Shipments                 |')
        print('|___________________________________________________________|')
        print('')
        resp = table.scan()
        ctr = 0
        if 'Items' in resp.keys():
            for i in resp['Items']:
                if i['Dispatch_Date'] == " ":
                    print(' --------------------- Shipment Details ---------------------')
                    print '   1. Shipment ID          : ', i['Shipment_ID']
                    print '   2. Shipment Description : ', i['Description']
                    print '   3. Sender Name          : ', i['Sender_Details']['Name']
                    print '   4. Sender Address       : ', i['Sender_Details']['Address']
                    print '   5. Receiver Name        : ', i['Receiver_Details']['Name']
                    print '   6. Receiver Address     : ', i['Receiver_Details']['Address']
                    print '   7. Shipment Value       : ', i['Shipment_Value']
                    print '   8. Receive Date         : ', i['Receive_Date']
                    print('')
                    ctr = 1
        if ctr == 0:
            print('   No Pending Shipments to show...')
    elif ch == 5:
        os.system('clear')
        print(' ___________________________________________________________ ')
        print('|                List of Dispatched Shipments               |')
        print('|___________________________________________________________|')
        print('')
        resp = table.scan()
        ctr = 0
        if 'Items' in resp.keys():
            for i in resp['Items']:
                if i['Dispatch_Date'] != " ":
                    print(' --------------------- Shipment Details ---------------------')
                    print '   1. Shipment ID          : ', i['Shipment_ID']
                    print '   2. Shipment Description : ', i['Description']
                    print '   3. Sender Name          : ', i['Sender_Details']['Name']
                    print '   4. Sender Address       : ', i['Sender_Details']['Address']
                    print '   5. Receiver Name        : ', i['Receiver_Details']['Name']
                    print '   6. Receiver Address     : ', i['Receiver_Details']['Address']
                    print '   7. Shipment Value       : ', i['Shipment_Value']
                    print '   8. Receive Date         : ', i['Receive_Date']
                    print '   9. Dispatched Date      : ', i['Dispatch_Date']
                    ctr = 1
                    print('')
        if ctr == 0:
            print('   No Dispatched Shipments to show...')
    elif ch == 6:
        os.system('clear')
        print(' ___________________________________________________________ ')
        print('|                      Search Shipment                      |')
        print('|___________________________________________________________|')
        print('')
        sd_id = raw_input('   1. Enter the Shipment ID to be searched : ')
        resp = table.get_item(Key={"Shipment_ID": sd_id})
        if 'Item' in resp.keys():
            print(' --------------------- Shipment Details ---------------------')
            print '   1. Shipment ID          : ', resp['Item']['Shipment_ID']
            print '   2. Shipment Description : ', resp['Item']['Description']
            print '   3. Sender Name          : ', resp['Item']['Sender_Details']['Name']
            print '   4. Sender Address       : ', resp['Item']['Sender_Details']['Address']
            print '   5. Receiver Name        : ', resp['Item']['Receiver_Details']['Name']
            print '   6. Receiver Address     : ', resp['Item']['Receiver_Details']['Address']
            print '   7. Shipment Value       : ', resp['Item']['Shipment_Value']
            print '   8. Receive Date         : ', resp['Item']['Receive_Date']
            print '   9. Dispatch Date        : ', resp['Item']['Dispatch_Date']
        else:
            print('   Invalid Shipment ID...')
    elif ch == 7:
        os.system('clear')
        print('   Exiting...')
        time.sleep(3)
        exit()
    else:
        os.system('clear')
        print('\n   Invalid Choice...')
    print('')
    ans = raw_input('   Do you want to continue(y/n) : ')
