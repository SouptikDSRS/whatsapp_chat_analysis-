from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
import pandas as pd
from collections import Counter
def fetch_stats(selected_user, df):
    extractor = URLExtract()
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Total messages
    num_messages = df.shape[0]

    # Total words
    words = []
    for message in df['message']:
        words.extend(str(message).split())

    # Total media messages
    num_media_messages = df['message'].str.lower().str.contains('media omitted', na=False).sum()

    # Total links
    num_link = []
    for message in df['message']:
        num_link.extend(extractor.find_urls(str(message)))

    return num_messages, len(words), num_media_messages, len(num_link)


def graph_user(df):
    # Top 5 most active users
    x = df['user'].value_counts().head(5)

    # Percentage of messages
    df_percent = (
        round((df['user'].value_counts() / df.shape[0]) * 100, 2)
        .head(5)
        .reset_index()
        .rename(columns={'index': 'name', 'user': 'percent'})
    )

    return x, df_percent


def create_word_cloud(selected_user, df):
    f = open('stop_hinglish.txt','r')
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    stop_word = f.read()
    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('media omitted', case=False, na=False)]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_word:
                y.append(word)
        return " ".join(y)
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc
def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    stop_word = f.read()
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] !=  r'<Media omitted>\n']
    words = []
    
    stop_word
    for message in temp['message']:
        for word in message.lower().split():
            if word in stop_word:
                words.append(word)
    most_common_word = pd.DataFrame(Counter(words).most_common(20))
    return most_common_word



def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in str(message) if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df



def message_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    time = []
    df['month_num'] = df['dates'].dt.month
    Timeline = df.groupby(['year','month']).count()['message'].reset_index()
    for i in range(Timeline.shape[0]):
        time.append(Timeline['month'][i]+ "-" + str(Timeline['year'][i]))
    Timeline['time'] = time

    return Timeline




def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    df['only_date']=pd.to_datetime(df['dates'].dt.date) 
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline



def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    return df['day_name'].value_counts()



def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    return df['month'].value_counts()