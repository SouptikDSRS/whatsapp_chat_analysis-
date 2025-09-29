import re
import pandas as pd

def preprocess(data):
    clean_data = re.sub(r'\u202f(AM|PM)', '', data)

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message = re.split(pattern, clean_data)[1:]
    dates = re.findall(pattern, clean_data)

    df = pd.DataFrame({'user_message': message, 'message_dates': dates})
    df['message_dates'] = pd.to_datetime(
        df['message_dates'],
        format='%m/%d/%y, %I:%M - ',
        errors='coerce'
    )
    df.rename(columns={'message_dates': 'dates'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    
    df['only_date'] = df['dates'].dt.date
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day_name()
    df['day_name'] = df['dates'].dt.day_name()
    df['hours'] = df['dates'].dt.hour
    df['minutes'] = df['dates'].dt.minute

    return df
